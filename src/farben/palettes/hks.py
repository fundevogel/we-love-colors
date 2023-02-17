"""
This module is part of the 'farben' package,
which is released under MIT license.
"""

from ..palette import Palette
from ..utils import hex2rgb


class HKS(Palette):
    """
    Holds HKS® utilities
    """

    # Identifier
    identifier = "hks"

    # Dictionary holding fetched colors
    sets = {"hks": []}

    # Copyright notices
    copyright_notices = {
        "xml": "\n    HKS® and related trademarks are the property of"
        + "\n    HKS Warenzeichenverband e.V (https://www.hks-farben.de) \n  ",
        "gpl": "##\n# HKS® and related trademarks are the property of"
        + "\n# HKS Warenzeichenverband e.V (https://www.hks-farben.de) \n##\n",
    }

    def fetch_all(self) -> None:
        """
        Fetches HKS® colors

        Available sets:
          - 'base'

        :return: None
        """

        # One URL to rule them all
        base_url = "https://www.kern.de/hks-farbtabelle"

        # Scrape Dulux® colors from HTML
        soup = self.get_html(base_url)

        for color_tile in soup.find_all("td", {"class": "ral"}):
            hexa = color_tile["bgcolor"]

            color = {}
            color["code"] = color_tile.text.strip()
            color["rgb"] = f"rgb({hex2rgb(hexa)})"
            color["hex"] = hexa.upper()
            color["name"] = ""

            self.sets["hks"].append(color)

            print(f'Loading {color["code"]} in set "hks" .. done')
