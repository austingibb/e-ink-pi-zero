import time
import digitalio
import busio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.ssd1680 import Adafruit_SSD1680Z
from adafruit_epd.epd import Adafruit_EPD

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)

display = Adafruit_SSD1680Z(
    122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy,
)
display.rotation = 1

print(f"Display: {display.width}x{display.height}")

display.fill(Adafruit_EPD.WHITE)
image = Image.new("RGB", (display.width, display.height), color=(255, 255, 255))
draw = ImageDraw.Draw(image)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
draw.text((10, 10), "Hello E-Ink!", font=font, fill=(0, 0, 0))

display.image(image)
display.display()
print("Display updated!")
