"""
This module is part of the 'farben' package,
which is released under MIT license.
"""

import re

from ..palette import Palette
from ..utils import hex2rgb


class RAL(Palette):
    """
    Holds RAL® utilities
    """

    # Identifier
    identifier = "ral"

    # Dictionary holding fetched colors
    sets = {"ral": []}

    # Copyright notices
    copyright_notices = {
        "xml": "\n    RAL® and related trademarks are the property of"
        + "\n    RAL gGmbH (https://www.ral-farben.de) (non-profit LLC) or"
        + "\n    RAL Deutsches Institut für Gütesicherung und Kennzeichnung "
        + "e. V. (https://www.ral.de)\n  ",
        "gpl": "##\n# RAL® and related trademarks are the property of"
        + "\n# RAL gGmbH (https://www.ral-farben.de) (non-profit LLC) or\n"
        + "# RAL Deutsches Institut für Gütesicherung und Kennzeichnung "
        + "e. V. (https://www.ral.de)\n##\n",
    }

    def fetch_all(self) -> None:
        """
        Fetches all RAL® colors at once

        :return: None
        """

        # One URL to rule them all
        base_url = "https://www.ral-farben.de/alle-ral-farben"

        # Scrape RAL® colors from HTML
        soup = self.get_html(base_url)

        for color_tile in soup.find_all("a", {"class": "farbe"}):
            code = color_tile.find("span", {"class": "number"}).text
            hexa = color_tile["style"].split(":")[1]

            color = {}
            color["code"] = f'{color_tile.find("span").text} {code}'
            color["rgb"] = f"rgb({hex2rgb(hexa)})"
            color["hex"] = hexa.upper()
            color["name"] = ""

            if subtext := color_tile.find("div", {"class": "subtext"}):
                color["name"] = re.split("\n", subtext.get_text(separator="\n"))[1]

            self.sets["ral"].append(color)

            print(f'Loading {color["code"]} in set "ral" .. done')
