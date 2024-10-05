## Setup AccessPoint Service

### new interface wlan_ap

```bash
sudo nano /usr/local/bin/create_wlan_ap.sh
```

Add text:

```text
#!/bin/bash

# Erstelle das wlan_ap Interface
sudo iw dev wlan0 interface add wlan_ap type __ap


sudo ip link set wlan_ap up
sudo ifdown wlan_ap && sudo ifup wlan_ap
sudo ip link set wlan0 up
sudo ifdown wlan0 && sudo ifup wlan0


# Starte hostapd
sudo systemctl restart hostapd
```

```bash
sudo chmod +x /usr/local/bin/create_wlan_ap.sh

sudo nano /etc/systemd/system/wlan_ap.service
```

```text
[Unit]
Description=Create wlan_ap interface and start hostapd
After=network.target

[Service]
ExecStart=/usr/local/bin/create_wlan_ap.sh
Type=oneshot
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable wlan_ap.service
```


### hostapd

```bash
############################### HOSTAPD ###############################
sudo apt update
sudo apt-get update


sudo iw dev wlan0 interface add wlan_ap type __ap
ip addr show


sudo apt-get install -y hostapd
sudo service hostapd stop
sudo update-rc.d hostapd disable

sudo nano /etc/hostapd/hostapd.conf
```

```text
# Set interface
interface=wlan_ap
# Set driver to
driver=nl80211
# Set your desired ssid(Wi-Fi name)
ssid=MyPiNetwork7
# Set the access point hardware mode to 802.11g
hw_mode=g
# Select WIFI channel
channel=6
country_code=DE
# Ensure to enable only WPA2
auth_algs=1
wpa=2
wpa_passphrase=Start12345
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ignore_broadcast_ssid=0
```

```bash
sudo nano /etc/default/hostapd
```

Add text:

```text
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

### dnsmasq

```bash
############################### DNSMASQ ###############################
sudo su
#sudo apt update
sudo apt-get update
sudo apt-get install -y dhcpcd5 dnsmasq
sudo service dnsmasq stop
sudo update-rc.d dnsmasq disable


sudo mv /etc/dnsmasq.conf /etc/dnsmasq.backup
sudo nano /etc/dnsmasq.conf
```

Add Text:

```text
interface=wlan_ap
# except-interface=eth0
dhcp-range=192.168.10.50,192.168.10.150,255.255.255.0,24h
```

```bash
sudo nano /etc/dhcpcd.conf
```

Add Text:

```text
interface wlan_ap
static ip_address=192.168.10.1/24
nohook wpa_supplicant
```

```bash
sudo nano /etc/network/interfaces
```

Add Text:

```text
allow-hotplug wlan_ap
iface wlan_ap inet static
    address 192.168.10.1
    netmask 255.255.255.0
```

```bash
sudo ip link set wlan_ap up
sudo ifdown wlan_ap && sudo ifup wlan_ap
sudo ip link set wlan0 up
sudo ifdown wlan0 && sudo ifup wlan0
```

```bash
sudo systemctl unmask hostapd
sudo systemctl unmask dnsmasq # kann glaube ich raus
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
sudo update-rc.d hostapd enable
sudo update-rc.d dnsmasq enable

sudo raspi-config nonint do_expand_rootfs
sudo raspi-config nonint do_wifi_country DE
sudo raspi-config nonint do_change_timezone Europe/Berlin
sudo raspi-config nonint do_hostname pwnServer
```


Set the WIFI-Country right

```bash
sudo raspi-config
```

1. "04 Localisation Options"
2. "I4 Change Wi-fi Country"
3. Set to "DE" - Germany
4. Reboot the pi if asked - if not, rebot the pi manually

After Reboot - Check if Services are running

```bash
sudo service --status-all
```

1. hostapd
2. dnsmasq

---
