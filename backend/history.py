"""Background telemetry sampler and ring-buffer history store."""

from __future__ import annotations

import queue
import threading
import time
from collections import deque
from typing import Any

from .collectors import TelemetryCollector


class TelemetryStore:
    """Runs a single background sampling loop and fans out snapshots to SSE subscribers."""

    def __init__(self, interval: float = 2.0, max_points: int = 300) -> None:
        self.interval = max(0.5, interval)
        self.max_points = max_points
        self.collector = TelemetryCollector()
        self._lock = threading.Lock()
        self._latest: dict[str, Any] | None = None
        self._history: deque[dict[str, Any]] = deque(maxlen=max_points)
        self._subscribers: set[queue.Queue[dict[str, Any]]] = set()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        # Collect initial snapshot synchronously so first HTTP request is instant
        self._sample_once()
        self._thread = threading.Thread(target=self._run, name="telemetry-sampler", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=3.0)

    def _run(self) -> None:
        while not self._stop_event.is_set():
            start = time.monotonic()
            try:
                self._sample_once()
            except Exception:
                # Never kill the background sampler on transient /proc read errors
                pass
            elapsed = time.monotonic() - start
            wait = max(0.1, self.interval - elapsed)
            self._stop_event.wait(wait)

    def _sample_once(self) -> None:
        snap = self.collector.collect_snapshot()
        cpu_temp = None
        if snap["temperatures"].get("cpu_primary"):
            cpu_temp = snap["temperatures"]["cpu_primary"]["current_c"]
        elif snap["temperatures"].get("hottest"):
            cpu_temp = snap["temperatures"]["hottest"]["current_c"]

        point = {
            "ts": snap["timestamp"],
            "cpu": snap["cpu"]["usage_pct"],
            "cpu_user": snap["cpu"]["user_pct"],
            "cpu_sys": snap["cpu"]["system_pct"],
            "mem": snap["memory"]["used_pct"],
            "temp": cpu_temp,
            "net_rx": snap["network"]["rx_bps"],
            "net_tx": snap["network"]["tx_bps"],
            "disk_r": snap["disk_io"]["read_bps"],
            "disk_w": snap["disk_io"]["write_bps"],
        }

        with self._lock:
            self._latest = snap
            self._history.append(point)
            subscribers = list(self._subscribers)

        for q in subscribers:
            try:
                q.put_nowait(snap)
            except queue.Full:
                try:
                    q.get_nowait()
                    q.put_nowait(snap)
                except queue.Empty:
                    pass

    def get_hardware(self, force: bool = False) -> dict[str, Any]:
        return self.collector.get_hardware(force=force)

    def get_latest(self) -> dict[str, Any]:
        with self._lock:
            if self._latest is not None:
                return self._latest
        self._sample_once()
        with self._lock:
            return self._latest  # type: ignore[return-value]

    def get_history(self) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._history)

    def subscribe(self) -> queue.Queue[dict[str, Any]]:
        q: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=4)
        with self._lock:
            self._subscribers.add(q)
        return q

    def unsubscribe(self, q: queue.Queue[dict[str, Any]]) -> None:
        with self._lock:
            self._subscribers.discard(q)
