# PwnServer Guide

## Overview
Das PwnServer-Projekt verwandelt einen Raspberry Pi Zero 2 W in einen BadUSB, der als USB-Tastatur erkannt wird und gleichzeitig ein Webinterface bietet, um Ducky Script Payloads über ein erstelltes WLAN-Netzwerk auszuführen.

Mit diesem Projekt kannst du Payloads in Ducky Script hochladen, speichern, suchen und direkt über das Webinterface auf dem verbundenen Zielgerät ausführen.

---

## Funktionen
- USB-HID Unterstützung (als Tastatur erkannt)
- Startet ein WLAN-Netzwerk (Hotspot)
- Erstellen, Ausführen und Speichern von Payloads
- Webinterface für die Steuerung von Ducky Script Payloads

---

[//]: # (## Projektstruktur)

[//]: # (- `pwn_server.py`: Hauptserver, der das Webinterface bereitstellt und Payloads injiziert.)

[//]: # (- `config.yaml`: Konfigurationsdatei für SSID, Passwort und WebUI Zugangsdaten.)

[//]: # (- `run_payload.sh`: Bash-Skript zur Ausführung der Ducky Script Payloads.)

[//]: # (- `templates/index.html`: Webinterface für die Steuerung des PwnServers.)

[//]: # (- `payloads/`: Verzeichnis für gespeicherte Ducky Script Payloads.)

---

## Requirements
1. **Hardware**
   - Raspberry Pi Zero 2 W
   - USB-Verbindung zu einem Rechner, um den Pi als BadUSB zu betreiben
   - optional:
     - pisugar2 battery
2. **Software**
   - **Kali Linux** vorinstalliert auf dem Pi (aktuellste Version)
   - **Python 3** und **pip**
---

## Start the Server:
```bash
cd ~
sudo su
pwnServer/start_server.sh
```


---




## Nutzung des PwnServer

1. Pi starten und Webinterface aufrufen
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
- Die Anleitung ist in logische Abschnitte unterteilt: 
   - Voraussetzungen, 
   - Installationsschritte,
   - Nutzung und Fehlersuche.
- Wichtige Befehle und Dateipfade sind klar strukturiert.
- Es gibt Hinweise zur Fehlersuche und zur Anpassung der Konfiguration.
```
Du kannst diese Datei einfach in dein Git-Repository als `INSTALLATION.md` einfügen, um deinen Nutzern eine einfache Installationsanleitung zur Verfügung zu stellen.
