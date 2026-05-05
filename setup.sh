#!/bin/bash
set -e

echo "=== E-Ink Weather Display Setup ==="

echo "=== Enabling SPI ==="
if ! grep -q "^dtparam=spi=on" /boot/firmware/config.txt; then
    echo "dtparam=spi=on" | sudo tee -a /boot/firmware/config.txt
    echo "SPI enabled. Reboot required after setup."
    REBOOT_NEEDED=1
else
    echo "SPI already enabled."
fi

echo "=== Installing system packages ==="
sudo apt-get update
sudo apt-get install -y python3-pip python3-pil fonts-dejavu

echo "=== Installing Python packages ==="
pip3 install -r requirements.txt

echo "=== Done ==="
if [ -n "$REBOOT_NEEDED" ]; then
    echo "Reboot required for SPI to take effect: sudo reboot"
fi
