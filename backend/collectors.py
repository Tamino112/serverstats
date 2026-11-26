"""Linux system hardware and live telemetry collectors using stdlib only."""

from __future__ import annotations

import json
import os
import platform
import pwd
import re
import shutil
import socket
import subprocess
import time
from pathlib import Path
from typing import Any


def _read_text(path: str | Path) -> str | None:
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        return None


def _run_cmd(args: list[str], timeout: float = 2.0) -> str | None:
    try:
        res = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env={**os.environ, "LC_ALL": "C"},
        )
        if res.returncode == 0 and res.stdout:
            return res.stdout
    except (OSError, subprocess.SubprocessError):
        pass
    return None


def _safe_float(val: Any) -> float | None:
    try:
        f = float(val)
        if f != f or f in (float("inf"), float("-inf")):
            return None
        return f
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Static Hardware & System Specification Collector
# ---------------------------------------------------------------------------

def _parse_os_release() -> dict[str, str]:
    data: dict[str, str] = {}
    content = _read_text("/etc/os-release")
    if not content:
        return {"name": platform.system(), "version": platform.release(), "id": "linux"}
    for line in content.splitlines():
        if "=" not in line or line.startswith("#"):
            continue
        k, v = line.split("=", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return {
        "name": data.get("PRETTY_NAME") or data.get("NAME") or "Linux",
        "version": data.get("VERSION_ID") or "",
        "id": data.get("ID") or "linux",
    }


def _collect_cpu_hardware() -> dict[str, Any]:
    info: dict[str, Any] = {
        "model": "Unbekannte CPU",
        "vendor": "",
        "architecture": platform.machine() or "unknown",
        "physical_cores": None,
        "logical_cores": os.cpu_count() or 1,
        "sockets": 1,
        "min_mhz": None,
        "max_mhz": None,
        "caches": {},
        "virtualization": None,
        "hypervisor": None,
    }

    # Try lscpu -J first (most structured and reliable across x86/ARM)
    lscpu_json = _run_cmd(["lscpu", "-J"])
    if lscpu_json:
        try:
            parsed = json.loads(lscpu_json)
            entries = parsed.get("lscpu", [])
            kv: dict[str, str] = {}
            for item in entries:
                field = str(item.get("field", "")).rstrip(":").strip().lower()
                val = str(item.get("data", "")).strip()
                if field and val:
                    kv[field] = val
            if "model name" in kv:
                info["model"] = kv["model name"]
            if "vendor id" in kv:
                info["vendor"] = kv["vendor id"]
            if "architecture" in kv:
                info["architecture"] = kv["architecture"]
            if "cpu(s)" in kv and kv["cpu(s)"].isdigit():
                info["logical_cores"] = int(kv["cpu(s)"])
            cores_per_socket = int(kv["core(s) per socket"]) if kv.get("core(s) per socket", "").isdigit() else None
            sockets = int(kv["socket(s)"]) if kv.get("socket(s)", "").isdigit() else 1
            info["sockets"] = sockets
            if cores_per_socket:
                info["physical_cores"] = cores_per_socket * sockets
            if "cpu max mhz" in kv:
                info["max_mhz"] = _safe_float(kv["cpu max mhz"].replace(",", "."))
            if "cpu min mhz" in kv:
                info["min_mhz"] = _safe_float(kv["cpu min mhz"].replace(",", "."))
            if "hypervisor vendor" in kv:
                info["hypervisor"] = kv["hypervisor vendor"]
            if "virtualization" in kv:
                info["virtualization"] = kv["virtualization"]
            elif "virtualization type" in kv:
                info["virtualization"] = kv["virtualization type"]
            for cache_key, label in [
                ("l1d cache", "L1d"),
                ("l1i cache", "L1i"),
                ("l2 cache", "L2"),
                ("l3 cache", "L3"),
            ]:
                if cache_key in kv:
                    info["caches"][label] = re.sub(r"\s*\(\d+\s+instances?\)$", "", kv[cache_key]).strip()
        except (json.JSONDecodeError, ValueError):
            pass

    # Fallback / enrichment from /proc/cpuinfo
    cpuinfo = _read_text("/proc/cpuinfo")
    if cpuinfo:
        model = None
        vendor = None
        core_ids: set[tuple[str, str]] = set()
        phys_id = "0"
        for line in cpuinfo.splitlines():
            if ":" not in line:
                continue
            k, v = (part.strip() for part in line.split(":", 1))
            if k in ("model name", "Model", "Hardware") and not model and v:
                model = v
            elif k == "vendor_id" and not vendor and v:
                vendor = v
            elif k == "physical id":
                phys_id = v
            elif k == "core id":
                core_ids.add((phys_id, v))
        if info["model"] == "Unbekannte CPU" and model:
            info["model"] = model
        if not info["vendor"] and vendor:
            info["vendor"] = vendor
        if info["physical_cores"] is None and core_ids:
            info["physical_cores"] = len(core_ids)

    # Frequency bounds from sysfs if lscpu didn't report them
    if info["max_mhz"] is None:
        max_khz = _read_text("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq")
        if max_khz and max_khz.isdigit():
            info["max_mhz"] = round(int(max_khz) / 1000.0, 1)
    if info["min_mhz"] is None:
        min_khz = _read_text("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq")
        if min_khz and min_khz.isdigit():
            info["min_mhz"] = round(int(min_khz) / 1000.0, 1)

    # Clean whitespace in CPU model name
    info["model"] = re.sub(r"\s+", " ", info["model"]).strip()
    if info["physical_cores"] is None:
        info["physical_cores"] = info["logical_cores"]

    return info


def _collect_board_hardware() -> dict[str, str | None]:
    dmi = Path("/sys/class/dmi/id")

    def clean_dmi(filename: str) -> str | None:
        val = _read_text(dmi / filename)
        if not val:
            return None
        low = val.lower()
        if low in (
            "to be filled by o.e.m.",
            "default string",
            "none",
            "n/a",
            "not specified",
            "system manufacturer",
            "system product name",
        ):
            return None
        return val

    sys_vendor = clean_dmi("sys_vendor")
    product_name = clean_dmi("product_name")
    board_vendor = clean_dmi("board_vendor")
    board_name = clean_dmi("board_name")
    bios_vendor = clean_dmi("bios_vendor")
    bios_version = clean_dmi("bios_version")

    # Raspberry Pi / ARM device-tree fallback
    if not product_name:
        dt_model = _read_text("/proc/device-tree/model")
        if dt_model:
            product_name = dt_model.rstrip("\x00").strip()

    system_str = " ".join(x for x in (sys_vendor, product_name) if x) or None
    board_str = " ".join(x for x in (board_vendor, board_name) if x) or None
    if board_str and system_str and board_str.lower() == system_str.lower():
        board_str = None
    bios_str = " ".join(x for x in (bios_vendor, bios_version) if x) or None

    return {
        "system": system_str,
        "board": board_str,
        "bios": bios_str,
    }


def _collect_gpu_hardware() -> list[dict[str, Any]]:
    gpus: list[dict[str, Any]] = []
    seen_names: set[str] = set()

    # Try nvidia-smi first for rich GPU metadata
    nvsmi = _run_cmd(
        ["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader,nounits"],
        timeout=2.0,
    )
    if nvsmi:
        for line in nvsmi.splitlines():
            parts = [p.strip() for p in line.split(",")]
            if parts and parts[0]:
                name = parts[0]
                seen_names.add(name.lower())
                gpus.append(
                    {
                        "name": name,
                        "driver": parts[1] if len(parts) > 1 else None,
                        "vram_mb": int(float(parts[2])) if len(parts) > 2 and _safe_float(parts[2]) else None,
                        "vendor": "NVIDIA",
                    }
                )

    # lspci for AMD, Intel, and fallback NVIDIA / virtual GPUs
    lspci_out = _run_cmd(["lspci"], timeout=2.0)
    if lspci_out:
        for line in lspci_out.splitlines():
            if any(tag in line for tag in ("VGA compatible controller", "3D controller", "Display controller")):
                # Format: "00:02.0 VGA compatible controller: Intel Corporation ..."
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    raw_name = parts[2].strip()
                    raw_name = re.sub(r"\s*\(rev [0-9a-fA-F]+\)$", "", raw_name).strip()
                    low = raw_name.lower()
                    if any(s in low or low in s for s in seen_names):
                        continue
                    seen_names.add(low)
                    vendor = "Other"
                    if "nvidia" in low:
                        vendor = "NVIDIA"
                    elif "amd" in low or "ati" in low or "radeon" in low:
                        vendor = "AMD"
                    elif "intel" in low:
                        vendor = "Intel"
                    gpus.append({"name": raw_name, "driver": None, "vram_mb": None, "vendor": vendor})

    return gpus


def _collect_block_devices() -> list[dict[str, Any]]:
    devices: list[dict[str, Any]] = []
    lsblk_out = _run_cmd(["lsblk", "-J", "-b", "-d", "-o", "NAME,MODEL,SIZE,ROTA,TRAN,TYPE"], timeout=2.0)
    if lsblk_out:
        try:
            data = json.loads(lsblk_out)
            for dev in data.get("blockdevices", []):
                if dev.get("type") not in ("disk", None):
                    continue
                name = str(dev.get("name") or "")
                if not name or name.startswith(("loop", "ram", "zram", "sr")):
                    continue
                size = int(dev.get("size") or 0)
                if size <= 0:
                    continue
                tran = str(dev.get("tran") or "").upper()
                rota = dev.get("rota")
                is_rotational = rota in (True, 1, "1", "true")
                if name.startswith("nvme") or tran == "NVME":
                    media = "NVMe"
                elif is_rotational:
                    media = "HDD"
                else:
                    media = "SSD"
                model = str(dev.get("model") or "").strip() or f"/dev/{name}"
                devices.append(
                    {
                        "name": name,
                        "model": re.sub(r"\s+", " ", model),
                        "size_bytes": size,
                        "media": media,
                        "transport": tran or media,
                    }
                )
        except (json.JSONDecodeError, ValueError):
            pass
    return devices


def _collect_memory_hardware() -> dict[str, Any]:
    """Best-effort RAM module summary (type/speed) when dmidecode is permitted."""
    meminfo = _parse_meminfo()
    result: dict[str, Any] = {
        "total_bytes": meminfo["total_bytes"],
        "type": None,
        "speed": None,
        "modules": None,
    }
    if os.geteuid() == 0 and shutil.which("dmidecode"):
        out = _run_cmd(["dmidecode", "-t", "memory"], timeout=2.0)
        if out:
            types: set[str] = set()
            speeds: list[int] = []
            installed = 0
            total_slots = 0
            for block in out.split("\n\n"):
                if "Memory Device" not in block:
                    continue
                total_slots += 1
                size_m = re.search(r"^\s*Size:\s*(.+)$", block, re.MULTILINE)
                if not size_m or "no module" in size_m.group(1).lower():
                    continue
                installed += 1
                type_m = re.search(r"^\s*Type:\s*(.+)$", block, re.MULTILINE)
                if type_m:
                    t = type_m.group(1).strip()
                    if t not in ("Unknown", "Other", "RAM"):
                        types.add(t)
                speed_m = re.search(
                    r"^\s*(?:Configured Memory Speed|Speed):\s*(\d+)\s*(?:MT/s|MHz)",
                    block,
                    re.MULTILINE,
                )
                if speed_m:
                    speeds.append(int(speed_m.group(1)))
            if types:
                result["type"] = "/".join(sorted(types))
            if speeds:
                result["speed"] = f"{max(speeds)} MT/s"
            if total_slots > 0:
                result["modules"] = f"{installed}/{total_slots}"
    return result


def _get_primary_ip() -> str | None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        try:
            return socket.gethostbyname(socket.gethostname())
        except OSError:
            return None


def collect_hardware_info() -> dict[str, Any]:
    os_info = _parse_os_release()
    uptime_s = _read_uptime()
    return {
        "hostname": socket.gethostname(),
        "primary_ip": _get_primary_ip(),
        "os": os_info,
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "boot_time": int(time.time() - uptime_s) if uptime_s else None,
        "cpu": _collect_cpu_hardware(),
        "memory": _collect_memory_hardware(),
        "board": _collect_board_hardware(),
        "gpus": _collect_gpu_hardware(),
        "disks": _collect_block_devices(),
        "lm_sensors_installed": shutil.which("sensors") is not None,
    }


# ---------------------------------------------------------------------------
# Temperature, Fan & Power Collectors
# ---------------------------------------------------------------------------

def _categorize_chip(chip_name: str, label: str = "") -> str:
    s = f"{chip_name} {label}".lower()
    if any(k in s for k in ("coretemp", "k10temp", "zenpower", "cpu_thermal", "soc_thermal", "x86_pkg_temp", "package id", "tctl", "tdie", "cpu")):
        return "CPU"
    if any(k in s for k in ("amdgpu", "nouveau", "nvidia", "radeon", "gpu", "i915")):
        return "GPU"
    if any(k in s for k in ("nvme", "drivetemp", "sata", "scsi", "composite", "disk")):
        return "Speicher"
    if any(k in s for k in ("iwlwifi", "r8169", "ixgbe", "igb", "mlx", "wifi", "nic", "phy")):
        return "Netzwerk"
    if any(k in s for k in ("nct", "it87", "f718", "w83627", "asus", "gigabyte", "dell", "thinkpad", "acpitz", "pch", "systin", "cputin", "motherboard", "vrm", "chipset")):
        return "Mainboard"
    return "Sonstige"


def _prettify_chip(chip_name: str) -> str:
    # Strip bus suffixes like "-isa-0000", "-pci-00c3", "-acpi-0"
    cleaned = re.sub(r"-(?:isa|pci|acpi|virtual|i2c|hid|scsi)-[0-9a-fA-F-]+$", "", chip_name)
    mapping = {
        "coretemp": "Intel Core",
        "k10temp": "AMD CPU",
        "zenpower": "AMD Zen",
        "nvme": "NVMe SSD",
        "drivetemp": "Festplatte",
        "acpitz": "ACPI Thermal",
        "amdgpu": "AMD GPU",
        "nouveau": "NVIDIA GPU",
        "iwlwifi_1": "WLAN-Modul",
        "pch_cannonlake": "Intel PCH",
        "pch_cometlake": "Intel PCH",
        "pch_skylake": "Intel PCH",
    }
    return mapping.get(cleaned.lower(), cleaned)


def parse_sensors_json(raw_json: str) -> dict[str, Any]:
    """Parse `sensors -j` output into normalized temperatures, fans, and power readings."""
    temps: list[dict[str, Any]] = []
    fans: list[dict[str, Any]] = []
    power: list[dict[str, Any]] = []

    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        return {"temps": temps, "fans": fans, "power": power}

    if not isinstance(data, dict):
        return {"temps": temps, "fans": fans, "power": power}

    for chip_name, chip_body in data.items():
        if not isinstance(chip_body, dict):
            continue
        adapter = str(chip_body.get("Adapter") or "")
        chip_display = _prettify_chip(chip_name)

        for feat_label, feat_vals in chip_body.items():
            if feat_label == "Adapter" or not isinstance(feat_vals, dict):
                continue

            # Temperature feature
            temp_input = None
            temp_max = None
            temp_crit = None
            fan_input = None
            fan_min = None
            power_input = None

            for k, v in feat_vals.items():
                fv = _safe_float(v)
                if fv is None:
                    continue
                if re.match(r"^temp\d+_input$", k):
                    temp_input = fv
                elif re.match(r"^temp\d+_max$", k):
                    temp_max = fv
                elif re.match(r"^temp\d+_crit$", k):
                    temp_crit = fv
                elif re.match(r"^fan\d+_input$", k):
                    fan_input = fv
                elif re.match(r"^fan\d+_min$", k):
                    fan_min = fv
                elif re.match(r"^power\d+_(?:average|input)$", k):
                    power_input = fv

            if temp_input is not None and -40.0 < temp_input < 140.0:
                # Filter out bogus 0.0 / 127.0 disconnected SuperIO pins without thresholds
                if temp_input == 0.0 and temp_max is None and temp_crit is None:
                    continue
                cat = _categorize_chip(chip_name, feat_label)
                temps.append(
                    {
                        "id": f"{chip_name}:{feat_label}",
                        "label": feat_label,
                        "chip": chip_display,
                        "chip_raw": chip_name,
                        "adapter": adapter,
                        "category": cat,
                        "current_c": round(temp_input, 1),
                        "high_c": round(temp_max, 1) if temp_max and 0 < temp_max < 150 else None,
                        "crit_c": round(temp_crit, 1) if temp_crit and 0 < temp_crit < 150 else None,
                    }
                )

            if fan_input is not None and fan_input >= 0:
                fans.append(
                    {
                        "id": f"{chip_name}:{feat_label}",
                        "label": feat_label,
                        "chip": chip_display,
                        "rpm": int(round(fan_input)),
                        "min_rpm": int(round(fan_min)) if fan_min is not None else None,
                    }
                )

            if power_input is not None and 0.0 <= power_input < 2000.0:
                power.append(
                    {
                        "id": f"{chip_name}:{feat_label}",
                        "label": feat_label,
                        "chip": chip_display,
                        "watts": round(power_input, 1),
                    }
                )

    return {"temps": temps, "fans": fans, "power": power}


def _collect_sysfs_hwmon() -> dict[str, Any]:
    """Direct Linux sysfs /sys/class/hwmon reader (zero dependencies fallback)."""
    temps: list[dict[str, Any]] = []
    fans: list[dict[str, Any]] = []
    power: list[dict[str, Any]] = []

    hwmon_root = Path("/sys/class/hwmon")
    if not hwmon_root.exists():
        return {"temps": temps, "fans": fans, "power": power}

    for hwdir in sorted(hwmon_root.iterdir()):
        chip_raw = _read_text(hwdir / "name") or hwdir.name
        chip_display = _prettify_chip(chip_raw)

        for input_file in sorted(hwdir.glob("temp*_input")):
            prefix = input_file.name[: -len("_input")]
            raw_val = _read_text(input_file)
            if not raw_val:
                continue
            fv = _safe_float(raw_val)
            if fv is None:
                continue
            temp_c = fv / 1000.0 if abs(fv) > 200 else fv
            if not (-40.0 < temp_c < 140.0):
                continue
            label = _read_text(hwdir / f"{prefix}_label") or f"{chip_display} {prefix}"
            max_raw = _read_text(hwdir / f"{prefix}_max")
            crit_raw = _read_text(hwdir / f"{prefix}_crit")
            high_c = (_safe_float(max_raw) or 0) / 1000.0 if max_raw else None
            crit_c = (_safe_float(crit_raw) or 0) / 1000.0 if crit_raw else None
            temps.append(
                {
                    "id": f"{hwdir.name}:{prefix}",
                    "label": label,
                    "chip": chip_display,
                    "chip_raw": chip_raw,
                    "adapter": "sysfs hwmon",
                    "category": _categorize_chip(chip_raw, label),
                    "current_c": round(temp_c, 1),
                    "high_c": round(high_c, 1) if high_c and 0 < high_c < 150 else None,
                    "crit_c": round(crit_c, 1) if crit_c and 0 < crit_c < 150 else None,
                }
            )

        for fan_file in sorted(hwdir.glob("fan*_input")):
            prefix = fan_file.name[: -len("_input")]
            raw_val = _read_text(fan_file)
            fv = _safe_float(raw_val)
            if fv is not None and fv >= 0:
                label = _read_text(hwdir / f"{prefix}_label") or f"Lüfter {prefix[3:]}"
                fans.append(
                    {
                        "id": f"{hwdir.name}:{prefix}",
                        "label": label,
                        "chip": chip_display,
                        "rpm": int(round(fv)),
                        "min_rpm": None,
                    }
                )

    return {"temps": temps, "fans": fans, "power": power}


def _collect_thermal_zones() -> list[dict[str, Any]]:
    temps: list[dict[str, Any]] = []
    thermal_root = Path("/sys/class/thermal")
    if not thermal_root.exists():
        return temps

    for zdir in sorted(thermal_root.glob("thermal_zone*")):
        temp_raw = _read_text(zdir / "temp")
        if not temp_raw:
            continue
        fv = _safe_float(temp_raw)
        if fv is None:
            continue
        temp_c = fv / 1000.0 if abs(fv) > 200 else fv
        if not (-40.0 < temp_c < 140.0):
            continue
        ztype = _read_text(zdir / "type") or zdir.name
        crit_c = None
        for trip_type in sorted(zdir.glob("trip_point_*_type")):
            tt = (_read_text(trip_type) or "").lower()
            if tt in ("critical", "hot"):
                idx = trip_type.name.replace("_type", "_temp")
                traw = _safe_float(_read_text(zdir / idx))
                if traw and traw > 0:
                    crit_c = round(traw / 1000.0 if traw > 200 else traw, 1)
                    break
        temps.append(
            {
                "id": f"thermal:{zdir.name}",
                "label": ztype,
                "chip": "Thermal Zone",
                "chip_raw": ztype,
                "adapter": "sysfs thermal",
                "category": _categorize_chip(ztype, ztype),
                "current_c": round(temp_c, 1),
                "high_c": None,
                "crit_c": crit_c,
            }
        )
    return temps


def _collect_nvidia_live() -> list[dict[str, Any]]:
    out = _run_cmd(
        [
            "nvidia-smi",
            "--query-gpu=index,name,temperature.gpu,fan.speed,power.draw,utilization.gpu,memory.used,memory.total",
            "--format=csv,noheader,nounits",
        ],
        timeout=1.5,
    )
    if not out:
        return []
    gpus: list[dict[str, Any]] = []
    for line in out.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 8:
            continue
        gpus.append(
            {
                "index": parts[0],
                "name": parts[1],
                "temp_c": _safe_float(parts[2]),
                "fan_pct": _safe_float(parts[3]),
                "power_w": _safe_float(parts[4]),
                "util_pct": _safe_float(parts[5]),
                "vram_used_mb": _safe_float(parts[6]),
                "vram_total_mb": _safe_float(parts[7]),
            }
        )
    return gpus


def pick_primary_cpu_temp(temps: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Pick the most representative CPU package/die temperature from sensor list."""
    cpu_temps = [t for t in temps if t.get("category") == "CPU"]
    if not cpu_temps:
        return None
    priority_patterns = [
        r"package id 0",
        r"package",
        r"tdie",
        r"tctl",
        r"x86_pkg_temp",
        r"cpu_thermal",
        r"cputin",
        r"core 0",
    ]
    for pat in priority_patterns:
        for t in cpu_temps:
            if re.search(pat, t["label"], re.IGNORECASE):
                return t
    # Otherwise pick highest CPU reading
    return max(cpu_temps, key=lambda x: x["current_c"])


def collect_temperatures() -> dict[str, Any]:
    temps: list[dict[str, Any]] = []
    fans: list[dict[str, Any]] = []
    power: list[dict[str, Any]] = []
    sources: list[str] = []

    lm_installed = shutil.which("sensors") is not None

    # 1. lm-sensors JSON
    if lm_installed:
        raw = _run_cmd(["sensors", "-j"], timeout=2.0)
        if raw:
            parsed = parse_sensors_json(raw)
            if parsed["temps"] or parsed["fans"] or parsed["power"]:
                temps.extend(parsed["temps"])
                fans.extend(parsed["fans"])
                power.extend(parsed["power"])
                sources.append("lm-sensors")

    # 2. Fallback to sysfs hwmon if lm-sensors returned no temps
    if not temps:
        hw = _collect_sysfs_hwmon()
        if hw["temps"] or hw["fans"]:
            temps.extend(hw["temps"])
            if not fans:
                fans.extend(hw["fans"])
            sources.append("sysfs-hwmon")

    # 3. Fallback to /sys/class/thermal if still empty
    if not temps:
        tz = _collect_thermal_zones()
        if tz:
            temps.extend(tz)
            sources.append("sysfs-thermal")

    # 4. NVIDIA GPU live telemetry
    gpu_live = _collect_nvidia_live()
    if gpu_live:
        sources.append("nvidia-smi")
        for g in gpu_live:
            if g["temp_c"] is not None:
                temps.append(
                    {
                        "id": f"nvidia:gpu{g['index']}",
                        "label": g["name"],
                        "chip": "NVIDIA GPU",
                        "chip_raw": "nvidia",
                        "adapter": "nvidia-smi",
                        "category": "GPU",
                        "current_c": round(g["temp_c"], 1),
                        "high_c": 83.0,
                        "crit_c": 95.0,
                    }
                )
            if g["power_w"] is not None:
                power.append(
                    {
                        "id": f"nvidia:power{g['index']}",
                        "label": f"{g['name']} Power",
                        "chip": "NVIDIA GPU",
                        "watts": round(g["power_w"], 1),
                    }
                )

    cpu_primary = pick_primary_cpu_temp(temps)
    hottest = max(temps, key=lambda x: x["current_c"]) if temps else None

    return {
        "available": len(temps) > 0,
        "lm_sensors_installed": lm_installed,
        "sources": sources,
        "cpu_primary": cpu_primary,
        "hottest": hottest,
        "sensors": temps,
        "fans": fans,
        "power": power,
        "gpu_live": gpu_live,
    }


# ---------------------------------------------------------------------------
# Live Telemetry Collectors (CPU, Memory, Disk, Network, Processes)
# ---------------------------------------------------------------------------

def _read_uptime() -> float:
    txt = _read_text("/proc/uptime")
    if txt:
        parts = txt.split()
        val = _safe_float(parts[0])
        if val is not None:
            return val
    return 0.0


def _parse_meminfo() -> dict[str, Any]:
    vals: dict[str, int] = {}
    txt = _read_text("/proc/meminfo") or ""
    for line in txt.splitlines():
        if ":" not in line:
            continue
        k, rest = line.split(":", 1)
        num_str = rest.strip().split()[0]
        if num_str.isdigit():
            vals[k.strip()] = int(num_str) * 1024  # kB -> bytes

    total = vals.get("MemTotal", 0)
    free = vals.get("MemFree", 0)
    buffers = vals.get("Buffers", 0)
    cached = vals.get("Cached", 0) + vals.get("SReclaimable", 0)
    available = vals.get("MemAvailable", free + buffers + cached)
    used = max(0, total - available)
    used_pct = round((used / total) * 100.0, 1) if total > 0 else 0.0

    swap_total = vals.get("SwapTotal", 0)
    swap_free = vals.get("SwapFree", 0)
    swap_used = max(0, swap_total - swap_free)
    swap_pct = round((swap_used / swap_total) * 100.0, 1) if swap_total > 0 else 0.0

    return {
        "total_bytes": total,
        "used_bytes": used,
        "available_bytes": available,
        "free_bytes": free,
        "buffers_bytes": buffers,
        "cached_bytes": cached,
        "used_pct": used_pct,
        "swap_total_bytes": swap_total,
        "swap_used_bytes": swap_used,
        "swap_free_bytes": swap_free,
        "swap_pct": swap_pct,
    }


def _read_proc_stat() -> dict[str, tuple[int, ...]]:
    stats: dict[str, tuple[int, ...]] = {}
    txt = _read_text("/proc/stat") or ""
    for line in txt.splitlines():
        if not line.startswith("cpu"):
            continue
        parts = line.split()
        key = parts[0]
        nums = tuple(int(x) for x in parts[1:11] if x.isdigit())
        if len(nums) >= 4:
            stats[key] = nums
    return stats


def _read_cpu_freqs() -> dict[int, float]:
    freqs: dict[int, float] = {}
    cpu_root = Path("/sys/devices/system/cpu")
    for cdir in cpu_root.glob("cpu[0-9]*"):
        cid_str = cdir.name[3:]
        if not cid_str.isdigit():
            continue
        cur = _read_text(cdir / "cpufreq/scaling_cur_freq")
        if cur and cur.isdigit():
            freqs[int(cid_str)] = round(int(cur) / 1000.0, 1)

    if not freqs:
        txt = _read_text("/proc/cpuinfo") or ""
        idx = 0
        for line in txt.splitlines():
            if line.lower().startswith("cpu mhz"):
                val = _safe_float(line.split(":", 1)[1].strip())
                if val is not None:
                    freqs[idx] = round(val, 1)
                idx += 1
    return freqs


def _read_loadavg() -> dict[str, Any]:
    txt = _read_text("/proc/loadavg") or "0 0 0 0/0 0"
    parts = txt.split()
    running, total = 0, 0
    if len(parts) >= 4 and "/" in parts[3]:
        r_s, t_s = parts[3].split("/", 1)
        running = int(r_s) if r_s.isdigit() else 0
        total = int(t_s) if t_s.isdigit() else 0
    return {
        "load1": round(_safe_float(parts[0]) or 0.0, 2),
        "load5": round(_safe_float(parts[1]) or 0.0, 2),
        "load15": round(_safe_float(parts[2]) or 0.0, 2),
        "tasks_running": running,
        "tasks_total": total,
    }


def _read_filesystems() -> list[dict[str, Any]]:
    ignore_fs = {
        "proc", "sysfs", "devtmpfs", "devpts", "tmpfs", "cgroup", "cgroup2",
        "pstore", "securityfs", "debugfs", "tracefs", "configfs", "fusectl",
        "mqueue", "hugetlbfs", "autofs", "squashfs", "nsfs", "ramfs",
        "rpc_pipefs", "binfmt_misc", "efivarfs", "bpf", "fuse.lxcfs",
        "fuse.portal", "fuse.gvfsd-fuse", "erofs",
    }
    mounts_txt = _read_text("/proc/mounts") or ""
    seen_devs: set[str] = set()
    seen_mounts: set[str] = set()
    filesystems: list[dict[str, Any]] = []

    for line in mounts_txt.splitlines():
        parts = line.split()
        if len(parts) < 3:
            continue
        dev, mount, fstype = parts[0], parts[1], parts[2]
        # Unescape octal spaces in mount path
        mount = mount.replace("\\040", " ")
        if fstype in ignore_fs:
            continue
        if dev.startswith("/dev/loop"):
            continue
        if fstype == "overlay" and mount != "/":
            continue
        if mount.startswith(("/proc", "/sys", "/dev", "/run/user", "/snap")):
            continue
        if dev.startswith("/dev/") and dev in seen_devs:
            continue
        if mount in seen_mounts:
            continue
        try:
            st = os.statvfs(mount)
        except OSError:
            continue
        total = st.f_blocks * st.f_frsize
        if total <= 0:
            continue
        avail = st.f_bavail * st.f_frsize
        free = st.f_bfree * st.f_frsize
        used = max(0, total - free)
        # Percentage matches `df` semantics: used / (used + avail)
        denom = used + avail
        used_pct = round((used / denom) * 100.0, 1) if denom > 0 else 0.0
        seen_devs.add(dev)
        seen_mounts.add(mount)
        filesystems.append(
            {
                "device": dev,
                "mount": mount,
                "fstype": fstype,
                "total_bytes": total,
                "used_bytes": used,
                "available_bytes": avail,
                "used_pct": used_pct,
            }
        )

    filesystems.sort(key=lambda x: (x["mount"] != "/", x["mount"]))
    return filesystems


def _read_diskstats() -> dict[str, tuple[int, int]]:
    """Return {dev_name: (read_bytes, write_bytes)} for whole block devices."""
    stats: dict[str, tuple[int, int]] = {}
    txt = _read_text("/proc/diskstats") or ""
    whole_dev_re = re.compile(r"^(?:sd[a-z]+|hd[a-z]+|vd[a-z]+|xvd[a-z]+|nvme\d+n\d+|mmcblk\d+)$")
    for line in txt.splitlines():
        parts = line.split()
        if len(parts) < 10:
            continue
        name = parts[2]
        if not whole_dev_re.match(name):
            continue
        sectors_read = int(parts[5])
        sectors_written = int(parts[9])
        stats[name] = (sectors_read * 512, sectors_written * 512)
    return stats


def _read_net_dev() -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    txt = _read_text("/proc/net/dev") or ""
    for line in txt.splitlines()[2:]:
        if ":" not in line:
            continue
        iface, rest = line.split(":", 1)
        iface = iface.strip()
        if iface == "lo":
            continue
        cols = rest.split()
        if len(cols) < 10:
            continue
        out[iface] = {
            "rx_bytes": int(cols[0]),
            "rx_packets": int(cols[1]),
            "tx_bytes": int(cols[8]),
            "tx_packets": int(cols[9]),
        }
    return out


def _read_ip_addresses() -> dict[str, dict[str, Any]]:
    """Read IPv4/IPv6 addresses per interface via `ip -j addr`."""
    meta: dict[str, dict[str, Any]] = {}
    out = _run_cmd(["ip", "-j", "addr"], timeout=1.5)
    if out:
        try:
            for item in json.loads(out):
                ifname = item.get("ifname")
                if not ifname or ifname == "lo":
                    continue
                ipv4: list[str] = []
                ipv6: list[str] = []
                for addr in item.get("addr_info", []):
                    fam = addr.get("family")
                    local = addr.get("local")
                    if fam == "inet" and local:
                        ipv4.append(local)
                    elif fam == "inet6" and local and not local.startswith("fe80"):
                        ipv6.append(local)
                meta[ifname] = {
                    "ipv4": ipv4,
                    "ipv6": ipv6,
                    "mac": item.get("address"),
                    "operstate": str(item.get("operstate") or "UNKNOWN").upper(),
                }
        except (json.JSONDecodeError, ValueError):
            pass
    return meta


def _uid_to_username(uid: int, cache: dict[int, str]) -> str:
    if uid in cache:
        return cache[uid]
    try:
        name = pwd.getpwuid(uid).pw_name
    except KeyError:
        name = str(uid)
    cache[uid] = name
    return name


class TelemetryCollector:
    """Stateful collector computing accurate delta rates for CPU, Disk I/O, Network, and Processes."""

    def __init__(self) -> None:
        self._prev_cpu: dict[str, tuple[int, ...]] = {}
        self._prev_disk: dict[str, tuple[int, int]] = {}
        self._prev_disk_ts: float = 0.0
        self._prev_net: dict[str, dict[str, int]] = {}
        self._prev_net_ts: float = 0.0
        self._prev_proc_ticks: dict[int, int] = {}
        self._prev_proc_total_ticks: int = 0
        self._uid_cache: dict[int, str] = {}
        self._page_size: int = os.sysconf("SC_PAGE_SIZE")
        self._clock_ticks: int = os.sysconf("SC_CLK_TCK")
        self._num_cpus: int = os.cpu_count() or 1
        self._hardware_cache: dict[str, Any] | None = None
        self._hardware_ts: float = 0.0

        # Prime baseline snapshots so the first real sample has deltas ready quickly
        self._prev_cpu = _read_proc_stat()
        self._prev_disk = _read_diskstats()
        self._prev_disk_ts = time.monotonic()
        self._prev_net = _read_net_dev()
        self._prev_net_ts = time.monotonic()

    def get_hardware(self, force: bool = False) -> dict[str, Any]:
        now = time.monotonic()
        if force or self._hardware_cache is None or (now - self._hardware_ts) > 300.0:
            self._hardware_cache = collect_hardware_info()
            self._hardware_ts = now
        return self._hardware_cache

    def _compute_cpu(self) -> dict[str, Any]:
        curr = _read_proc_stat()
        prev = self._prev_cpu
        self._prev_cpu = curr
        freqs = _read_cpu_freqs()

        def calc_delta(key: str) -> dict[str, float]:
            c = curr.get(key)
            p = prev.get(key)
            if not c or not p:
                return {"total": 0.0, "user": 0.0, "system": 0.0, "iowait": 0.0}
            deltas = [max(0, c[i] - p[i]) for i in range(min(len(c), len(p)))]
            tot = sum(deltas)
            if tot <= 0:
                return {"total": 0.0, "user": 0.0, "system": 0.0, "iowait": 0.0}
            user = deltas[0] + (deltas[1] if len(deltas) > 1 else 0)
            system = deltas[2] + (deltas[5] if len(deltas) > 5 else 0) + (deltas[6] if len(deltas) > 6 else 0)
            idle = deltas[3]
            iowait = deltas[4] if len(deltas) > 4 else 0
            busy = max(0, tot - idle - iowait)
            return {
                "total": round((busy / tot) * 100.0, 1),
                "user": round((user / tot) * 100.0, 1),
                "system": round((system / tot) * 100.0, 1),
                "iowait": round((iowait / tot) * 100.0, 1),
            }

        overall = calc_delta("cpu")
        cores: list[dict[str, Any]] = []
        core_keys = sorted(
            (k for k in curr if k != "cpu" and k[3:].isdigit()),
            key=lambda x: int(x[3:]),
        )
        for k in core_keys:
            cid = int(k[3:])
            d = calc_delta(k)
            cores.append(
                {
                    "id": cid,
                    "usage_pct": d["total"],
                    "freq_mhz": freqs.get(cid),
                }
            )

        avg_freq = round(sum(freqs.values()) / len(freqs), 1) if freqs else None
        load = _read_loadavg()

        return {
            "usage_pct": overall["total"],
            "user_pct": overall["user"],
            "system_pct": overall["system"],
            "iowait_pct": overall["iowait"],
            "freq_mhz": avg_freq,
            "cores": cores,
            "load": load,
        }

    def _compute_disk_io(self) -> dict[str, Any]:
        now = time.monotonic()
        curr = _read_diskstats()
        dt = max(0.05, now - self._prev_disk_ts) if self._prev_disk_ts else 1.0
        total_read_bps = 0.0
        total_write_bps = 0.0
        devices: list[dict[str, Any]] = []

        for name, (r_bytes, w_bytes) in sorted(curr.items()):
            prev_r, prev_w = self._prev_disk.get(name, (r_bytes, w_bytes))
            r_bps = max(0.0, (r_bytes - prev_r) / dt)
            w_bps = max(0.0, (w_bytes - prev_w) / dt)
            total_read_bps += r_bps
            total_write_bps += w_bps
            devices.append(
                {
                    "name": name,
                    "read_bps": round(r_bps, 1),
                    "write_bps": round(w_bps, 1),
                }
            )

        self._prev_disk = curr
        self._prev_disk_ts = now
        return {
            "read_bps": round(total_read_bps, 1),
            "write_bps": round(total_write_bps, 1),
            "devices": devices,
        }

    def _compute_network(self) -> dict[str, Any]:
        now = time.monotonic()
        curr = _read_net_dev()
        dt = max(0.05, now - self._prev_net_ts) if self._prev_net_ts else 1.0
        ip_meta = _read_ip_addresses()

        interfaces: list[dict[str, Any]] = []
        total_rx_bps = 0.0
        total_tx_bps = 0.0

        virtual_prefixes = ("veth", "docker", "br-", "virbr", "cni", "flannel", "cali", "kube", "sit", "gre", "ip6tnl", "tunl", "teql")

        for name, vals in sorted(curr.items()):
            prev = self._prev_net.get(name, vals)
            rx_bps = max(0.0, (vals["rx_bytes"] - prev["rx_bytes"]) / dt)
            tx_bps = max(0.0, (vals["tx_bytes"] - prev["tx_bytes"]) / dt)

            sys_net = Path("/sys/class/net") / name
            operstate = (_read_text(sys_net / "operstate") or ip_meta.get(name, {}).get("operstate") or "UNKNOWN").upper()
            speed_raw = _read_text(sys_net / "speed")
            speed_mbps = int(speed_raw) if speed_raw and speed_raw.isdigit() and int(speed_raw) > 0 else None
            mac = _read_text(sys_net / "address") or ip_meta.get(name, {}).get("mac")
            is_virtual = name.startswith(virtual_prefixes)

            if not is_virtual:
                total_rx_bps += rx_bps
                total_tx_bps += tx_bps

            interfaces.append(
                {
                    "name": name,
                    "operstate": operstate,
                    "is_virtual": is_virtual,
                    "ipv4": ip_meta.get(name, {}).get("ipv4", []),
                    "ipv6": ip_meta.get(name, {}).get("ipv6", []),
                    "mac": mac,
                    "speed_mbps": speed_mbps,
                    "rx_bps": round(rx_bps, 1),
                    "tx_bps": round(tx_bps, 1),
                    "rx_total_bytes": vals["rx_bytes"],
                    "tx_total_bytes": vals["tx_bytes"],
                }
            )

        # If all interfaces were virtual (e.g. inside certain containers), sum all
        if total_rx_bps == 0.0 and total_tx_bps == 0.0 and interfaces:
            total_rx_bps = sum(i["rx_bps"] for i in interfaces)
            total_tx_bps = sum(i["tx_bps"] for i in interfaces)

        # Sort physical UP interfaces first
        interfaces.sort(key=lambda x: (x["is_virtual"], x["operstate"] != "UP", x["name"]))

        self._prev_net = curr
        self._prev_net_ts = now
        return {
            "rx_bps": round(total_rx_bps, 1),
            "tx_bps": round(total_tx_bps, 1),
            "interfaces": interfaces,
        }

    def _compute_processes(self, total_mem_bytes: int) -> list[dict[str, Any]]:
        cpu_stat = _read_proc_stat().get("cpu")
        curr_total_ticks = sum(cpu_stat) if cpu_stat else 0
        delta_total = curr_total_ticks - self._prev_proc_total_ticks
        if delta_total <= 0:
            delta_total = 1

        new_proc_ticks: dict[int, int] = {}
        procs: list[dict[str, Any]] = []

        try:
            entries = os.listdir("/proc")
        except OSError:
            return []

        for entry in entries:
            if not entry.isdigit():
                continue
            pid = int(entry)
            stat_txt = _read_text(f"/proc/{pid}/stat")
            if not stat_txt:
                continue
            # comm may contain spaces and parentheses; locate last ')'
            lparen = stat_txt.find("(")
            rparen = stat_txt.rfind(")")
            if lparen == -1 or rparen == -1 or rparen <= lparen:
                continue
            comm = stat_txt[lparen + 1 : rparen]
            rest = stat_txt[rparen + 2 :].split()
            if len(rest) < 22:
                continue
            state = rest[0]
            utime = int(rest[11])
            stime = int(rest[12])
            rss_pages = int(rest[21])
            rss_bytes = max(0, rss_pages * self._page_size)
            proc_ticks = utime + stime
            new_proc_ticks[pid] = proc_ticks

            if self._prev_proc_total_ticks > 0 and pid in self._prev_proc_ticks:
                delta_proc = max(0, proc_ticks - self._prev_proc_ticks[pid])
                cpu_pct = round((delta_proc / delta_total) * 100.0 * self._num_cpus, 1)
                cpu_pct = min(cpu_pct, 100.0 * self._num_cpus)
            else:
                cpu_pct = 0.0

            mem_pct = round((rss_bytes / total_mem_bytes) * 100.0, 1) if total_mem_bytes > 0 else 0.0

            try:
                uid = os.stat(f"/proc/{pid}").st_uid
                user = _uid_to_username(uid, self._uid_cache)
            except OSError:
                user = "?"

            procs.append(
                {
                    "pid": pid,
                    "name": comm,
                    "user": user,
                    "state": state,
                    "cpu_pct": cpu_pct,
                    "mem_pct": mem_pct,
                    "mem_bytes": rss_bytes,
                }
            )

        self._prev_proc_ticks = new_proc_ticks
        self._prev_proc_total_ticks = curr_total_ticks

        # Keep top processes by CPU + top by RAM (deduplicated)
        top_cpu = sorted(procs, key=lambda p: (p["cpu_pct"], p["mem_bytes"]), reverse=True)[:18]
        top_mem = sorted(procs, key=lambda p: (p["mem_bytes"], p["cpu_pct"]), reverse=True)[:18]
        merged: dict[int, dict[str, Any]] = {}
        for p in top_cpu + top_mem:
            merged[p["pid"]] = p
        result = sorted(merged.values(), key=lambda p: (p["cpu_pct"], p["mem_bytes"]), reverse=True)[:30]
        return result

    def collect_snapshot(self) -> dict[str, Any]:
        ts = time.time()
        cpu = self._compute_cpu()
        memory = _parse_meminfo()
        temperatures = collect_temperatures()
        filesystems = _read_filesystems()
        disk_io = self._compute_disk_io()
        network = self._compute_network()
        processes = self._compute_processes(memory["total_bytes"])
        uptime_s = _read_uptime()

        return {
            "timestamp": ts,
            "uptime_seconds": int(uptime_s),
            "cpu": cpu,
            "memory": memory,
            "temperatures": temperatures,
            "filesystems": filesystems,
            "disk_io": disk_io,
            "network": network,
            "processes": processes,
        }
