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
sudo apt-get install -y python3-pip python3-pil fonts-dejavu python3-venv

echo "=== Creating virtual environment ==="
python3 -m venv venv

echo "=== Installing Python packages ==="
./venv/bin/pip install adafruit-circuitpython-epd adafruit-blinka Pillow

echo "=== Setting up .env ==="
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from template. Edit it with your OpenWeather API key!"
fi

echo "=== Installing systemd service ==="
sudo cp weather-display.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable weather-display

echo "=== Done ==="
if [ -n "$REBOOT_NEEDED" ]; then
    echo "Reboot required for SPI to take effect: sudo reboot"
fi
echo "Edit .env with your API key, then: sudo systemctl start weather-display"
