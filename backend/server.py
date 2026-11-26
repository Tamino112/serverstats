"""Zero-dependency HTTP + SSE server for ServerStats."""

from __future__ import annotations

import json
import mimetypes
import queue
import signal
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .history import TelemetryStore


STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


class ServerStatsHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(
        self,
        server_address: tuple[str, int],
        store: TelemetryStore,
        static_dir: Path = STATIC_DIR,
    ) -> None:
        self.store = store
        self.static_dir = static_dir.resolve()
        super().__init__(server_address, ServerStatsHandler)


class ServerStatsHandler(BaseHTTPRequestHandler):
    server: ServerStatsHTTPServer
    protocol_version = "HTTP/1.1"

    def log_message(self, format: str, *args: Any) -> None:
        # Keep systemd journal clean; log errors only
        if args and len(args) >= 2 and str(args[1]).startswith(("4", "5")):
            super().log_message(format, *args)

    def _send_json(self, payload: Any, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_static(self, req_path: str) -> None:
        rel = req_path.lstrip("/") or "index.html"
        target = (self.server.static_dir / rel).resolve()
        try:
            target.relative_to(self.server.static_dir)
        except ValueError:
            self.send_error(HTTPStatus.FORBIDDEN)
            return

        if target.is_dir():
            target = target / "index.html"

        if not target.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content = target.read_bytes()
        mime, _ = mimetypes.guess_type(str(target))
        if not mime:
            mime = "application/octet-stream"
        if mime.startswith(("text/", "application/javascript")):
            mime = f"{mime}; charset=utf-8"

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(content)))
        if rel == "index.html":
            self.send_header("Cache-Control", "no-cache")
        else:
            self.send_header("Cache-Control", "public, max-age=300")
        self.end_headers()
        self.wfile.write(content)

    def _handle_sse(self) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        sub = self.server.store.subscribe()
        try:
            # Send initial snapshot immediately
            latest = self.server.store.get_latest()
            payload = f"event: stats\ndata: {json.dumps(latest, separators=(',', ':'), ensure_ascii=False)}\n\n"
            self.wfile.write(payload.encode("utf-8"))
            self.wfile.flush()

            while True:
                try:
                    snap = sub.get(timeout=15.0)
                    msg = f"event: stats\ndata: {json.dumps(snap, separators=(',', ':'), ensure_ascii=False)}\n\n"
                    self.wfile.write(msg.encode("utf-8"))
                    self.wfile.flush()
                except queue.Empty:
                    # Heartbeat comment to keep reverse proxies / browsers alive
                    self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
            pass
        finally:
            self.server.store.unsubscribe(sub)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            self._send_json({"status": "ok"})
            return
        if path == "/api/system":
            force = "refresh=1" in (parsed.query or "")
            self._send_json(self.server.store.get_hardware(force=force))
            return
        if path == "/api/stats":
            self._send_json(self.server.store.get_latest())
            return
        if path == "/api/history":
            self._send_json(
                {
                    "interval": self.server.store.interval,
                    "points": self.server.store.get_history(),
                }
            )
            return
        if path == "/api/stream":
            self._handle_sse()
            return

        self._serve_static(path)


def run_server(host: str = "0.0.0.0", port: int = 8080, interval: float = 2.0) -> None:
    store = TelemetryStore(interval=interval, max_points=300)
    store.start()
    httpd = ServerStatsHTTPServer((host, port), store)

    def _shutdown(signum: int, _frame: Any) -> None:
        store.stop()
        # shutdown must not be called from serve_forever thread directly; exit cleanly
        sys.exit(0)

    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)

    print(f"ServerStats listening on http://{host}:{port} (interval={interval}s)", flush=True)
    try:
        httpd.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        store.stop()
        httpd.server_close()
