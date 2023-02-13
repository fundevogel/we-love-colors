"""
This module is part of the 'we-love-colors' package,
which is released under MIT license.
"""

from ..palette import Palette
from ..utils import hex2rgb


class Copic(Palette):
    """
    Holds Copic® utilities
    """

    # Identifier
    identifier = "copic"

    # Dictionary holding fetched colors
    sets = {"copic": []}

    # Copyright notices
    copyright_notices = {
        "xml": "\n    Copic® and related trademarks are the property of\n    "
        + "Too Marker Corporation (https://www.toomarker.co.jp/en)\n  ",
        "gpl": "##\n# Copic® and related trademarks are the property of\n"
        + "# Too Marker Corporation (https://www.toomarker.co.jp/en)\n##\n",
    }

    def fetch_colors(self) -> None:
        """
        Fetches Copic® colors

        Available sets:
          - 'base' (currently 289 colors)

        :return: None
        """

        # One URL to rule them all
        base_url = "https://copic.de/copic-classic-farb/bestellraster"

        # Scraping Copic® colors from HTML
        soup = self.get_html(base_url)

        for color_tile in soup.find(
            "div", {"class": "collection-color--desktop"}
        ).find_all("div", {"class": "product-item-hex"}):
            data = color_tile["data-name"].split(" ")
            hexa = color_tile["style"][12:-8]

            color = {}
            color["code"] = data.pop(0)
            color["rgb"] = "rgb(" + hex2rgb(hexa) + ")"
            color["hex"] = hexa.upper()
            color["name"] = " ".join(data)

            self.sets["copic"].append(color)

            print(f'Loading {color["code"]} in set "copic" .. done')
