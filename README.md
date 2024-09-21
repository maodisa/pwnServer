# PwnServer Guide

## Overview
Das PwnServer-Projekt verwandelt einen Raspberry Pi Zero 2 W in einen BadUSB, der als USB-Tastatur erkannt wird und gleichzeitig ein Webinterface bietet, um Ducky Script Payloads über ein erstelltes WLAN-Netzwerk auszuführen.

Mit diesem Projekt kannst du Payloads in Ducky Script hochladen, speichern, suchen und direkt über das Webinterface auf dem verbundenen Zielgerät ausführen.

---

## Funktionen
- Startet ein WLAN-Netzwerk (Hotspot)
- Webinterface für die Steuerung von Ducky Script Payloads
- Ausführen und Speichern von Payloads
- USB-HID Unterstützung (als Tastatur erkannt)

---

## Projektstruktur
- `pwn_server.py`: Hauptserver, der das Webinterface bereitstellt und Payloads injiziert.
- `config.yaml`: Konfigurationsdatei für SSID, Passwort und WebUI Zugangsdaten.
- `run_payload.sh`: Bash-Skript zur Ausführung der Ducky Script Payloads.
- `templates/index.html`: Webinterface für die Steuerung des PwnServers.
- `payloads/`: Verzeichnis für gespeicherte Ducky Script Payloads.

---

## Requirements
1. **Hardware**
   - Raspberry Pi Zero 2 W
   - USB-Verbindung zu einem Rechner, um den Pi als BadUSB zu betreiben
   - WLAN-Adapter (integriert im Raspberry Pi Zero 2 W)
   
2. **Software**
   - **Kali Linux** vorinstalliert auf dem Pi (aktuellste Version)
   - **Python 3** und **pip**
   - **Flask** Webframework
   - **nmcli** für WLAN-Netzwerkmanagement

3. **Ducky Script Interpreter**
   - Wir verwenden das Tool **DuckPi**, um Ducky Script Payloads auf dem Pi auszuführen.

---

### battery - pisugar2 - OPTIONAL!
```bash
sudo su
raspi-config # --> i2f aktivieren

exit

wget https://cdn.pisugar.com/release/pisugar-power-manager.sh
bash pisugar-power-manager.sh -c release
nano /etc/pisugar-server/config.json
```

change the text

```text
"auto_power_on": true,
```

or use the webinterface

```bash
reboot
```

---

















## Installation steps

### 1. Projekt klonen

Zuerst musst du das Projekt auf den Raspberry Pi klonen:

```bash
git clone https://github.com/maodisa/pwnServer.git
cd pwnServer
```
### 2. Abhängigkeiten installieren
Installiere die notwendigen Python-Pakete:

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip git
pip3 install -r requirements.txt
```

### 3. Ducky Script Interpreter (DuckPi) installieren
DuckPi wird verwendet, um Ducky Script in Tastatureingaben umzuwandeln. Klone und installiere DuckPi:

```bash
cd /opt/
git clone https://github.com/JohnSmithTech/duckpi.git
cd duckpi
sudo python3 setup.py install
```

### 4. HID Gadget (BadUSB) konfigurieren
Damit der Raspberry Pi als USB-Tastatur erkannt wird, musst du das HID Gadget konfigurieren. Führe folgendes Skript aus:

```bash
sudo bash -c 'echo -e "options g_hid usbgadget=1 hid=2" > /etc/modprobe.d/g_hid.conf'
```

Starte anschließend den Pi neu:

```bash
sudo reboot
```

### 5. WLAN-Hotspot konfigurieren
Das Projekt verwendet nmcli, um ein WLAN-Netzwerk zu erstellen, sobald der Pi eingeschaltet wird. Das Netzwerk wird über das Flask-Backend gesteuert.

Du kannst die Konfiguration in der Datei config.yaml anpassen:

```yaml
SSID: "PwnPi"
Password: "supersecret"
WebUI_Username: "admin"
WebUI_Password: "password"
```
### 6. Systemd-Service einrichten
Erstelle einen Systemd-Service, damit das PwnServer-Programm automatisch beim Start des Raspberry Pi ausgeführt wird.

Erstelle eine neue Service-Datei:

```bash
sudo nano /etc/systemd/system/pwnserver.service
```
Füge folgenden Inhalt in die Datei ein:

```ini
[Unit]
Description=PwnServer Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/kali/pwnServer/pwn_server.py
WorkingDirectory=/home/kali/pwnServer
StandardOutput=inherit
StandardError=inherit
Restart=always
User=kali

[Install]
WantedBy=multi-user.target
```

Speichere die Datei und starte den Service:

```bash
sudo systemctl enable pwnserver.service
sudo systemctl start pwnserver.service
```
### 7. Projektverzeichnisstruktur
Das Projekt sollte die folgende Verzeichnisstruktur haben:

```graphql

pwnServer/
│
├── config.yaml                   # Konfigurationsdatei für Netzwerk- und Web-UI-Einstellungen
├── pwn_server.py                 # Haupt-Server-Skript (startet Webserver und steuert BadUSB)
├── run_payload.sh                # Bash-Skript, um die Ducky Script Payload auszuführen
├── requirements.txt              # Python-Abhängigkeiten für das Projekt
├── README.md                     # Projektbeschreibung
├── INSTALLATION.md               # Installationsanleitung
├── payloads/                     # Verzeichnis für gespeicherte Ducky Script Payloads
│   └── example_payload.txt        # Beispiel-Payload
├── templates/                    # HTML-Templates für das Webinterface
│   └── index.html                # Haupt-HTML-Seite des Webservers
└── scripts/                      # Verzeichnis für unterstützende Skripte oder Dateien
    └── duckpi/                   # Verzeichnis mit DuckPi (optional, wenn du es lokal ins Projekt einbinden willst)
```

## Nutzung des PwnServer

1. Pi anschließen und Webinterface aufrufen
   - Sobald der Pi über USB mit einem Rechner verbunden ist, startet er automatisch und wird als USB-Tastatur erkannt. Gleichzeitig wird der WLAN-Hotspot aktiviert.
   - Verbinde dich mit dem WLAN des Pi (SSID und Passwort stehen in config.yaml).
   - Öffne einen Browser und gehe zu http://<Pi-IP-Adresse> (normalerweise http://192.168.4.1).
2. Ducky Script Payloads ausführen
   - Du kannst entweder direkt ein Ducky Script Payload im Webinterface eingeben und ausführen oder
   - Du kannst Payloads hochladen und später über eine Suche abrufen und ausführen.
3. Payloads suchen und ausführen
   - Das Webinterface bietet eine Suchfunktion, mit der du nach gespeicherten Payloads suchen und sie schnell ausführen kannst.

### Konfiguration
Anpassung der config.yaml
In der Datei config.yaml kannst du folgende Parameter anpassen:

SSID: Der Name des WLAN-Hotspots, den der Pi erstellt.
Password: Das Passwort für den WLAN-Hotspot.
WebUI_Username: Der Benutzername für den Login ins Webinterface.
WebUI_Password: Das Passwort für das Webinterface.
### Fehlersuche

#### 1. Service-Probleme
Falls der PwnServer nicht automatisch startet, kannst du den Status des Services überprüfen:

```bash
sudo systemctl status pwnserver.service
```
#### 2. USB-HID Probleme
Falls der Pi nicht als USB-Tastatur erkannt wird, überprüfe, ob das HID Gadget korrekt eingerichtet wurde:

```bash
lsmod | grep g_hid
```
## Lizenz
Dieses Projekt steht unter der MIT-Lizenz. Siehe die Datei LICENSE für weitere Details.

```yaml
---

### Erklärungen

- Die Datei ist in Markdown-Format, ideal für Dokumentationen in Git-Repositories.
- Die Anleitung ist in logische Abschnitte unterteilt: Voraussetzungen, Installationsschritte, Nutzung und Fehlersuche.
- Wichtige Befehle und Dateipfade sind klar strukturiert.
- Es gibt Hinweise zur Fehlersuche und zur Anpassung der Konfiguration.
```
Du kannst diese Datei einfach in dein Git-Repository als `INSTALLATION.md` einfügen, um deinen Nutzern eine einfache Installationsanleitung zur Verfügung zu stellen.
