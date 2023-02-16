"""
This module is part of the 'farben' package,
which is released under MIT license.
"""

import json
import pathlib
import random
from typing import Dict, List, Optional

import bs4
from lxml import etree
import requests


class Palette:
    """
    Holds basic palette utilities
    """

    # Copyright notice for various file formats
    copyright_notices: Dict[str, str]

    # Identifier
    identifier: str

    # Color sets
    sets: dict

    # UA strings
    ua: List[str] = [
        # Firefox
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
        + "/51.0.2704.103 Safari/537.36",
        # Opera
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
        + "/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
        # Safari
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15"
        + " (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
        # Internet Explorer
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobil"
        + "e/9.0)",
        # Google
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    ]

    def __init__(self) -> None:
        """
        Constructor

        :return: None
        """

        # Copyright notices
        self.default_copyright_notices = {
            "xml": "\n    For copyright and other legal information,\n    "
            + 'please refer to "README.md" in the root of this project\n  ',
            "gpl": "##\n# For copyright and other legal information, "
            + 'please refer to "README.md" in the root of this project\n##\n',
        }

        # Create path for brand colors
        self.brand_path = pathlib.Path.cwd() / "palettes" / self.identifier
        self.brand_path.mkdir(parents=True, exist_ok=True)

    def get(self, url: str) -> requests.Response:
        """
        Sends 'GET' request

        :param url: str Target URL
        :return: requests.Response HTTP response
        """

        # Open HTTP session
        with requests.Session() as session:
            # Set headers (using random UA)
            session.headers = {"User-Agent": random.choice(self.ua)}

            # .. fetch URL contents
            response = session.get(url, timeout=10)

            # Unless status code indicates problem ..
            response.raise_for_status()

            # .. provide HTTP response
            return response

    def get_html(self, url: str) -> bs4.BeautifulSoup:
        """
        Fetches HTML for given URL

        :param url: str Target URL
        :return: bs4.BeautifulSoup Source HTML
        """

        # Attempt to ..
        try:
            # .. fetch source HTML
            return bs4.BeautifulSoup(self.get(url).text, "lxml")

        # .. otherwise ..
        except requests.exceptions.HTTPError:
            # .. provide empty results
            return bs4.BeautifulSoup("", "lxml")

    def get_json(self, url: str) -> List[dict]:
        """
        Fetches JSON for given URL

        :param url: str Target URL
        :return: list Source JSON
        """

        # Attempt to ..
        try:
            # .. fetch source JSON
            return self.get(url).json()

        # .. otherwise ..
        except requests.exceptions.HTTPError:
            # .. provide empty results
            return []

    def make_palettes(self, palette: Optional[str]) -> None:
        """
        Makes color palettes for one or all palette types

        :param palette: str | None
        :return: None
        """

        # Build path to JSON file (= main file)
        data_file = self.brand_path / "colors.json"

        with data_file.open("w", encoding="utf-8") as file:
            json.dump(self.sets, file, indent=4)

        print(f'Saving "{data_file.relative_to(pathlib.Path.cwd())}" .. done')

        # Build & create path to color sets
        sets_path = self.brand_path / "sets"
        sets_path.mkdir(parents=True, exist_ok=True)

        # Iterate over available palette types
        for dtype in ["acb", "gpl", "soc", "xml"]:
            if palette is not None and dtype is not palette:
                continue

            # Iterate over color sets
            for set_name, data in self.sets.items():
                # Build path to palette file
                palette_file = sets_path / f"{set_name}.{dtype}"

                # Party time!
                getattr(self, f"make_{dtype}")(palette_file, data)

    def make_xml(self, xml_file: pathlib.Path, data: dict):
        """
        Builds XML color palette (Scribus)

        :param xml_file: pathlib.Path Target XML file
        :param data: dict Color data
        :return: None
        """

        # Insert header (including copyright notice)
        copyright_notice = self.copyright_notices.get(
            "xml", self.default_copyright_notices["xml"]
        )
        comment = etree.Comment(copyright_notice)
        root = etree.Element("SCRIBUSCOLORS")
        root.insert(0, comment)

        for color in data:
            rgb = color["rgb"][4:-1].split(",")
            name = color["name"].title() if color["name"] else color["code"]
            entry = etree.SubElement(root, "COLOR")

            entry.set("NAME", name)
            entry.set("SPACE", "RGB")
            entry.set("R", rgb[0])
            entry.set("G", rgb[1])
            entry.set("B", rgb[2])

        # Write color data
        tree = etree.ElementTree(root)
        tree.write(xml_file, xml_declaration=True, encoding="UTF-8", pretty_print=True)

        print(f'Generating "{xml_file.relative_to(pathlib.Path.cwd())}" .. done')

    def make_gpl(self, gpl_file: pathlib.Path, data: dict) -> None:
        """
        Builds GPL color palette (GIMP + Inkscape)

        :param gpl_file: pathlib.Path Target GPL file
        :param data: dict Color data
        :return: None
        """

        # Write color data
        with open(gpl_file, "w", encoding="utf-8") as file:
            title = (
                gpl_file.stem.title()
                if self.identifier != "pantone"
                else gpl_file.stem.replace("colors", "Colors")
            )

            file.write("GIMP Palette\n")
            file.write("Name: " + title + "\n")
            file.write(
                self.copyright_notices.get("gpl", self.default_copyright_notices["gpl"])
            )

            for color in data:
                name = color["name"].title() if color["name"] else color["code"]
                line = color["rgb"][4:-1].split(",")

                for idx, _ in enumerate(line):
                    line[idx] = f"{line[idx]:0>3}"

                line.append(name)
                file.write(" ".join(line) + "\n")

        print(f'Generating "{gpl_file.relative_to(pathlib.Path.cwd())}" .. done')

    def make_acb(self, acb_file: pathlib.Path, data: dict) -> None:
        """
        Builds ACB color palette (AutoCAD)

        :param acb_file: pathlib.Path Target ACB file
        :param data: dict Color data
        :return: None
        """

        root = etree.Element("colorbook")

        title = etree.SubElement(root, "bookName")
        title.text = (
            acb_file.stem.title()
            if self.identifier != "pantone"
            else acb_file.stem.replace("colors", "Colors")
        )
        copyright_notice = self.copyright_notices.get(
            "xml", self.default_copyright_notices["xml"]
        )
        comment = etree.Comment(copyright_notice)
        root.insert(0, comment)

        color_page = etree.SubElement(root, "colorPage")
        page_color = etree.SubElement(color_page, "pageColor")
        rgb8 = etree.SubElement(page_color, "RGB8")
        page_background = {
            "red": "100",
            "green": "100",
            "blue": "100",
        }

        for color, value in page_background.items():
            entry = etree.SubElement(rgb8, color)
            entry.text = value

        for color in data:
            rgb = color["rgb"][4:-1].split(",")
            name = color["name"].title() if color["name"] != "" else color["code"]

            entry = etree.SubElement(color_page, "colorEntry")
            color_name = etree.SubElement(entry, "colorName")
            color_name.text = name

            keys = ["red", "green", "blue"]
            rgb_dict = {k: v for k, v in zip(keys, rgb)}
            rgb8 = etree.SubElement(entry, "RGB8")

            for color, value in rgb_dict.items():
                entry = etree.SubElement(rgb8, color)
                entry.text = value

        # Write color data
        tree = etree.ElementTree(root)
        tree.write(acb_file, xml_declaration=True, encoding="UTF-8", pretty_print=True)

        print(f'Generating "{acb_file.relative_to(pathlib.Path.cwd())}" .. done')

    def make_soc(self, soc_file: pathlib.Path, data: dict) -> None:
        """
        Builds SOC color palette (OpenOffice + LibreOffice)

        :param soc_file: pathlib.Path Target SOC file
        :param data: dict Color data
        :return: None
        """

        namespaces = {
            "office": "http://openoffice.org/2000/office",
            "style": "http://openoffice.org/2000/style",
            "text": "http://openoffice.org/2000/text",
            "table": "http://openoffice.org/2000/table",
            "draw": "http://openoffice.org/2000/drawing",
            "fo": "http://www.w3.org/1999/XSL/Format",
            "xlink": "http://www.w3.org/1999/xlink",
            "dc": "http://purl.org/dc/elements/1.1/",
            "meta": "http://openoffice.org/2000/meta",
            "number": "http://openoffice.org/2000/datastyle",
            "svg": "http://www.w3.org/2000/svg",
            "chart": "http://openoffice.org/2000/chart",
            "dr3d": "http://openoffice.org/2000/dr3d",
            "math": "http://www.w3.org/1998/Math/MathML",
            "form": "http://openoffice.org/2000/form",
            "script": "http://openoffice.org/2000/script",
            "config": "http://openoffice.org/2001/config",
        }

        copyright_notice = self.copyright_notices.get(
            "xml", self.default_copyright_notices["xml"]
        )
        comment = etree.Comment(copyright_notice)
        root = etree.Element("color-table", nsmap=namespaces)
        root.insert(0, comment)

        for color in data:
            name = color["name"].title() if color["name"] != "" else color["code"]
            entry = etree.SubElement(root, "color")

            entry.set("name", name)
            entry.set("color", color["hex"])

        # Write SOC color palettes to disk (mirroring JSON source structure)
        tree = etree.ElementTree(root)
        tree.write(soc_file, xml_declaration=True, encoding="UTF-8", pretty_print=True)

        with soc_file.open("r", encoding="utf-8") as file:
            data = file.read()
            data = data.replace("color-table", "office:color-table")
            data = data.replace("<color", "<draw:color")
            data = data.replace("name=", "draw:name=")
            data = data.replace("color=", "draw:color=")

        with soc_file.open("w", encoding="utf-8") as file:
            file.write(data)

        print(f'Generating "{soc_file.relative_to(pathlib.Path.cwd())}" .. done')
