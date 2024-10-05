## Setup ipv4 forwarding to internet

### BASIC

```bash
sudo nano /etc/network/interfaces.d/wlan0
```

Add Text:

```text
allow-hotplug wlan0
iface wlan0 inet dhcp
    wpa-ssid "DeinExternesNetzwerkSSID"
    wpa-psk "DeinExternesNetzwerkPasswort"
```

```bash
sudo nano /etc/sysctl.conf
```

Add Text:

```text
net.ipv4.ip_forward=1
```

```bash
sudo sysctl -p

sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```

#### Option 1: Manuelle Erstellung von /etc/rc.local - GENOMMEN

```bash
sudo nano /etc/rc.local
```

Add Text:

```text
#!/bin/sh -e
iptables-restore < /etc/iptables.ipv4.nat
exit 0
```

```bash
sudo chmod +x /etc/rc.local
sudo sysctl -p

sudo nano /etc/systemd/system/rc-local.service
```

Add Text:

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
```

#### Option 2: Verwendung eines systemd-Skripts (empfohlen)

```bash
sudo nano /etc/systemd/system/iptables-restore.service
```

Add Text:

```text
[Unit]
Description=Restore iptables rules
After=network.target

[Service]
Type=oneshot
ExecStart=/sbin/iptables-restore < /etc/iptables.ipv4.nat
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable iptables-restore.service
sudo systemctl start iptables-restore.service
```

### REMOVE POWERSAVER MODE

#### Option 1: Verwende rc.local

```bash
sudo nano /etc/rc.local
```

Add Text before "exit 0":

```text
/sbin/iwconfig wlan0 power off
```

```bash
sudo chmod +x /etc/rc.local
```

#### Option 2: Verwende einen systemd-Service (empfohlene Methode)

```bash
sudo nano /etc/systemd/system/disable-wifi-powersave.service
```

Add Text:

```text
[Unit]
Description=Disable WiFi Power Save
After=network.target

[Service]
ExecStart=/sbin/iwconfig wlan0 power off

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable disable-wifi-powersave.service
sudo systemctl start disable-wifi-powersave.service
```

### DEBUGGING

```bash
sudo iwconfig wlan0 power off
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Add Text:

```text
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=DE

network={
    ssid="DeinNetzwerk"
    psk="DeinPasswort"
    key_mgmt=WPA-PSK
}
```

```bash
sudo nano /etc/rc.local
```

Add Text before "exit 0":

```text
/sbin/iw dev wlan0 set power_save off
```


#### PI Bash hist:

```bash
55  cd /etc/sysctl.d/
56  ll
57  sudo nano 99-sysctl.conf
58  sysctl -p
59  mv 99-sysctl.conf ../sysctl.conf
60  sudo mv 99-sysctl.conf ../sysctl.conf
61  ll
62  cd ..
63  sysctl -p
64  sudo sysctl -p
65  sudo shutdown
66  pi a
67  ip a
68  iwlist
69  iwlist Redmi scan
70  iwlist "FRITZ\!Box 6660 Cable ZN" scan
71  sudo nano  /etc/network/interfaces
72  sudo nano /etc/sysctl.conf
73  sudo nano /etc/network/interfaces.d/wlan1
74  sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE
75  sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
76  sudo nano /etc/rc.local
77  sudo chmod +x /etc/rc.local
78  sudo nano /etc/systemd/system/rc-local.service
79  sudo systemctl enable rc-local
80  sudo systemctl start rc-local
81  nohook wpa_supplicant
82  sudo systemctl restart dhcpcd
83  sudo systemctl restart hostapd
84  sudo systemctl restart dnsmasq
85  sudo reboot
86  ip a
87  sudo reboot
88  sudo apt update
89  sudo nano /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf
90  sudo nano /etc/dnsmasq.conf
91  sudo iptables -t nat -L -v
92  sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE
93  sudo iptables -t nat -L -v
94  sudo nano /etc/hostapd/hostapd.conf
95  sudo iwconfig wlan0 power off
96  sudo iwconfig wlan1 power off
97  sudo nano /etc/rc.local
98  iwconfig wlan0
99  sudo chmod +x /etc/rc.local
100  reboot
101  sudo reboot
102  ip a
103  sudo iwconfig wlan0 power off
104  sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
105  sudo nano /etc/sysctl.conf
106  sudo iptables -t nat -L -v
107  sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
108  sudo nano /etc/dhcp/dhcpd.conf
109  sudo nano /etc/dhcpcd.conf
110  sudo cat /etc/dhcpcd.conf
111  sudo ll /etc/dhcp
112  sudo ls -al /etc/dhcp
113  sudo cat /etc/dhcp/dhclient.conf
114  sudo nano /etc/dnsmasq.conf
115  sudo systemctl restart dnsmasq
116  sudo reboot
117  sudo nano /etc/dnsmasq.conf
118  sudo systemctl restart dnsmasq
119  sudo reboot
120  sudo nano /etc/dnsmasq.conf
121  sudo systemctl restart dnsmasq
122  sudo systemctl status dnsmasq
123  sudo nano /etc/resolv.conf
```














