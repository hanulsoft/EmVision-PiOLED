#!/bin/bash
# Install EmVision OLED

sudo usermod -aG i2c $USER
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo apt-get update
sudo apt install python3-pip python3-pil sysstat -y
pip3 install Adafruit-SSD1306