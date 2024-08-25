# Raspberry PI Quirks

### Headless Setup
Flash a Raspian on an SDCard, then mount it and
```bash
# enable SSH (pi:raspberry)
touch /run/media/$USER/boot/ssh

# fallback to a static IP
sudo tee -a /run/media/$USER/rootfs/etc/dhcpcd.conf > /dev/null <<EOT
# define static profile
profile static_eth0
static ip_address=10.0.0.23/24
static routers=10.0.0.1
static domain_name_servers=10.0.0.1

# fallback to static profile on eth0
interface eth0
fallback static_eth0
EOT

sudo umount /run/media/$USER/boot
```

### PI Bootstrapping
* Direct LAN connection with static IP in same network, then `ssh-copy-id pi@10.0.0.23`.   
* `sudo raspi-config`:   
  1 - change password   
  2 - N1, N2 - change hostname, setup WiFi   
  5 - P4, P5 - enable SPI, enable I2C   
* `sudo apt install unattended-upgrades sshfs python3-pip`
* `sudo reboot`

### connect4cube Installation
PWM access requires [root permissions](https://github.com/jgarff/rpi_ws281x/issues/326).

The rpi-ws281x package is only available on the pi, but pipenv does not support multiple
package sets apart from --dev. So it has to be installed separately with the install-rpi script.
```bash
sudo pip3 install pipenv
sudo pipenv install
sudo pipenv run install-rpi
sudo pipenv shell
```

### Automatically Start connect4cube
Use a systemd unit file to automatically start connect4cube and keep restarting it once it stops.
The connect4cube project has to be located in the pi home directory: /home/pi/connect4cube
```bash
cd
git clone https://github.com/keykey7/connect4cube.git
sudo cp connect4cube.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/connect4cube.service
sudo systemctl daemon-reload
sudo systemctl enable connect4cube.service
sudo systemctl start connect4cube.service
```
