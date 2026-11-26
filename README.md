# ServerStats

Leichtgewichtige, moderne Weboberfläche zur Echtzeit-Überwachung von Linux-Servern — ohne externe Python-Pakete, ohne Build-Step und mit automatischer Einrichtung von Temperatursensoren und Autostart.

## Funktionen

- **CPU & Kerne**: Gesamtauslastung (User / System / IOWait), Auslastung und Taktfrequenz pro Kern, Load Average (1m / 5m / 15m) und Verlaufsdiagramm.
- **Arbeitsspeicher & Swap**: Belegter RAM, Cache/Puffer, freier Speicher und Swap-Auslastung in Echtzeit.
- **Temperaturen, Lüfter & Leistung**: Automatische Erkennung aller Sensoren über `lm-sensors`, Linux `sysfs` (`hwmon` / `thermal_zone`) sowie `nvidia-smi` — gruppiert nach CPU, GPU, Speicher (NVMe/SATA), Mainboard und Netzwerk, inklusive Lüfterdrehzahlen (RPM) und Leistungsaufnahme (Watt).
- **Verbaute Hardware**: Exaktes CPU-Modell, Kerne/Threads, Taktbereich, Cache-Größen, RAM-Details, Grafikkarte(n), Mainboard/System, BIOS, Betriebssystem, Kernel und physische Laufwerke.
- **Dateisysteme & Disk-I/O**: Alle eingehängten Partitionen mit Belegungsbalken sowie Live-Lese-/Schreibdurchsatz.
- **Netzwerk**: Aktive Adapter, IPv4/IPv6-Adressen, Link-Geschwindigkeit, Live-RX/TX-Rate und Gesamtvolumen.
- **Prozesse**: Durchsuchbare und sortierbare Übersicht der aktivsten Prozesse nach CPU und RAM.
- **Oberfläche**: Klares, reduziertes Design mit Hell- und Dunkelmodus, Deutsch/Englisch-Umschalter und Echtzeit-Updates per Server-Sent Events (SSE).

## Installation auf einem Linux-Server (inkl. Sensoren & Autostart)

```bash
git clone https://github.com/Tamino112/serverstats.git
cd serverstats
sudo ./install.sh
```

Das Installationsskript erledigt automatisch:
1. Installation benötigter Systempakete (`python3`, `lm-sensors`, `pciutils`, optional `dmidecode`) für Debian/Ubuntu, Fedora/RHEL/Rocky/Alma, Arch, openSUSE und Alpine.
2. Nicht-interaktive Sensor-Erkennung (`sensors-detect --auto`) und Laden der Kernel-Module (`coretemp`, `k10temp`, `drivetemp`) inklusive Autoload beim Neustart.
3. Installation nach `/opt/serverstats` und Einrichtung eines `systemd`-Dienstes (`serverstats.service`) mit automatischem Start beim Booten (`Restart=always`).

Danach ist die Seite direkt im Browser unter `http://<server-ip>:8080` erreichbar.

### Optionen bei der Installation

```bash
# Eigener Port oder eigenes Abfrageintervall (z. B. Port 9090, alle 1,5 Sekunden)
sudo ./install.sh --port 9090 --interval 1.5

# Vollständige Deinstallation
sudo ./install.sh --uninstall
```

## Verwaltung (systemd)

```bash
systemctl status serverstats       # Status prüfen
systemctl restart serverstats      # Dienst neu starten
journalctl -u serverstats -f       # Live-Logs anzeigen
```

Die Konfiguration liegt in `/etc/serverstats.env`:

```env
SERVERSTATS_HOST=0.0.0.0
SERVERSTATS_PORT=8080
SERVERSTATS_INTERVAL=2.0
```

## Lokaler Test ohne Installation

```bash
python3 run.py --port 8080
```