"""
This module is part of the 'farben' package,
which is released under MIT license.
"""

from ..palette import Palette
from ..utils import rgb2hex


class NCS(Palette):
    """
    Holds Natural Colour System® utilities
    """

    # Identifier
    identifier = "ncs"

    # Dictionary holding fetched colors
    sets = {"ncs": []}

    # Copyright notices
    copyright_notices = {
        "xml": "\n    Natural Colour System® and related trademarks are the property of"
        + "\n    NCS Colour AB (https://ncscolour.com) \n  ",
        "gpl": "##\n# Natural Colour System® and related trademarks are the property of"
        + "\n# NCS Colour AB (https://ncscolour.com) \n##\n",
    }

    def fetch_colors(self) -> None:
        """
        Fetches Natural Colour System® colors

        Available sets:
          - 'base'

        :return: None
        """

        # One URL to rule them all
        base_url = "https://www.e-paint.co.uk/NCS-2050-index-colour-chart.asp"

        # Scrape Dulux® colors from HTML
        soup = self.get_html(base_url)

        for color_tile in soup.find("ul", {"class": "colour-charts"}).find_all("li"):
            color = {}
            color["code"] = color_tile.find("h2").text.strip()
            color["rgb"] = color_tile.find("img")["style"].split(":")[1]
            color["hex"] = rgb2hex(color["rgb"])
            color["name"] = ""

            self.sets["ncs"].append(color)

            print(f'Loading {color["code"]} in set "ncs" .. done')
