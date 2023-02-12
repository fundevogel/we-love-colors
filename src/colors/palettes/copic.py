import json
import os
from urllib.request import urlopen

from bs4 import BeautifulSoup

from .palette import Palette


class Copic(Palette):
    """
    Holds Copic® utilities
    """

    # Dictionary holding fetched colors
    sets = {"copic": []}

    # Identifier
    identifier = "copic"

    # Copyright notices
    copyright = {
        "xml": "\n    Copic® and related trademarks are the property of\n    Too Marker Corporation (https://www.toomarker.co.jp/en)\n  ",
        "gpl": "##\n# Copic® and related trademarks are the property of\n# Too Marker Corporation (https://www.toomarker.co.jp/en)\n##\n",
    }

    def __init__(self):
        super().__init__()

    ##
    # Fetches Copic® colors
    #
    # Valid `set_name` parameter:
    # - 'copic', currently 289 colors
    ##
    def fetch(self, set_name: str = "copic"):
        # One baseURL to rule them all
        base_url = "https://www.copicmarker.com/collections/collect"

        # Scraping Copic® colors from HTML
        html = urlopen(base_url)
        soup = BeautifulSoup(html, "lxml")

        for color_tile in soup.find(
            "div", {"class": "collection-color--desktop"}
        ).find_all("div", {"class": "product-item-hex"}):
            data_name = color_tile["data-name"]
            data_list = data_name.split(" ")

            hexadecimal = color_tile["style"][12:-8]
            rgb_list = tuple(
                int(hexadecimal.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)
            )
            rgb = [str(i) for i in rgb_list]

            color = {}
            color["code"] = data_list.pop(0)
            color["rgb"] = "rgb(" + ",".join(rgb) + ")"
            color["hex"] = hexadecimal.upper()
            color["name"] = " ".join(data_list)

            self.sets[set_name].append(color)

            print("Loading " + color["code"] + ' in set "' + set_name + '" .. done')
