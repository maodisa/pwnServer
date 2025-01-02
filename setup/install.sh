#!/bin/bash

# Update and upgrade the system
sudo apt update && sudo apt-get update
# sudo apt upgrade -y

# Install required packages
sudo apt-get install -y hostapd dnsmasq python3 python3-pip python3.12-venv git

# Stop and disable services to configure
sudo systemctl stop hostapd dnsmasq
dpkg-reconfigure hostapd

# Create wlan_ap interface
sudo iw dev wlan0 interface add wlan_ap type __ap
sudo ip link set wlan_ap up

# Configure Hostapd
cat <<EOT | sudo tee /etc/hostapd/hostapd.conf
interface=wlan_ap
driver=nl80211
ssid=PwnC2Server_uni_project__no_harm
hw_mode=g
channel=6
country_code=DE
auth_algs=1
wpa=2
wpa_passphrase=Start12345
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ignore_broadcast_ssid=0
wmm_enabled=0
wpa_group_rekey=1800
EOT

cat <<EOT | sudo tee /etc/default/hostapd
DAEMON_CONF="/etc/hostapd/hostapd.conf"
EOT

# Configure dnsmasq
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.backup
cat <<EOT | sudo tee /etc/dnsmasq.conf
interface=wlan_ap
except-interface=eth0
dhcp-range=192.168.10.50,192.168.10.150,255.255.255.0,24h
EOT

cat <<EOT | sudo tee /etc/dhcpcd.conf
interface wlan_ap
static ip_address=192.168.10.1/24
nohook wpa_supplicant
EOT

cat <<EOT | sudo tee -a /etc/network/interfaces
allow-hotplug wlan_ap
iface wlan_ap inet static
    address 192.168.10.1
    netmask 255.255.255.0
EOT

# Enable and start services
sudo systemctl unmask hostapd
sudo systemctl unmask dnsmasq
sudo systemctl enable hostapd dnsmasq
sudo systemctl restart hostapd dnsmasq

# Additional configuration for BadUSB setup
cd ~
git clone https://github.com/maodisa/pwnServer.git
cd pwnServer
sudo chmod +x start_server.sh

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r setup/requirements.txt

# Configure udev rules
cat <<EOT | sudo tee /etc/udev/rules.d/99-badusb.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="1d6b", ATTR{idProduct}=="0002", RUN+="/usr/bin/python3 ~/pwnServer/app/admin/python/ducky_script/hid_trigger.py"
EOT

sudo chmod +x ~/pwnServer/app/admin/python/ducky_script/hid_trigger.py

# Configure USB gadget
cat <<EOT | sudo tee /usr/bin/pwnPal_usb
#!/bin/bash
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

# Add HID function
mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length
echo -ne \x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x03\x95\x05\x75\x01\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91\x03\x95\x06\x75\x08\x15\x00\x25\x65\x05\x07\x19\x00\x29\x65\x81\x00\xc0 > functions/hid.usb0/report_desc
ln -s functions/hid.usb0 configs/c.1/
ls /sys/class/udc > UDC
EOT

sudo chmod +x /usr/bin/pwnPal_usb

# Final system configuration
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
echo "libcomposite" | sudo tee -a /etc/modules

# Reboot to apply changes
sudo reboot
