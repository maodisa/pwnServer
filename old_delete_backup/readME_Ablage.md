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


[//]: # (#####################################################################################################################)

```bash
sudo apt install dnsmasq hostapd
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd
sudo systemctl disable dnsmasq
sudo systemctl disable hostapd

sudo nano /etc/dhcpcd.conf
```
Add:
```text
interface wlan0
static ip_address=192.168.4.1/24
nohook wpa_supplicant
```
```bash
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.backup
sudo nano /etc/dnsmasq.conf
```
Add:
```text
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
```
```bash
sudo nano /etc/hostapd/hostapd.conf
```
Add:
```text
interface=wlan0
driver=nl80211
ssid=PiAccessPoint
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=DeinSicheresPasswort
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
```
```bash
sudo nano /etc/default/hostapd
```
Add:
```text
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

```bash
sudo nano /etc/sysctl.conf
```
Add:
```text
net.ipv4.ip_forward=1
```
```bash
sudo sysctl -p

sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
sudo nano /etc/rc.local
```
Add:
```text
#!/bin/bash
iptables-restore < /etc/iptables.ipv4.nat
exit 0
```
```bash
sudo chmod +x /etc/rc.local

sudo nano /etc/systemd/system/rc-local.service
```
Add:
```text
[Unit]
Description=/etc/rc.local Compatibility
ConditionPathExists=/etc/rc.local

[Service]
Type=forking
ExecStart=/etc/rc.local start
TimeoutSec=0
StandardOutput=tty
RemainAfterExit=yes
SysVStartPriority=99

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable rc-local
sudo systemctl start rc-local

sudo systemctl status rc-local
```










```bash
sudo journalctl -u dnsmasq
sudo journalctl -u dnsmasq -f # echtzeitanzeige

cat /proc/sys/net/ipv4/ip_forward

# Der Wert sollte 1 sein. Falls nicht, kannst du das folgendermaßen aktivieren:
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
sudo nano /etc/sysctl.conf
```
Add:
```text

```


[//]: # (################################################################################################################)



## Projekt klonen
```bash
sudo apt-get update
sudo apt dist-upgrade -y
sudo apt-get install -y python3 python3-pip git python3.12-venv
```

Zuerst musst du das Projekt auf den Raspberry Pi klonen:

```bash
git clone https://github.com/maodisa/pwnServer.git
cd pwnServer
```
## Abhängigkeiten installieren
Installiere die notwendigen Python-Pakete:


### install python venv!!! --> oder alles als root?
```bash
# im pwnServer ordner:
python3 -m venv .venv

# Jedes Mal, wenn du die Anwendung startest, musst du die virtuelle Umgebung aktivieren
source .venv/bin/activate
pip3 install -r requirements.txt
```

### Set-Up autorun for ducky
```bash
lsusb
# $ Bus 001 Device 002: ID <Vendor-ID>:<Product-ID> [Beschreibung]
#sudo nano /etc/udev/rules.d/99-badusb.rules
#sudo touch /etc/udev/rules.d/99-badusb.rules
# add lines:
# ANPASSEN AUF ROOT!!!
## SUBSYSTEM=="usb", ATTR{idVendor}=="<Vendor-ID>", ATTR{idProduct}=="<Product-ID>", RUN+="/usr/bin/python3 /home/kali/pwnServer/app/admin/python/ducky_script/hid_trigger.py"
sudo echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="1d6b", ATTR{idProduct}=="0002", RUN+="/usr/bin/python3 ~/pwnServer/app/admin/python/ducky_script/hid_trigger.py"' | sudo tee -a /etc/udev/rules.d/99-badusb.rules
# change to executable
sudo chmod +x /home/kali/pwnServer/app/admin/python/ducky_script/hid_trigger.py

#restart the service:


# Debugging der Udev-Regeln
sudo udevadm monitor --environment --udev

# Überprüfen der Systemprotokolle:
sudo journalctl -f
```




## Pi as HID-Device (Keyboard)
https://randomnerdtutorials.com/raspberry-pi-zero-usb-keyboard-hid/
```bash
ip a

echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
sudo echo "libcomposite" | sudo tee -a /etc/modules

# Creating the config script
sudo touch /usr/bin/pwnPal_usb
sudo chmod +x /usr/bin/pwnPal_usb # {DeviceName}
```

```bash
sudo nano /usr/bin/pwnPal_usb
```
Add the following:
```bash
#!/bin/bash
cd /sys/kernel/config/usb_gadget/
mkdir -p isticktoit
cd isticktoit
echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
mkdir -p strings/0x409
echo "fedcba0123456789" > strings/0x409/serialnumber
echo "Pwn Community" > strings/0x409/manufacturer
echo "Good USB Device" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

# Add functions here
# https://www.isticktoit.net/?p=1383
# HID!!
mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.usb0/report_desc
ln -s functions/hid.usb0 configs/c.1/

# MOUSE!!
mkdir -p functions/hid.mouse
echo 0 > functions/hid.mouse/protocol
echo 0 > functions/hid.mouse/subclass
echo 7 > functions/hid.mouse/report_length
echo -ne \\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x03\\x05\\x01\\x09\\x30\\x09\\x31\\x15\\x81\\x25\\x7f\\x75\\x08\\x95\\x02\\x81\\x06\\xc0\\xc0 > functions/hid.mouse/report_desc
ln -s functions/hid.mouse configs/c.1/

# USB!!
FILE=/piusb.bin
MNTPOINT=/mnt/usb_share
mkdir -p ${MNTPOINT}
# mount -o loop,ro,offset=1048576 -t ext4 $FILE ${FILE/img/d} # FOR OLD WAY OF MAKING THE IMAGE
mount -o loop,ro, -t vfat $FILE ${MNTPOINT} # FOR IMAGE CREATED WITH DD
mkdir -p functions/mass_storage.usb0
echo 1 > functions/mass_storage.usb0/stall
echo 0 > functions/mass_storage.usb0/lun.0/cdrom
echo 0 > functions/mass_storage.usb0/lun.0/ro
echo 0 > functions/mass_storage.usb0/lun.0/nofua
echo $FILE > functions/mass_storage.usb0/lun.0/file
ln -s functions/mass_storage.usb0 configs/c.1/

# End functions

ls /sys/class/udc > UDC
```