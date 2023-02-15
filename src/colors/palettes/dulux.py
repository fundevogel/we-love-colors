"""
This module is part of the 'we-love-colors' package,
which is released under MIT license.
"""

from ..palette import Palette
from ..utils import rgb2hex


class Dulux(Palette):
    """
    Holds Dulux® utilities
    """

    # Identifier
    identifier = "dulux"

    # Dictionary holding fetched colors
    sets = {"dulux": []}

    # Copyright notices
    copyright_notices = {
        "xml": "\n    Dulux® and related trademarks are the property of"
        + "\n    AkzoNobel N.V. (https://www.akzonobel.com) or\n    "
        + "DuluxGroup (https://www.dulux.com.au) (Australia & New Zealand) \n  ",
        "gpl": "##\n# Dulux® and related trademarks are the property of"
        + "\n# AkzoNobel N.V. (https://www.akzonobel.com) or\n"
        + "# DuluxGroup (https://www.dulux.com.au) (Australia & New Zealand) \n##\n",
    }

    def fetch_colors(self) -> None:
        """
        Fetches Dulux® colors

        Available sets:
          - 'base' (currently 1768 colors)

        :return: None
        """

        # One URL to rule them all
        base_url = "https://colour.dulux.ca/all-colors"

        # Scrape Dulux® colors from HTML
        soup = self.get_html(base_url)

        for color_tile in soup.find_all("a", {"class": "all-color-tile"}):
            color = {}
            color["code"] = color_tile.find(
                attrs={"class": "color-number"}
            ).text.strip()
            color["rgb"] = color_tile.get("style")[17:].replace(" ", "")
            color["hex"] = rgb2hex(color["rgb"])
            color["name"] = color_tile.find(attrs={"class": "color-name"}).text.strip()

            self.sets["dulux"].append(color)

            print(f'Loading {color["code"]} in set "dulux" .. done')
