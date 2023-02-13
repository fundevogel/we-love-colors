"""
This module is part of the 'we-love-colors' package,
which is released under MIT license.
"""

from ..palette import Palette
from ..utils import rgb2hex


class Prismacolor(Palette):
    """
    Holds Prismacolor® utilities
    """

    # Identifier
    identifier = "prismacolor"

    # Dictionary holding fetched colors
    sets = {"premier": []}

    # Copyright notices
    copyright_notices = {
        "xml": "\n    Prismacolor® and related trademarks are the property of\n    "
        + "Berol Corporation (http://www.berol.co.uk), "
        + "owned by Sanford L.P. (http://www.sanfordb2b.com),\n    "
        + "a Newell Brands (https://www.newellbrands.com) company\n  ",
        "gpl": "##\n# Prismacolor® and related trademarks are the property of\n"
        + "# Berol Corporation (http://www.berol.co.uk), "
        + "owned by Sanford L.P. (http://www.sanfordb2b.com),\n"
        + "# a Newell Brands (https://www.newellbrands.com) company\n##\n",
    }

    def fetch_colors(self) -> None:
        """
        Fetches Prismacolor® colors

        Available sets:
          - 'premier' (currently 150 colors)

        :param set_name: str Name of color set
        :return: None
        """

        # One URL to rule them all
        base_url = (
            "https://kredki.eu/pl/p/Prismacolor-Colored-Pencils-Kredki-Art-150-Kol/75"
        )

        # Scraping Prismacolor® colors from HTML
        soup = self.get_html(base_url)

        for list_element in soup.find("div", {"class": "resetcss"}).findAll("li")[1:]:
            # Create data array
            color = {}

            if not list_element.text[0:2] == "PC":
                continue

            line = list_element.text.split(":")
            data = line[0][0:-4].split(" ")
            rgb_string = line[1][:-4].replace(" ", "")

            color["code"] = " ".join([data.pop(0), data.pop(0)])
            color["rgb"] = "rgb(" + rgb_string + ")"
            color["hex"] = rgb2hex(rgb_string)
            color["name"] = " ".join(data)

            self.sets["premier"].append(color)

            print(f'Loading {color["code"]} in set "premier" .. done')
