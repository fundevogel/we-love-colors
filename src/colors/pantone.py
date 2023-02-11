#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# Imports
# For more information, see https://www.python.org/dev/peps/pep-0008/#imports
##

import json
import os
from urllib.request import urlopen

from bs4 import BeautifulSoup

from .helpers.nat_sort import natural_sort
from .palette import Palette


class Pantone(Palette):
    # Dictionary holding fetched colors (raw)
    sets = {
        "graphic-design": [],
        "fashion-design": [],
        "product-design": [],
    }

    # Identifier
    identifier = "pantone"

    # Copyright notices
    copyright = {
        "xml": "\n    PANTONE® and related trademarks are the property of\n    Pantone LLC (https://www.pantone.com), a division of X-Rite, a Danaher company\n  ",
        "gpl": "##\n# PANTONE® and related trademarks are the property of\n# Pantone LLC (https://www.pantone.com), a division of X-Rite, a Danaher company\n##\n",
    }

    def __init__(self):
        super().__init__()

    ##
    # Fetches PANTONE® colors
    #
    # Valid `set_name` parameter:
    # - 'graphic-design', currently 15870 colors (pp 1-32)
    # - 'fashion-design', currently 2443 colors (pp 1-14)
    # - 'product-design', currently 4967 colors (pp 1-10)
    ##
    def fetch(self, set_name, firstPage, lastPage):
        # One baseURL to rule them all
        base_url = "https://www.numerosamente.it/pantone-list/"

        # Translating set_name to valid URL path name via `dict.get()`
        set_url = {
            "graphic-design": "graphic-designers/",
            "fashion-design": "fashion-and-interior-designers/",
            "product-design": "industrial-designers/",
        }

        # Looping through URLs & scraping color information from HTML tables
        for i in range(firstPage, lastPage + 1):
            html = urlopen(base_url + set_url.get(set_name) + str(i))
            soup = BeautifulSoup(html, "lxml")

            print("Loading page " + str(i) + " .. done")

            for remoteElement in soup.findAll("tr")[1:]:
                color = {}
                color["code"] = remoteElement.findAll("td")[0].text
                color["rgb"] = remoteElement.findAll("td")[1].text
                color["hex"] = remoteElement.findAll("td")[2].text
                color["name"] = remoteElement.findAll("td")[3].text

                # Checking if a fetched element already exists ..
                found_same_name = False
                for localElement in self.sets[set_name]:
                    if color["name"] != "" and color["name"] == localElement["name"]:
                        found_same_name = True

                # .. if not, adding it is da real MVP
                if not found_same_name:
                    self.sets[set_name].append(color)

                print("Loading " + color["code"] + ' in set "' + set_name + '" .. done')

    ##
    # Fetches all PANTONE® colors at once
    ##
    def fetch_all(self):
        self.fetch("graphic-design", 1, 32)
        self.fetch("fashion-design", 1, 14)
        self.fetch("product-design", 1, 10)

    ##
    # Creates JSON files for Dulux® color sets
    ##
    def create_json(self, input_filename=""):
        if input_filename == "":
            input_filename = self.identifier

        # Dictionary holding fetched colors (processed)
        sets_processed = {
            ##
            # Pantone Color Systems - Graphics
            # Pantone Matching System - PMS
            # For more information, see https://www.pantone.com/color-systems/for-graphic-design
            # or visit their shop: https://www.pantone.com/graphics
            ##
            "graphic-design": {
                # TODO: Solid/Spot Colors (Coated & Uncoated) - Link?
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
                # TODO: 'Textile Paper eXtended'
                "TPX": [],
                # TODO: 'Textile Paper Green'
                "TPG": [],
                # TODO: 'Textile Cotton eXtended'
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
                # TODO: 'Textile Cotton eXtended'
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

        with open(self.json_path + "/" + input_filename + ".json", "r") as file:
            data = json.load(file)

        # Looping through PANTONE® color sets
        for set, colors in data.items():
            subset = sets_processed[set]

            # Extracting each PANTONE® color subset
            for i, color in enumerate(colors):
                code = color["code"]

                if code[0:7] in colors_of_the_year:
                    code = code[0:7]
                    color["year"] = 2000 + colors_of_the_year.index(code)
                    sets_processed["custom-palettes"]["color-of-the-year"].append(color)

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
                                # TODO: There are no uncoated Metallics, deleting rather than skipping?
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

        for set, subsets in sets_processed.items():
            if len(subsets) == 0:
                break

            # Creating subdirectories
            file_path = self.json_path + "/" + set
            os.makedirs(file_path, exist_ok=True)

            for subset, colors in subsets.items():
                # Applying natural sort order to all PANTONE® 'Graphics' colors
                if set == "graphic-design":
                    natural_sort(colors, "code")
                if set == "custom-palettes":
                    colors.sort(key=lambda k: k["year"])

                if subset == "color-of-the-year":
                    subset = "CotY"

                json_path = (
                    file_path + "/" + subset + "_" + str(len(colors)) + "-colors.json"
                )

                # Dumping Pantone® color sets
                with open(json_path, "w") as file:
                    file.write(json.dumps(colors, indent=4))

                print("Generating %s .. done" % json_path)
