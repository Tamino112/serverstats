#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# ServerStats — Automatischer Linux-Installer
# Installiert Abhängigkeiten (inkl. lm-sensors für Temperaturen), erkennt
# Hardware-Sensoren automatisch und richtet systemd-Autostart ein.
# =============================================================================

INSTALL_DIR="/opt/serverstats"
SERVICE_NAME="serverstats"
ENV_FILE="/etc/serverstats.env"
HOST="0.0.0.0"
PORT="8080"
INTERVAL="2.0"
UNINSTALL=0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

info()  { printf '\033[1;34m[INFO]\033[0m  %s\n' "$*"; }
ok()    { printf '\033[1;32m[OK]\033[0m    %s\n' "$*"; }
warn()  { printf '\033[1;33m[WARN]\033[0m  %s\n' "$*"; }
err()   { printf '\033[1;31m[ERR]\033[0m   %s\n' "$*" >&2; }

usage() {
  cat <<EOF
Verwendung: sudo ./install.sh [OPTIONEN]

Optionen:
  --port PORT          HTTP-Port (Standard: 8080)
  --host HOST          Bind-Adresse (Standard: 0.0.0.0)
  --interval SEKUNDEN  Aktualisierungsintervall in Sekunden (Standard: 2.0)
  --install-dir PFAD   Installationsverzeichnis (Standard: /opt/serverstats)
  --uninstall          Entfernt ServerStats und den Autostart-Dienst vollständig
  -h, --help           Diese Hilfe anzeigen
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --port)        PORT="$2"; shift 2 ;;
    --host)        HOST="$2"; shift 2 ;;
    --interval)    INTERVAL="$2"; shift 2 ;;
    --install-dir) INSTALL_DIR="$2"; shift 2 ;;
    --uninstall)   UNINSTALL=1; shift ;;
    -h|--help)     usage; exit 0 ;;
    *)             err "Unbekannte Option: $1"; usage; exit 1 ;;
  esac
done

if [[ "${EUID}" -ne 0 ]]; then
  err "Bitte als root oder mit sudo ausführen: sudo $0 $*"
  exit 1
fi

# -----------------------------------------------------------------------------
# Deinstallation
# -----------------------------------------------------------------------------
if [[ "${UNINSTALL}" -eq 1 ]]; then
  info "Deinstalliere ${SERVICE_NAME}..."
  if command -v systemctl >/dev/null 2>&1; then
    systemctl disable --now "${SERVICE_NAME}.service" 2>/dev/null || true
    rm -f "/etc/systemd/system/${SERVICE_NAME}.service"
    systemctl daemon-reload
  elif command -v rc-service >/dev/null 2>&1; then
    rc-service "${SERVICE_NAME}" stop 2>/dev/null || true
    rc-update del "${SERVICE_NAME}" default 2>/dev/null || true
    rm -f "/etc/init.d/${SERVICE_NAME}"
  fi
  rm -rf "${INSTALL_DIR}"
  rm -f "${ENV_FILE}"
  rm -f "/etc/modules-load.d/serverstats-sensors.conf"
  ok "ServerStats wurde vollständig entfernt."
  exit 0
fi

# -----------------------------------------------------------------------------
# 1. Paketmanager erkennen & Abhängigkeiten installieren (inkl. lm-sensors)
# -----------------------------------------------------------------------------
install_packages() {
  info "Installiere benötigte Systempakete (python3, lm-sensors, pciutils)..."

  if command -v apt-get >/dev/null 2>&1; then
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -y -qq python3 lm-sensors pciutils >/dev/null
    apt-get install -y -qq dmidecode >/dev/null 2>&1 || true
  elif command -v dnf >/dev/null 2>&1; then
    dnf install -y -q python3 lm_sensors pciutils >/dev/null
    dnf install -y -q dmidecode >/dev/null 2>&1 || true
  elif command -v yum >/dev/null 2>&1; then
    yum install -y -q python3 lm_sensors pciutils >/dev/null
    yum install -y -q dmidecode >/dev/null 2>&1 || true
  elif command -v pacman >/dev/null 2>&1; then
    pacman -Sy --noconfirm --needed python lm_sensors pciutils >/dev/null
    pacman -S --noconfirm --needed dmidecode >/dev/null 2>&1 || true
  elif command -v zypper >/dev/null 2>&1; then
    zypper --non-interactive install -y python3 sensors pciutils >/dev/null
    zypper --non-interactive install -y dmidecode >/dev/null 2>&1 || true
  elif command -v apk >/dev/null 2>&1; then
    apk add --no-cache python3 lm-sensors pciutils >/dev/null
    apk add --no-cache dmidecode >/dev/null 2>&1 || true
  else
    warn "Kein unterstützter Paketmanager gefunden. Bitte stelle sicher, dass python3 und lm-sensors installiert sind."
  fi

  if ! command -v python3 >/dev/null 2>&1; then
    err "python3 konnte nicht gefunden oder installiert werden."
    exit 1
  fi
  ok "Abhängigkeiten sind installiert."
}

# -----------------------------------------------------------------------------
# 2. Temperatursensoren automatisch erkennen & Kernel-Module laden
# -----------------------------------------------------------------------------
setup_sensors() {
  info "Konfiguriere Temperatursensoren (lm-sensors)..."

  if command -v sensors-detect >/dev/null 2>&1; then
    # Nicht-interaktive automatische Sensor-Erkennung (mit Timeout als Schutz)
    if command -v timeout >/dev/null 2>&1; then
      yes "" 2>/dev/null | timeout 30 sensors-detect --auto >/dev/null 2>&1 || true
    else
      yes "" 2>/dev/null | sensors-detect --auto >/dev/null 2>&1 || true
    fi
  else
    warn "sensors-detect nicht verfügbar — überspringe automatische Hardware-Erkennung."
  fi

  # Gängige Kernel-Module für CPU- und Festplattentemperaturen laden (best-effort)
  local modules_to_try=("coretemp" "k10temp" "drivetemp")
  local loaded_modules=()
  if command -v modprobe >/dev/null 2>&1; then
    for mod in "${modules_to_try[@]}"; do
      if modprobe "${mod}" 2>/dev/null; then
        loaded_modules+=("${mod}")
      fi
    done
  fi

  # Erfolgreich geladene Module für den Neustart persistent hinterlegen
  if [[ ${#loaded_modules[@]} -gt 0 && -d /etc/modules-load.d ]]; then
    printf '%s\n' "${loaded_modules[@]}" > /etc/modules-load.d/serverstats-sensors.conf
  fi

  # lm-sensors / kmod Dienst aktivieren, falls vorhanden
  if command -v systemctl >/dev/null 2>&1; then
    systemctl enable --now lm-sensors.service 2>/dev/null || true
    systemctl enable --now lm_sensors.service 2>/dev/null || true
  fi

  if command -v sensors >/dev/null 2>&1; then
    if sensors >/dev/null 2>&1; then
      ok "Temperatursensoren aktiv."
    else
      warn "lm-sensors installiert, aber aktuell keine physischen Sensoren erkannt (normal in VMs/Containern)."
    fi
  fi
}

# -----------------------------------------------------------------------------
# 3. Anwendungsdateien nach /opt/serverstats installieren
# -----------------------------------------------------------------------------
install_files() {
  info "Installiere ServerStats nach ${INSTALL_DIR}..."
  mkdir -p "${INSTALL_DIR}"
  rm -rf "${INSTALL_DIR}/backend" "${INSTALL_DIR}/static"
  cp -r "${SCRIPT_DIR}/backend" "${INSTALL_DIR}/backend"
  cp -r "${SCRIPT_DIR}/static" "${INSTALL_DIR}/static"
  cp "${SCRIPT_DIR}/run.py" "${INSTALL_DIR}/run.py"
  chmod +x "${INSTALL_DIR}/run.py"

  cat > "${ENV_FILE}" <<EOF
SERVERSTATS_HOST=${HOST}
SERVERSTATS_PORT=${PORT}
SERVERSTATS_INTERVAL=${INTERVAL}
EOF
  chmod 644 "${ENV_FILE}"
  ok "Dateien nach ${INSTALL_DIR} kopiert."
}

# -----------------------------------------------------------------------------
# 4. Autostart-Dienst (systemd oder OpenRC) einrichten
# -----------------------------------------------------------------------------
setup_autostart() {
  local python_bin
  python_bin="$(command -v python3)"

  if command -v systemctl >/dev/null 2>&1 && [[ -d /run/systemd/system ]]; then
    info "Richte systemd-Autostart (${SERVICE_NAME}.service) ein..."

    cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<EOF
[Unit]
Description=ServerStats — Linux Server Telemetry Web UI
After=network-online.target lm-sensors.service lm_sensors.service
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=${INSTALL_DIR}
EnvironmentFile=-${ENV_FILE}
ExecStart=${python_bin} ${INSTALL_DIR}/run.py
Restart=always
RestartSec=3
NoNewPrivileges=true
ProtectHome=true

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable --now "${SERVICE_NAME}.service"
    systemctl restart "${SERVICE_NAME}.service"
    ok "systemd-Dienst aktiviert und gestartet (Autostart beim Booten aktiv)."

  elif command -v rc-update >/dev/null 2>&1; then
    info "Richte OpenRC-Autostart (${SERVICE_NAME}) ein..."
    cat > "/etc/init.d/${SERVICE_NAME}" <<EOF
#!/sbin/openrc-run
name="ServerStats"
description="Linux Server Telemetry Web UI"
command="${python_bin}"
command_args="${INSTALL_DIR}/run.py --host ${HOST} --port ${PORT} --interval ${INTERVAL}"
command_background=true
pidfile="/run/${SERVICE_NAME}.pid"
directory="${INSTALL_DIR}"

depend() {
    need net
}
EOF
    chmod +x "/etc/init.d/${SERVICE_NAME}"
    rc-update add "${SERVICE_NAME}" default
    rc-service "${SERVICE_NAME}" restart
    ok "OpenRC-Dienst aktiviert und gestartet."
  else
    warn "Kein systemd/OpenRC erkannt. Du kannst ServerStats manuell starten mit:"
    echo "  ${python_bin} ${INSTALL_DIR}/run.py --host ${HOST} --port ${PORT}"
  fi
}

# -----------------------------------------------------------------------------
# Ausführung
# -----------------------------------------------------------------------------
install_packages
setup_sensors
install_files
setup_autostart

SERVER_IP="$(hostname -I 2>/dev/null | awk '{print $1}' || echo '127.0.0.1')"
[[ -z "${SERVER_IP}" ]] && SERVER_IP="127.0.0.1"

echo ""
ok "Installation abgeschlossen!"
echo "  Web-Oberfläche : http://${SERVER_IP}:${PORT}"
echo "  Konfiguration  : ${ENV_FILE}"
echo "  Status prüfen  : systemctl status ${SERVICE_NAME}"
echo "  Live-Logs      : journalctl -u ${SERVICE_NAME} -f"
echo "  Deinstallieren : sudo ./install.sh --uninstall"
echo ""
