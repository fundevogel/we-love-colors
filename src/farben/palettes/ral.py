"""
This module is part of the 'farben' package,
which is released under MIT license.
"""

from urllib.request import urlopen

from PIL import ImageFile

from ..palette import Palette
from ..utils import rgb2hex


class RAL(Palette):
    """
    Holds RAL® utilities
    """

    # Identifier
    identifier = "ral"

    # Dictionary holding fetched colors
    sets = {
        "classic": [],
        "design": [],
        "effect": [],
        "plastics-p1": [],
        "plastics-p2": [],
        # IDEA: Merging them together?
        # 'plastics' {
        #   'p1': [],
        #   'p2': [],
        # }
    }

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

    def fetch_colors(self) -> None:
        """
        Fetches all RAL® colors at once

        :return: None
        """

        self.fetch("classic")
        self.fetch("design")
        self.fetch("effect")
        self.fetch("plastics")

    def fetch(self, set_name: str) -> None:
        """
        Fetches RAL® colors

        Available sets:
          - 'classic'
          - 'design'
          - 'effect'
          - 'plastics

        :param set_name: str Name of color set
        :return: None
        """

        # One URL to rule them all
        base_url = (
            "https://www.ral-farben.de/content/anwendung-hilfe/"
            + f"all-ral-colours-names/overview-ral-{set_name}-colours.html"
        )

        # Scrape RAL® colors from HTML
        soup = self.get_html(base_url)
        color_grids = soup.find_all("ul", {"class": "color-grid"})

        for index, color_grid in enumerate(color_grids, 1):
            list_elements = color_grid.findAll("li")

            for idx, list_element in enumerate(list_elements, 1):
                list_element = list_element.text.splitlines()

                # Parsing each RAL® color's background image, extracting RGB values
                slug = {"design": "designplus", "effect": "ral-effect"}

                identifier = slug.get(set_name) if (set_name in slug) else set_name

                if set_name == "plastics":
                    identifier = set_name + "-p" + str(index)

                # See https://stackoverflow.com/a/2271015
                image_url = (
                    "https://www.ral-farben.de/out/ralfarben/img/thumbs/"
                    + f"{identifier}-{idx}.png"
                )
                image = urlopen(image_url)
                parser = ImageFile.Parser()

                while True:
                    chunk = image.read(1024)

                    if not chunk:
                        break

                    parser.feed(chunk)

                image = parser.close()
                rgb_values = [str(i) for i in image.getpixel((0, 0))]

                color = {}
                color["code"] = list_element[1].strip()
                color["rgb"] = "rgb(" + ",".join(rgb_values) + ")"
                color["hex"] = rgb2hex(rgb_values)
                color["name"] = ""

                if len(list_element) > 2:
                    color["name"] = (
                        list_element[2] if len(list_element) == 3 else list_element[3]
                    )

                if not set_name == "plastics":
                    self.sets[set_name].append(color)
                else:
                    self.sets[identifier].append(color)

                print(f'Loading {color["code"]} in set "{set_name}" .. done')
