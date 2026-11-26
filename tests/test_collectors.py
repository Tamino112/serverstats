"""Unit and integration tests for ServerStats collectors and HTTP API."""

from __future__ import annotations

import json
import threading
import unittest
from urllib.request import urlopen

from backend.collectors import (
    TelemetryCollector,
    collect_hardware_info,
    parse_sensors_json,
    pick_primary_cpu_temp,
)
from backend.history import TelemetryStore
from backend.server import ServerStatsHTTPServer


SAMPLE_SENSORS_JSON = json.dumps(
    {
        "coretemp-isa-0000": {
            "Adapter": "ISA adapter",
            "Package id 0": {
                "temp1_input": 48.0,
                "temp1_max": 80.0,
                "temp1_crit": 100.0,
            },
            "Core 0": {
                "temp2_input": 44.0,
                "temp2_max": 80.0,
                "temp2_crit": 100.0,
            },
            "Core 1": {
                "temp3_input": 46.5,
                "temp3_max": 80.0,
                "temp3_crit": 100.0,
            },
        },
        "nvme-pci-0100": {
            "Adapter": "PCI adapter",
            "Composite": {
                "temp1_input": 37.85,
                "temp1_max": 84.85,
                "temp1_crit": 89.85,
            },
        },
        "nct6775-isa-0290": {
            "Adapter": "ISA adapter",
            "fan1": {"fan1_input": 1120.0, "fan1_min": 300.0},
            "fan2": {"fan2_input": 840.0},
            "SYSTIN": {"temp1_input": 33.0, "temp1_max": 80.0},
            "AUXTIN0": {"temp3_input": 0.0},
        },
        "amdgpu-pci-0300": {
            "Adapter": "PCI adapter",
            "edge": {"temp1_input": 52.0, "temp1_crit": 100.0},
            "PPT": {"power1_average": 24.6},
        },
    }
)


class TestSensorsParsing(unittest.TestCase):
    def test_parse_sensors_json_extracts_temps_fans_power(self) -> None:
        parsed = parse_sensors_json(SAMPLE_SENSORS_JSON)
        temps = parsed["temps"]
        fans = parsed["fans"]
        power = parsed["power"]

        # AUXTIN0 with 0.0 and no thresholds should be filtered out
        labels = [t["label"] for t in temps]
        self.assertIn("Package id 0", labels)
        self.assertIn("Composite", labels)
        self.assertIn("SYSTIN", labels)
        self.assertIn("edge", labels)
        self.assertNotIn("AUXTIN0", labels)

        # Categories
        by_label = {t["label"]: t for t in temps}
        self.assertEqual(by_label["Package id 0"]["category"], "CPU")
        self.assertEqual(by_label["Composite"]["category"], "Speicher")
        self.assertEqual(by_label["SYSTIN"]["category"], "Mainboard")
        self.assertEqual(by_label["edge"]["category"], "GPU")
        self.assertAlmostEqual(by_label["Composite"]["current_c"], 37.9, places=1)

        # Fans & Power
        self.assertEqual(len(fans), 2)
        self.assertEqual(fans[0]["rpm"], 1120)
        self.assertEqual(len(power), 1)
        self.assertAlmostEqual(power[0]["watts"], 24.6, places=1)

        # Primary CPU temp selection
        primary = pick_primary_cpu_temp(temps)
        self.assertIsNotNone(primary)
        self.assertEqual(primary["label"], "Package id 0")


class TestLiveCollectorsAndServer(unittest.TestCase):
    def test_hardware_and_snapshot(self) -> None:
        hw = collect_hardware_info()
        self.assertTrue(hw["hostname"])
        self.assertTrue(hw["cpu"]["model"])
        self.assertGreaterEqual(hw["cpu"]["logical_cores"], 1)
        self.assertGreater(hw["memory"]["total_bytes"], 0)

        collector = TelemetryCollector()
        snap = collector.collect_snapshot()
        self.assertIn("cpu", snap)
        self.assertIn("memory", snap)
        self.assertIn("temperatures", snap)
        self.assertIn("filesystems", snap)
        self.assertIn("network", snap)
        self.assertIn("processes", snap)
        self.assertGreaterEqual(len(snap["cpu"]["cores"]), 1)

    def test_http_endpoints(self) -> None:
        store = TelemetryStore(interval=1.0, max_points=30)
        store.start()
        httpd = ServerStatsHTTPServer(("127.0.0.1", 0), store)
        port = httpd.server_address[1]
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            with urlopen(f"http://127.0.0.1:{port}/api/health", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                self.assertEqual(json.loads(resp.read())["status"], "ok")

            with urlopen(f"http://127.0.0.1:{port}/api/system", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                sys_data = json.loads(resp.read())
                self.assertIn("cpu", sys_data)

            with urlopen(f"http://127.0.0.1:{port}/api/stats", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                stats_data = json.loads(resp.read())
                self.assertIn("memory", stats_data)

            with urlopen(f"http://127.0.0.1:{port}/", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                html = resp.read().decode("utf-8")
                self.assertIn("ServerStats", html)
        finally:
            httpd.shutdown()
            httpd.server_close()
            store.stop()


if __name__ == "__main__":
    unittest.main()
