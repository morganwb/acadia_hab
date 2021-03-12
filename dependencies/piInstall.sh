#!/bin/bash
# piInstall.sh
# Install all dependencies to use the Raspberry Pi Zero as an APRS coprocessor
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


# Install the CircuitPython libraries to run Bluetooth Low Energy and communicate with the other flight computers
sudo pip3 install adafruit-circuitpython-ble
