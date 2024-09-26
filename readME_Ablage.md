# OLD Method
Establish an SSH connection with your Pi and use the next command to create a new Python script:

```bash
nano example.py
```

```python
#!/usr/bin/env python3
NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def execute_duckyscript(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            command = line.strip()
            if command.startswith("DELAY"):
                delay_time = int(command.split()[1])
                time.sleep(delay_time / 1000.0)  # DELAY in ms
            elif command.startswith("PRINT"):
                text = command.split(' ', 1)[1]
                for char in text:
                    write_character(char)
            # Weitere Duckyscript-Befehle können hier hinzugefügt werden

def write_character(char):
    # Hier können die Charaktere für die Eingabe hinzugefügt werden
    if char.isalpha():
        key_code = ord(char.lower()) - ord('a') + 4  # a=4, b=5, ..., z=30
        write_report(NULL_CHAR*2 + chr(key_code) + NULL_CHAR*5)
        write_report(NULL_CHAR*8)  # Release key
    elif char == ' ':
        write_report(NULL_CHAR*2 + chr(44) + NULL_CHAR*5)  # SPACE
        write_report(NULL_CHAR*8)  # Release key
    # Weitere Zeichen können hier behandelt werden

if __name__ == "__main__":
    import time
    execute_duckyscript("duckyscript.txt")
```
# wie verschiedene keyboards hinzufügen und alles dynamischer halten?
Erstelle "duckyscript.txt":
```yaml
DELAY 1000
PRINT Hello
DELAY 500
PRINT World

```


execute Code via:

```bash
sudo python3 example.py
```


![img.png](img.png)




# OLD Installation









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