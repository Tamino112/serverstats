#!/usr/bin/env python3
"""Entrypoint for ServerStats Linux monitoring web interface."""

from __future__ import annotations

import argparse
import os

from backend.server import run_server


def main() -> None:
    parser = argparse.ArgumentParser(description="ServerStats — Linux Server Telemetry Web UI")
    parser.add_argument(
        "--host",
        default=os.environ.get("SERVERSTATS_HOST", "0.0.0.0"),
        help="Bind address (default: 0.0.0.0 or $SERVERSTATS_HOST)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("SERVERSTATS_PORT", "8080")),
        help="TCP port (default: 8080 or $SERVERSTATS_PORT)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=float(os.environ.get("SERVERSTATS_INTERVAL", "2.0")),
        help="Sampling interval in seconds (default: 2.0 or $SERVERSTATS_INTERVAL)",
    )
    args = parser.parse_args()
    run_server(host=args.host, port=args.port, interval=args.interval)


if __name__ == "__main__":
    main()
