"""
This module is part of the 'farben' package,
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
        base_url = "https://swatchtool.com/data_prismacolor.json"

        # Load Prismacolor® colors as JSON
        data = self.get_json(base_url)

        for item in data:
            # Create data array
            color = {}

            color["code"] = f'PC {item["id"]}'
            color["rgb"] = f'rgb({item["rgb"]})'
            color["hex"] = rgb2hex(item["rgb"])
            color["name"] = item["name"]

            self.sets["premier"].append(color)

            print(f'Loading {color["code"]} in set "premier" .. done')
