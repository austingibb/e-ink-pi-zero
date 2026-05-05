from datetime import datetime, timezone, timedelta
import json
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.epd import Adafruit_EPD

small_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16
)
medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
large_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24
)

import os
_base = os.path.dirname(os.path.abspath(__file__))
icon_font = ImageFont.truetype(os.path.join(_base, "meteocons.ttf"), 48)

ICON_MAP = {
    "01d": "B",
    "01n": "C",
    "02d": "H",
    "02n": "I",
    "03d": "N",
    "03n": "N",
    "04d": "Y",
    "04n": "Y",
    "09d": "Q",
    "09n": "Q",
    "10d": "R",
    "10n": "R",
    "11d": "Z",
    "11n": "Z",
    "13d": "W",
    "13n": "W",
    "50d": "J",
    "50n": "K",
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Weather_Graphics:
    def __init__(self, display, *, am_pm=True, celsius=True):
        self.am_pm = am_pm
        self.celsius = celsius

        self.small_font = small_font
        self.medium_font = medium_font
        self.large_font = large_font

        self.display = display

        self._weather_icon = None
        self._city_name = None
        self._main_text = None
        self._temperature = None
        self._description = None
        self._time_text = None
        self._timezone_offset = 0

    def display_weather(self, weather):
        weather = json.loads(weather.decode("utf-8"))

        self._weather_icon = ICON_MAP[weather["weather"][0]["icon"]]

        city_name = weather["name"] + ", " + weather["sys"]["country"]
        print(city_name)
        self._city_name = city_name

        main = weather["weather"][0]["main"]
        print(main)
        self._main_text = main

        temperature = weather["main"]["temp"] - 273.15
        print(temperature)
        if self.celsius:
            self._temperature = "%d C" % temperature
        else:
            self._temperature = "%d F" % ((temperature * 9 / 5) + 32)

        description = weather["weather"][0]["description"]
        description = description[0].upper() + description[1:]
        print(description)
        self._description = description

        self._timezone_offset = weather.get("timezone", 0)

        self.update_time()

    def update_time(self):
        tz = timezone(timedelta(seconds=self._timezone_offset))
        now = datetime.now(tz)
        self._time_text = now.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")
        self.update_display()

    def update_display(self):
        self.display.fill(Adafruit_EPD.WHITE)
        image = Image.new("RGB", (self.display.width, self.display.height), color=WHITE)
        draw = ImageDraw.Draw(image)

        if self._weather_icon is not None:
            (font_width, font_height) = icon_font.getbbox(self._weather_icon)[2:4]
            draw.text(
                (
                    self.display.width // 2 - font_width // 2,
                    self.display.height // 2 - font_height // 2 - 5,
                ),
                self._weather_icon,
                font=icon_font,
                fill=BLACK,
            )

        if self._city_name is not None:
            draw.text(
                (5, 5), self._city_name, font=self.medium_font, fill=BLACK,
            )

        if self._time_text is not None:
            (font_width, font_height) = medium_font.getbbox(self._time_text)[2:4]
            draw.text(
                (5, font_height * 2 - 5),
                self._time_text,
                font=self.medium_font,
                fill=BLACK,
            )

        if self._main_text is not None:
            (font_width, font_height) = large_font.getbbox(self._main_text)[2:4]
            draw.text(
                (5, self.display.height - font_height * 2),
                self._main_text,
                font=self.large_font,
                fill=BLACK,
            )

        if self._description is not None:
            (font_width, font_height) = small_font.getbbox(self._description)[2:4]
            draw.text(
                (5, self.display.height - font_height - 5),
                self._description,
                font=self.small_font,
                fill=BLACK,
            )

        if self._temperature is not None:
            (font_width, font_height) = large_font.getbbox(self._temperature)[2:4]
            draw.text(
                (
                    self.display.width - font_width - 5,
                    self.display.height - font_height * 2,
                ),
                self._temperature,
                font=self.large_font,
                fill=BLACK,
            )

        self.display.image(image)
        self.display.display()
