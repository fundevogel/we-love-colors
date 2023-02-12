import json
import os

from .palette import Palette


class Dulux(Palette):
    """
    Holds Dulux® utilities
    """

    # Dictionary holding fetched colors
    sets = {"dulux": []}

    # Identifier
    identifier = "dulux"

    # Copyright notices
    copyright = {
        "xml": "\n    Dulux® and related trademarks are the property of\n    AkzoNobel N.V. (https://www.akzonobel.com) (joint-stock company) (worldwide) or\n    DuluxGroup (https://www.dulux.com.au) (Australia & New Zealand) \n  ",
        "gpl": "##\n# Dulux® and related trademarks are the property of\n# AkzoNobel N.V. (https://www.akzonobel.com) (joint-stock company) (worldwide) or\n# DuluxGroup (https://www.dulux.com.au) (Australia & New Zealand) \n##\n",
    }

    def __init__(self):
        super().__init__()

    ##
    # Fetches Dulux® colors
    # Valid `set_name` parameter:
    # - 'dulux', currently 1768 colors
    ##
    def fetch(self, set_name: str = "dulux"):
        # One baseURL to rule them all
        base_url = "https://colour.dulux.ca/all-colors"

        # Scraping Dulux® colors from HTML
        soup = self.get_html(base_url)

        for color_tile in soup.find_all("a", {"class": "all-color-tile"}):
            rgb_string = color_tile.get("style")[17:].replace(", ", ",")
            rgb_list = rgb_string[4:-1].split(",")
            rgb = [int(i) for i in rgb_list]

            color = {}
            color["code"] = color_tile.find(attrs={"class": "color-number"}).text
            color["rgb"] = rgb_string
            color["hex"] = "#%02x%02x%02x" % tuple(
                rgb
            )  # Converting to hexadecimal color code, see https://stackoverflow.com/a/3380739
            color["name"] = color_tile.find(attrs={"class": "color-name"}).text

            for i, entry in color.items():
                color[i] = entry.strip()

            self.sets[set_name].append(color)

            print("Loading " + color["code"] + ' in set "' + set_name + '" .. done')
