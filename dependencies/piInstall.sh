#!/bin/bash
# piInstall.sh
# Install all dependencies to use the Raspberry Pi Zero as an APRS beacon
sudo apt-get update -y && sudo apt-get upgrade -y


# Install DireWolf and dependencies
sudo apt-get install cmake libasound2-dev libudev-dev -y
git clone https://www.github.com/wb2osz/direwolf && cd direwolf
git checkout dev
mkdir build && cd build
cmake -DUNITTEST=1 ..
make -j4
make test
sudo make install
make install-conf


# Install the I2S drivers to run the Adafruit I2S audio bonnet
curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh | bash


# Install the Adafruit Libraries to interface with the I2C sensors
sudo pip3 install adafruit-circuitpython-bmp3xx adafruit-circuitpython-lc709203f adafruit-circuitpython-lsm6ds adafruit-circuitpython-lsm6ds adafruit-circuitpython-lis3mdl adafruit-circuitpython-gps

