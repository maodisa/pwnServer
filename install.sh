#!/bin/bash
# update the pi
sudo apt-get update
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
pip3 install -r requirements.txt

# search for usb-port
#lsusb
# $ Bus 001 Device 002: ID <Vendor-ID>:<Product-ID> [Beschreibung]

# create File "99-badusb.rules" and write to it
sudo echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="1d6b", ATTR{idProduct}=="0002", RUN+="/usr/bin/python3 ~/pwnServer/app/admin/python/ducky_script/hid_trigger.py"' | sudo tee -a /etc/udev/rules.d/99-badusb.rules

# change to executable
sudo chmod +x /home/kali/pwnServer/app/admin/python/ducky_script/hid_trigger.py

# setup pi config to set pi as usb
sudo echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
sudo echo "dwc2" | sudo tee -a /etc/modules
sudo echo "libcomposite" | sudo tee -a /etc/modules

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
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02>ln -s functions/hid.usb0 configs/c.1/

# MOUSE!!
mkdir -p functions/hid.mouse
echo 0 > functions/hid.mouse/protocol
echo 0 > functions/hid.mouse/subclass
echo 7 > functions/hid.mouse/report_length
echo -ne \\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03>ln -s functions/hid.mouse configs/c.1/

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

ls /sys/class/udc > UDC' | tee -a /usr/bin/pwnPal_usb

sudo chmod +x /usr/bin/pwnPal_usb