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

OPEN_WEATHER_TOKEN = ""
LOCATION = "Manhattan, US"
DATA_SOURCE_URL = "https://api.openweathermap.org/data/2.5/weather"

if len(OPEN_WEATHER_TOKEN) == 0:
    raise RuntimeError(
        "You need to set your token first. Register at https://home.openweathermap.org/users/sign_up"
    )

params = {"q": LOCATION, "appid": OPEN_WEATHER_TOKEN}
data_source = DATA_SOURCE_URL + "?" + urllib.parse.urlencode(params)

display = Adafruit_SSD1680Z(
    122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy,
)

display.rotation = 1

gfx = Weather_Graphics(display, am_pm=True, celsius=False)
weather_refresh = None

while True:
    if (not weather_refresh) or (time.monotonic() - weather_refresh) > 600:
        try:
            response = urllib.request.urlopen(data_source)
            if response.getcode() == 200:
                value = response.read()
                print("Response is", value)
                gfx.display_weather(value)
                weather_refresh = time.monotonic()
            else:
                print(f"Unable to retrieve data: HTTP {response.getcode()}")
        except Exception as e:
            print(f"Error fetching weather: {e}")

    gfx.update_time()
    time.sleep(300)
