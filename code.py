import os
import time
import urllib.request
import urllib.parse
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

btn_a = digitalio.DigitalInOut(board.D5)
btn_a.switch_to_input(pull=digitalio.Pull.UP)
btn_b = digitalio.DigitalInOut(board.D6)
btn_b.switch_to_input(pull=digitalio.Pull.UP)

OPEN_WEATHER_TOKEN = os.environ["OPEN_WEATHER_TOKEN"]
DATA_SOURCE_URL = "https://api.openweathermap.org/data/2.5/weather"

LOCATIONS = ["American Fork, US", "Seattle, US"]
location_index = 0

if not OPEN_WEATHER_TOKEN:
    raise RuntimeError(
        "OPEN_WEATHER_TOKEN is not set. Register at https://home.openweathermap.org/users/sign_up"
    )

def build_url(location):
    params = {"q": location, "appid": OPEN_WEATHER_TOKEN}
    return DATA_SOURCE_URL + "?" + urllib.parse.urlencode(params)

def fetch_weather(location):
    url = build_url(location)
    try:
        response = urllib.request.urlopen(url)
        if response.getcode() == 200:
            value = response.read()
            print(f"[{location}] OK")
            return value
        else:
            print(f"[{location}] HTTP {response.getcode()}")
    except Exception as e:
        print(f"[{location}] Error: {e}")
    return None

display = Adafruit_SSD1680Z(
    122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy,
)
display.rotation = 1

gfx = Weather_Graphics(display, am_pm=True, celsius=False)
weather_refresh = time.monotonic()
last_display_update = 0
weather_loaded = False

gfx.update_time()

while True:
    now = time.monotonic()

    if (not weather_loaded) or (now - weather_refresh) > 10:
        data = fetch_weather(LOCATIONS[location_index])
        if data:
            gfx.display_weather(data)
            weather_loaded = True
            last_display_update = now
        weather_refresh = now

    if weather_loaded and (now - last_display_update) > 300:
        gfx.update_time()
        last_display_update = now

    if not btn_a.value:
        location_index = (location_index + 1) % len(LOCATIONS)
        print(f"Location: {LOCATIONS[location_index]}")
        weather_loaded = False
        time.sleep(0.3)

    if not btn_b.value:
        location_index = (location_index - 1) % len(LOCATIONS)
        print(f"Location: {LOCATIONS[location_index]}")
        weather_loaded = False
        time.sleep(0.3)

    time.sleep(0.1)
