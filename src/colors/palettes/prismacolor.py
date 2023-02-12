import json
import os

from .palette import Palette


class Prismacolor(Palette):
    """
    Holds Prismacolor® utilities
    """

    # Dictionary holding fetched colors
    sets = {"premier": []}

    # Identifier
    identifier = "prismacolor"

    # Copyright notices
    copyright = {
        "xml": "\n    Prismacolor® and related trademarks are the property of\n    Berol Corporation (http://www.berol.co.uk), owned by Sanford L.P. (http://www.sanfordb2b.com),\n    a Newell Brands (https://www.newellbrands.com) company\n  ",
        "gpl": "##\n# Prismacolor® and related trademarks are the property of\n# Berol Corporation (http://www.berol.co.uk), owned by Sanford L.P. (http://www.sanfordb2b.com),\n# a Newell Brands (https://www.newellbrands.com) company\n##\n",
    }

    def __init__(self):
        super().__init__()

    ##
    # Fetches Prismacolor® colors
    #
    # Valid `set_name` parameter:
    # - 'premier', currently 150 colors
    ##
    def fetch(self, set_name: str = "premier"):
        # One baseURL to rule them all
        base_url = (
            "https://kredki.eu/pl/p/Prismacolor-Colored-Pencils-Kredki-Art-150-Kol/75"
        )

        # Scraping Prismacolor® colors from HTML
        soup = self.get_html(base_url)

        for list_element in soup.find("div", {"class": "resetcss"}).findAll("li")[1:]:
            color_list = []
            line = list_element.text

            color = {}

            if not line[0:2] == "PC":
                continue

            line = line.split(":")
            code_name = line[0][0:-4].split(" ")
            rgb_string = line[1][:-4].replace(", ", ",")
            rgb_list = rgb_string.split(",")
            rgb = [int(i) for i in rgb_list]

            # Converting to hexadecimal color code, see https://stackoverflow.com/a/3380739
            hexadecimal = "#%02x%02x%02x" % tuple(rgb)

            color["code"] = " ".join([code_name.pop(0), code_name.pop(0)])
            color["rgb"] = "rgb(" + rgb_string.strip() + ")"
            color["hex"] = hexadecimal.upper()
            color["name"] = " ".join(code_name)

            self.sets[set_name].append(color)

            print("Loading " + color["code"] + ' in set "' + set_name + '" .. done')
