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
    sets = {
        "classic": [],
        "sketch": [],
        "ciao": [],
    }

    # Copyright notices
    copyright_notices = {
        "xml": "\n    Copic® and related trademarks are the property of\n    "
        + "Too Marker Corporation (https://www.toomarker.co.jp/en)\n  ",
        "gpl": "##\n# Copic® and related trademarks are the property of\n"
        + "# Too Marker Corporation (https://www.toomarker.co.jp/en)\n##\n",
    }

    def fetch_colors(self) -> None:
        """
        Fetches all Copic® colors at once

        Available sets:
          - 'classic' (currently 289 colors)
          - 'sketch'
          - 'ciao'

        :return: None
        """

        self.fetch("classic")
        self.fetch("sketch")
        self.fetch("ciao")

    def fetch(self, set_name: str) -> None:
        """
        Fetches Copic® colors

        :param set_name: str Name of color set
        :return: None
        """

        # One URL to rule them all
        base_url = f"https://copic.de/copic-{set_name}-farb/bestellraster"

        # Scrape Copic® colors from HTML
        soup = self.get_html(base_url)

        for color_block in soup.find_all("div", {"class": "copic-colors__color-block"}):
            hexa = color_block.find("div", {"class": "copic-colors__cap"})[
                "style"
            ].split()[1]
            name = color_block.find("div", {"class": "copic-colors__color-name"})

            color = {}
            color["code"] = color_block.find("strong").text
            color["rgb"] = f"rgb({hex2rgb(hexa)})"
            color["hex"] = hexa.upper()
            color["name"] = name.text

            self.sets[set_name].append(color)

            print(f'Loading {color["code"]} in set "{set_name}" .. done')
