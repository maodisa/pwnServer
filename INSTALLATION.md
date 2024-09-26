# Installation steps
## battery - pisugar2 - OPTIONAL!
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

## remove xfce to reduce cpu usage: 

```bash
sudo apt purge xfce4* lightdm*
```
---


## 1. Projekt klonen

Zuerst musst du das Projekt auf den Raspberry Pi klonen:

```bash
git clone https://github.com/maodisa/pwnServer.git
cd pwnServer
```
## 2. Abhängigkeiten installieren
Installiere die notwendigen Python-Pakete:

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip git
pip3 install -r requirements.txt
```



### install python venv!!! --> oder alles als root?
```bash
sudo apt install python3.12-venv
# im pwnServer ordner:
python3 -m venv .venv

# Jedes Mal, wenn du die Anwendung startest, musst du die virtuelle Umgebung aktivieren
source .venv/bin/activate
```

### Set-Up autorun for ducky
```bash
lsusb
# $ Bus 001 Device 002: ID <Vendor-ID>:<Product-ID> [Beschreibung]
sudo nano /etc/udev/rules.d/99-badusb.rules
# add lines:
# ANPASSEN AUF ROOT!!!
## SUBSYSTEM=="usb", ATTR{idVendor}=="<Vendor-ID>", ATTR{idProduct}=="<Product-ID>", RUN+="/usr/bin/python3 /home/kali/pwnServer/app/admin/python/ducky_script/hid_trigger.py"

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
sudo apt update
sudo apt dist-upgrade


echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
sudo echo "libcomposite" | sudo tee -a /etc/modules

# Creating the config script
sudo touch /usr/bin/pwnPal_usb
pi@raspberrypi:~ $ sudo chmod +x /usr/bin/pwnPal_usb # {DeviceName}
```
1. Run the crontab -e command
2. Add the job to the @reboot.
3. Add the following line to the ent of the file:
4. @reboot /usr/bin/pwnPal_usb # libcomposite configuration
5. Save and close the file. 

Now job will run at the Linux boot time.
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



