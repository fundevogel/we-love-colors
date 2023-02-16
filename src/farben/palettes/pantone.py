"""
This module is part of the 'farben' package,
which is released under MIT license.
"""

from typing import Dict, List, Optional

from ..palette import Palette
from ..utils import natural_sort


class Pantone(Palette):
    """
    Holds PANTONE® utilities
    """

    # Identifier
    identifier = "pantone"

    # Dictionary holding fetched colors (raw)
    sets = {
        "graphic-design": [],
        "fashion-design": [],
        "product-design": [],
    }

    # Copyright notices
    copyright_notices = {
        "xml": "\n    PANTONE® and related trademarks are the property of\n    "
        + "Pantone LLC (https://www.pantone.com), a division of X-Rite, "
        + "a Danaher company\n  ",
        "gpl": "##\n# PANTONE® and related trademarks are the property of\n"
        + "# Pantone LLC (https://www.pantone.com), a division of X-Rite, "
        + "a Danaher company\n##\n",
    }

    def fetch_colors(self) -> None:
        """
        Fetches all PANTONE® colors at once

        Available sets:
          - 'graphic-design' (currently 15870 colors), pp 1-32
          - 'fashion-design' (currently 2443 colors), pp 1-14
          - 'product-design' (currently 4967 colors), pp 1-10

        :return: None
        """

        self.fetch("graphic-design", 1, 32)
        self.fetch("fashion-design", 1, 14)
        self.fetch("product-design", 1, 10)

    def fetch(self, set_name: str, first_page: int, last_page: int) -> None:
        """
        Fetches PANTONE® colors

        :param set_name: str Name of color set
        :param first_page: int Number of first page
        :param last_page: int Number of last page
        :return: None
        """

        # One URL to rule them all
        base_url = "https://www.numerosamente.it/pantone-list"

        # Map base color sets to their corresponding URL parts
        set_url = {
            "graphic-design": "graphic-designers",
            "fashion-design": "fashion-and-interior-designers",
            "product-design": "industrial-designers",
        }

        # Looping through URLs & Scrape color information from HTML tables
        for i in range(first_page, last_page + 1):
            soup = self.get_html(f"{base_url}/{set_url[set_name]}/{i}")

            print(f"Loading page {i} .. done")

            for remote_element in soup.findAll("tr")[1:]:
                color = {}
                color["code"] = remote_element.findAll("td")[0].text
                color["rgb"] = remote_element.findAll("td")[1].text
                color["hex"] = remote_element.findAll("td")[2].text
                color["name"] = remote_element.findAll("td")[3].text

                # Checking if a fetched element already exists ..
                found_same_name = False

                for local_element in self.sets[set_name]:
                    if color["name"] and color["name"] == local_element["name"]:
                        found_same_name = True

                # .. if not, adding it is da real MVP
                if not found_same_name:
                    self.sets[set_name].append(color)

                print(f'Loading {color["code"]} in set "{set_name}" .. done')

    def extract_subsets(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Extracts color subsets

        :return: None
        """

        # Dictionary holding fetched colors (processed)
        data = {
            ##
            # Pantone Color Systems - Graphics
            # Pantone Matching System - PMS
            # For more information, see https://www.pantone.com/color-systems/for-graphic-design
            # or visit their shop: https://www.pantone.com/graphics
            ##
            "graphic-design": {
                # NOTE: Solid/Spot Colors (Coated & Uncoated) - Link?
                "C": [],
                "U": [],
                ##
                # CMYK Color Guide (Coated & Uncoated)
                # https://www.pantone.com/products/graphics/cmyk-coated-uncoated
                ##
                "PC": [],
                "PU": [],
                ##
                # Color Bridge Set (Coated & Uncoated)
                # https://www.pantone.com/products/graphics/color-bridge-coated-uncoated
                ##
                "CP": [],  # https://www.pantone.com/products/graphics/color-bridge-coated
                "UP": [],  # https://www.pantone.com/products/graphics/color-bridge-uncoated
                ##
                # Extended Gamut Coated Guide
                # https://www.pantone.com/products/graphics/extended-gamut-coated-guide
                ##
                "XGC": [],
                ##
                # Pastels & Neons (Coated & Uncoated)
                # https://www.pantone.com/products/graphics/pastels-neons
                ##
                # Neons
                "NC": [],
                "NU": [],
                # Pastels
                "PAC": [],
                "PAU": [],
                ##
                # Metallics (Coated)
                # https://www.pantone.com/products/graphics/metallics-guide
                ##
                "MC": [],
            },
            ##
            # Pantone Color Systems - Fashion
            # Fashion, Home + Interiors - FHI
            # For more information, see https://www.pantone.com/color-systems/for-fashion-design
            # or visit their shop: https://www.pantone.com/fashion-home-interiors
            ##
            "fashion-design": {
                # NOTE: 'Textile Paper eXtended'
                "TPX": [],
                # NOTE: 'Textile Paper Green'
                "TPG": [],
                # NOTE: 'Textile Cotton eXtended'
                "TCX": [],
                ##
                # Nylon Brights Set
                # https://www.pantone.com/products/fashion-home-interiors/nylon-brights-set
                ##
                "TN": [],
                ##
                # Pantone SkinTone™ Guide
                # https://www.pantone.com/products/fashion-home-interiors/pantone-skintone-guide
                ##
                "SP": [],
            },
            ##
            # Pantone Color Systems - Product
            # Plastic Standards
            # For more information, see https://www.pantone.com/color-systems/for-product-design
            # or visit the shop: https://www.pantone.com/plastics
            ##
            "product-design": {
                "PQ": [],  # https://www.pantone.com/color-intelligence/articles/technical/did-you-know-pantone-plastics-standards-explained
                # NOTE: 'Textile Cotton eXtended'
                "TCX": [],
            },
            "custom-palettes": {
                "color-of-the-year": []
                # IDEA: Palettes created around CotY
            },
        }

        # Lists holding base pastels
        base_pastels = [
            "Yellow 0131",
            "Red 0331",
            "Magenta 0521",
            "Violet 0631",
            "Blue 0821",
            "Green 0921",
            "Black 0961",
        ]
        base_pastels_coated = [color + " C" for color in base_pastels]
        base_pastels_uncoated = [color + " U" for color in base_pastels]

        ##
        # List holding codes for PANTONE®'s 'Color of the Year' (CotY) since 2000
        # https://www.pantone.com/color-intelligence/color-of-the-year/color-of-the-year-2019
        ##
        colors_of_the_year = [
            "15-4020",  # 2000: Cerulean Blue
            "17-2031",  # 2001: Fuchsia Rose
            "19-1664",  # 2002: True Red
            "14-4811",  # 2003: Aqua Sky
            "17-1456",  # 2004: Tigerlily
            "15-5217",  # 2005: Blue Turquoise
            "13-1106",  # 2006: Sand Dollar
            "19-1557",  # 2007: Chili Pepper
            "18-3943",  # 2008: Blue Iris
            "14-0848",  # 2009: Mimosa
            "15-5519",  # 2010: Turquoise
            "18-2120",  # 2011: Honeysuckle
            "17-1463",  # 2012: Tangerine Tango
            "17-5641",  # 2013: Emerald
            "18-3224",  # 2014: Radiant Orchid
            "18-1438",  # 2015: Marsala
            "15-3919",  # 2016: Serenity
            "13-1520",  # 2016: Rose Quartz
            "15-0343",  # 2017: Greenery
            "18-3838",  # 2018: Ultra Violet
            "16-1546",  # 2019: Living Coral
        ]

        # # Build path to JSON file
        # data_file = self.brand_path / f"{self.identifier}.json"

        # with data_file.open("r", encoding="utf-8") as file:
        #     data = json.load(file)

        # Looping through PANTONE® color sets
        for set_name, colors in self.sets.items():
            subset = data[set_name]

            # Extract each PANTONE® color subset
            for color in colors:
                code = color["code"]

                if code[0:7] in colors_of_the_year:
                    code = code[0:7]
                    color["year"] = 2000 + colors_of_the_year.index(code)
                    data["custom-palettes"]["color-of-the-year"].append(color)

                if code[0:2] == "P ":
                    if code[-2:] == " C":
                        subset["PC"].append(color)

                    if code[-2:] == " U":
                        subset["PU"].append(color)

                else:
                    if code[-2:] == " C":
                        if len(code) == 5:
                            if ("801 C" <= code <= "814 C") or (
                                "901 C" <= code <= "942 C"
                            ):
                                subset["NC"].append(color)
                                continue

                            if "871 C" <= code <= "877 C":
                                subset["MC"].append(color)
                                continue

                        if len(code) == 6:
                            if "8001 C" <= code <= "8965 C":
                                subset["MC"].append(color)
                                continue

                            if ("9020 C" <= code <= "9603 C") or (
                                code in base_pastels_coated
                            ):
                                subset["PAC"].append(color)
                                continue

                        if len(code) == 7 and ("10101 C" <= code <= "10399 C"):
                            subset["MC"].append(color)
                            continue

                        subset["C"].append(color)

                    if code[-2:] == " U":
                        if len(code) == 5:
                            if ("801 U" <= code <= "814 U") or (
                                "901 U" <= code <= "942 U"
                            ):
                                subset["NU"].append(color)
                                continue

                            if "871 U" <= code <= "877 U":
                                # NOTE: There are no uncoated Metallics, deleting rather than skipping?
                                continue

                        if (len(code) == 6 and ("9020 U" <= code <= "9603 U")) or (
                            code in base_pastels_uncoated
                        ):
                            subset["PAU"].append(color)
                            continue

                        subset["U"].append(color)

                if code[-3:] == " CP":
                    subset["CP"].append(color)

                if code[-3:] == " UP":
                    subset["UP"].append(color)

                if code[-3:] == "XGC":
                    subset["XGC"].append(color)

                if code[-3:] == "TCX":
                    subset["TCX"].append(color)

                if code[-3:] == "TPG":
                    subset["TPG"].append(color)

                if code[-3:] == "TPX":
                    subset["TPX"].append(color)

                if code[-3:] == " TN":
                    subset["TN"].append(color)

                if code[-3:] == " SP":
                    subset["SP"].append(color)

                if code[0:3] == "PQ-":
                    subset["PQ"].append(color)

        return data

    def make_palettes(self, palette: Optional[str]) -> None:
        """
        Makes color palettes for one or all palette types

        :param palette: str | None
        :return: None
        """

        # Act normal, be cool
        super().make_palettes(palette)

        # Iterate over color sets
        for set_name, subsets in self.extract_subsets().items():
            # Build & create path to color subsets
            subsets_path = self.brand_path / "sets" / set_name
            subsets_path.mkdir(parents=True, exist_ok=True)

            for dtype in ["acb", "gpl", "soc", "xml"]:
                if palette is not None and dtype is not palette:
                    continue

                # Iterate over color subsets
                for subset_name, colors in subsets.items():
                    # Apply natural sort order to all PANTONE® 'Graphics' colors
                    if set_name == "graphic-design":
                        natural_sort(colors, "code")

                    if set_name == "custom-palettes":
                        subset_name = "CotY"
                        colors.sort(key=lambda k: k["year"])

                    # Build path to palette file
                    palette_file = subsets_path / f"{subset_name}.{dtype}"

                    # Party time!
                    getattr(self, f"make_{dtype}")(palette_file, colors)
