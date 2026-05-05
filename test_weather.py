import json
import digitalio
import busio
import board
from adafruit_epd.ssd1680 import Adafruit_SSD1680Z
from weather_graphics import Weather_Graphics

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)

display = Adafruit_SSD1680Z(
    122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy,
)
display.rotation = 1

gfx = Weather_Graphics(display, am_pm=True, celsius=False)

weather_data = {
    "weather": [{"id": 802, "main": "Clouds", "description": "scattered clouds", "icon": "03d"}],
    "main": {"temp": 294.26, "feels_like": 293.15, "temp_min": 292.04, "temp_max": 296.48, "pressure": 1013, "humidity": 41},
    "name": "American Fork",
    "sys": {"country": "US"},
}

gfx.display_weather(json.dumps(weather_data).encode("utf-8"))
print("Weather displayed!")
