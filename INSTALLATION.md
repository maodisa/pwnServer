# Installation steps

## Setup Micro-SD-Card

### 1 Click

<img src="README_statics/installation/kali_setup/img_0.png" alt="drawing" style="width:500px;"/>

### 2 Click

<img src="README_statics/installation/kali_setup/img_1.png" alt="drawing" style="width:500px;"/>

### 3 Click and scroll down

<img src="README_statics/installation/kali_setup/img_2.png" alt="drawing" style="width:500px;"/>

### 4 Click

<img src="README_statics/installation/kali_setup/img_3.png" alt="drawing" style="width:500px;"/>

### 5. Click

<img src="README_statics/installation/kali_setup/img_4.png" alt="drawing" style="width:500px;"/>

### 6. Click

<img src="README_statics/installation/kali_setup/img_5.png" alt="drawing" style="width:500px;"/>

### 7. Click

<img src="README_statics/installation/kali_setup/img_6.png" alt="drawing" style="width:500px;"/>

### 8. Click (BE CAREFULLY)

<img src="README_statics/installation/kali_setup/img_7.png" alt="drawing" style="width:500px;"/>

### 9. Click

<img src="README_statics/installation/kali_setup/img_8.png" alt="drawing" style="width:500px;"/>

### 10. Click

<img src="README_statics/installation/kali_setup/img_9.png" alt="drawing" style="width:500px;"/>

### 11. Click

<img src="README_statics/installation/kali_setup/img_10.png" alt="drawing" style="width:500px;"/>


---

## Connect the Pi to the internet

Login to your pi:

- Username: kali
- Password: kali

[//]: # (### WIFI)

[//]: # (use the HDMI port and GUI to connect the pi to wifi via kali-linux)

### use LAN !!!

use the USB-Data Port to connect a LAN-Cable to the pi

---

## Connect to your Pi

### SSH into your pi

use Windows cmd or powershell to ssh into your pi. Look in your router witch ip your pi has.

```bash
ssh kali@x.x.x.x
```

replace "x.x.x.x" with the IP of the Raspberry pi in your Network

---

## Setup AccessPoint Service

### new interface wlan_ap

```bash
echo '#!/bin/bash

# Erstelle das wlan_ap Interface
sudo iw dev wlan0 interface add wlan_ap type __ap


sudo ip link set wlan_ap up
sudo ifdown wlan_ap && sudo ifup wlan_ap
sudo ip link set wlan0 up
sudo ifdown wlan0 && sudo ifup wlan0
sudo iw dev wlan0 set power_save off
sudo iw dev wlan_ap set power_save off


sudo systemctl disable dhcpcd
sudo systemctl stop dhcpcd


# Starte hostapd
sudo systemctl restart hostapd' | sudo tee /usr/local/bin/create_wlan_ap.sh

sudo chmod +x /usr/local/bin/create_wlan_ap.sh

echo '[Unit]
Description=Create wlan_ap interface and start hostapd
After=network.target

[Service]
ExecStart=/usr/local/bin/create_wlan_ap.sh
Type=oneshot
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target' | sudo tee /etc/systemd/system/wlan_ap.service

sudo systemctl enable wlan_ap.service
```


### hostapd

```bash
############################### HOSTAPD ###############################
sudo apt update && sudo apt-get update

sudo iw dev wlan0 interface add wlan_ap type __ap
ip addr show


sudo apt-get install -y hostapd
sudo service hostapd stop
sudo update-rc.d hostapd disable

echo '# Set interface
interface=wlan_ap
# Set driver to
driver=nl80211
# Set your desired ssid(Wi-Fi name)
ssid=PwnC2Server_uni_project__no_harm
# Set the access point hardware mode to 802.11g
hw_mode=g
# Select WIFI channel
channel=6
country_code=DE
# Ensure to enable only WPA2
auth_algs=1
wpa=2

# Set Password
wpa_passphrase=Start12345
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ignore_broadcast_ssid=0
wmm_enabled=0
wpa_group_rekey=1800' | sudo tee /etc/hostapd/hostapd.conf

echo 'DAEMON_CONF="/etc/hostapd/hostapd.conf"' | sudo tee /etc/default/hostapd

sudo iw dev wlan_ap set power_save off

```

### dnsmasq

```bash
############################### DNSMASQ ###############################
sudo su
#sudo apt update
#sudo apt-get update
apt-get install -y dhcpcd5 dnsmasq
service dnsmasq stop
update-rc.d dnsmasq disable


mv /etc/dnsmasq.conf /etc/dnsmasq.backup

echo 'interface=wlan_ap
except-interface=eth0
dhcp-range=192.168.10.50,192.168.10.150,255.255.255.0,24h' | tee /etc/dnsmasq.conf

echo 'interface wlan_ap
static ip_address=192.168.10.1/24
nohook wpa_supplicant' | tee /etc/dhcpcd.conf

echo 'allow-hotplug wlan_ap
iface wlan_ap inet static
    address 192.168.10.1
    netmask 255.255.255.0' | tee /etc/network/interfaces
```

NEW!!!!!!!!!!!!!!!!

```bash
############################### DNSMASQ ###############################
sudo su
#sudo apt update
#sudo apt-get update
apt-get install -y dhcpcd5 dnsmasq
service dnsmasq stop
update-rc.d dnsmasq disable


mv /etc/dnsmasq.conf /etc/dnsmasq.backup

echo 'interface=wlan_ap
except-interface=eth0
dhcp-range=10.10.10.50,10.10.10.150,255.255.255.0,24h' | tee /etc/dnsmasq.conf

echo 'interface wlan_ap
static ip_address=10.10.10.1/24
nohook wpa_supplicant' | tee /etc/dhcpcd.conf

echo 'allow-hotplug wlan_ap
iface wlan_ap inet static
    address 10.10.10.1
    netmask 255.255.255.0' | tee /etc/network/interfaces
```

### Put all together

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

#sudo raspi-config nonint do_expand_rootfs
sudo raspi-config nonint do_wifi_country DE
sudo raspi-config nonint do_change_timezone Europe/Berlin
#sudo raspi-config nonint do_hostname pwnServer

sudo reboot
```


After Reboot - Check if Services are running

```bash
sudo service --status-all
```

1. hostapd
2. dnsmasq

---


## Setup BadUSB:

```bash
sudo su
sudo apt update && apt-get update
#sudo apt upgrade
#sudo apt-get upgrade

#sudo apt --fix-broken install

sudo apt-get install -y git
cd ~
# clone Repository
git clone https://github.com/maodisa/pwnServer.git
cd pwnServer/

##### OPTIONAL FOR DEVELOPMENT!!!!
git checkout terminal
#####

sudo chmod +x start_server.sh
```

## Run installation.sh

[//]: # (```bash)

[//]: # (sudo chmod +x install.sh)

[//]: # (sudo ./install.sh)

[//]: # (```)

install.sh:

```bash
# update the pi
#sudo apt-get update
#sudo apt dist-upgrade -y

# install needed packages
sudo apt-get install -y python3 python3-pip python3.12-venv

# create .venv dir
python3 -m venv .venv

# activate venv
# Jedes Mal, wenn du die Anwendung startest, musst du die virtuelle Umgebung aktivieren
#sudo su
source .venv/bin/activate

# install pip requirements
pip3 install -r setup/requirements.txt

# search for usb-port
lsusb
# $ Bus 001 Device 002: ID <Vendor-ID>:<Product-ID> [Beschreibung]

# create File "99-badusb.rules" and write to it
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="1d6b", ATTR{idProduct}=="0002", RUN+="/usr/bin/python3 ~/pwnServer/app/admin/python/ducky_script/hid_trigger.py"' | sudo tee -a /etc/udev/rules.d/99-badusb.rules

# change to executable
sudo chmod +x /home/kali/pwnServer/app/admin/python/ducky_script/hid_trigger.py

# setup pi config to set pi as usb
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
echo "libcomposite" | sudo tee -a /etc/modules

sudo su

# create File "pwnPal_usb" and write to it
echo '#!/bin/bash
cd /sys/kernel/config/usb_gadget/
mkdir -p pwnServer
cd pwnServer
echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "Levi Kuhlmann" > strings/0x409/manufacturer
echo "USB Device" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

# Add functions here
mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.usb0/report_desc
ln -s functions/hid.usb0 configs/c.1/
# End functions

ls /sys/class/udc > UDC' | sudo tee -a /usr/bin/pwnPal_usb

sudo chmod +x /usr/bin/pwnPal_usb
```

After the installations script is done:

1. Run the crontab -e command

```bash
crontab -e
```

2. Choose "nano" as texteditor (press "1" and hit ENTER)
3. Add the following line to the ent of the file:

```text
@reboot /usr/bin/pwnPal_usb # libcomposite configuration
```

4. Save and close the file. Use the following Commands

```text
STRG+x
SHIFT+y
ENTER
```
```bash
sudo reboot
```

Now job will run at the Linux boot time.

---



## (OPTIONAL) battery - pisugar2

```bash
#sudo raspi-config # --> i2f aktivieren

sudo raspi-config nonint do_i2c 0



wget https://cdn.pisugar.com/release/pisugar-power-manager.sh
bash pisugar-power-manager.sh -c release
nano /etc/pisugar-server/config.json
```

change the text

```text
{
  "auth_user": "admin",
  "auth_password": "admin",
  "session_timeout": 3600,
  "i2c_bus": 1,
  "i2c_addr": null,
  "auto_wake_time": null,
  "auto_wake_repeat": 0,
  "single_tap_enable": true,
  "single_tap_shell": "sudo systemctl start pisugar-server",
  "double_tap_enable": true,
  "double_tap_shell": "sudo restart",
  "long_tap_enable": true,
  "long_tap_shell": "sudo shutdown now",
  "auto_shutdown_level": 3.0,
  "auto_shutdown_delay": null,
  "auto_charging_range": [
    80.0,
    100.0
  ],
  "full_charge_duration": null,
  "auto_power_on": true,
  "soft_poweroff": null,
  "soft_poweroff_shell": null,
  "auto_rtc_sync": null,
  "adj_comm": null,
  "adj_diff": null,
  "rtc_adj_ppm": null,
  "anti_mistouch": null,
  "bat_protect": null,
  "battery_curve": null
}
```

or use the webinterface at "127.0.0.1::8421"

```bash
sudo reboot
```

### Commands of controlling pisugar-server systemd service

```bash
# reload daemon
sudo systemctl daemon-reload

# check status
sudo systemctl status pisugar-server

# start service
sudo systemctl start pisugar-server

# stop service
sudo systemctl stop pisugar-server

# disable service
sudo systemctl disable pisugar-server

# enable service
sudo systemctl enable pisugar-server
```

---

## (OPTIONAL) remove xfce (remove desktop env):

to reduce cpu usage

```bash
sudo apt purge xfce4* lightdm*
```


```bash
sudo apt --fix-broken install

sudo apt upgrade
sudo apt-get upgrade

```