import glob
import json
import os

from lxml import etree


class Palette:
    """
    Holds basic palette utilities
    """

    def __init__(self):
        # Copyright notices
        self.default_copyright = {
            "xml": '\n    For copyright and other legal information,\n    please refer to "README.md" in the root of this project\n  ',
            "gpl": '##\n# For copyright and other legal information, please refer to "README.md" in the root of this project\n##\n',
        }

        # Creating global JSON path
        self.json_path = "./palettes/" + self.identifier + "/json"
        os.makedirs(self.json_path, exist_ok=True)

        # Globbing all JSON source files
        self.json_files = glob.glob(self.json_path + "/*/*.json", recursive=True)

    ##
    # Dumps fetched colors as JSON
    ##
    def save(self, output_filename=""):
        if output_filename == "":
            output_filename = self.identifier

        json_path = self.json_path + "/" + output_filename + ".json"

        with open(json_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(self.sets, indent=4))

        print('Saving "' + json_path + '" .. done')

    ##
    # Creates JSON files for each color set
    ##
    def create_json(self, input_filename=""):
        if input_filename == "":
            input_filename = self.identifier

        with open(
            self.json_path + "/" + input_filename + ".json", "r", encoding="utf-8"
        ) as file:
            data = json.load(file)

        for set, colors in data.items():
            if len(colors) == 0:
                break

            # Creating subdirectory
            file_path = self.json_path + "/sets"
            os.makedirs(file_path, exist_ok=True)

            json_path = file_path + "/" + set + "_" + str(len(colors)) + "-colors.json"

            # Dumps color sets as JSON
            with open(json_path, "w", encoding="utf-8") as file:
                file.write(json.dumps(colors, indent=4))

            print("Generating %s .. done" % json_path)

    ##
    # Makes color palettes in various formats
    ##
    def make_palettes(self):
        self.make_xml()
        self.make_gpl()
        self.make_acb()
        self.make_soc()

    # Builds XML color palette (Scribus)
    def make_xml(self):
        for path in self.json_files:
            output_path = os.path.dirname(path).replace("/json", "/xml")
            file_name = os.path.basename(path).replace(".json", "")
            xml_file = output_path + "/" + file_name + ".xml"

            root = etree.Element("SCRIBUSCOLORS")
            comment = etree.Comment(
                self.copyright.get("xml", self.default_copyright["xml"])
            )
            root.insert(0, comment)

            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            for color in data:
                rgb = color["rgb"][4:-1].split(",")
                name = color["name"].title() if color["name"] != "" else color["code"]
                entry = etree.SubElement(root, "COLOR")

                entry.set("NAME", name)
                entry.set("SPACE", "RGB")
                entry.set("R", rgb[0])
                entry.set("G", rgb[1])
                entry.set("B", rgb[2])

            # Creating directories for XML color palettes (if it doesn't exist already)
            os.makedirs(output_path, exist_ok=True)

            # Writing XML color palettes to disk (mirroring JSON source structure)
            tree = etree.ElementTree(root)
            tree.write(
                xml_file, xml_declaration=True, encoding="UTF-8", pretty_print=True
            )

            print("Generating %s .. done" % xml_file)

    # Builds GPL color palette (GIMP + Inkscape)
    def make_gpl(self):
        for path in self.json_files:
            output_path = os.path.dirname(path).replace("/json", "/gpl")
            file_name = os.path.basename(path).replace(".json", "")
            gpl_file = output_path + "/" + file_name + ".gpl"

            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Creating directories for GPL color palettes (if it doesn't exist already)
            os.makedirs(output_path, exist_ok=True)

            # Writing GPL color palettes to disk (mirroring JSON source structure)
            with open(gpl_file, "w", encoding="utf-8") as file:
                title = (
                    file_name.title()
                    if self.identifier != "pantone"
                    else file_name.replace("colors", "Colors")
                )

                file.write("GIMP Palette\n")
                file.write("Name: " + title + "\n")
                file.write(self.copyright.get("gpl", self.default_copyright["gpl"]))

                for color in data:
                    name = (
                        color["name"].title() if color["name"] != "" else color["code"]
                    )
                    line = color["rgb"][4:-1].split(",")

                    for i in range(len(line)):
                        line[i] = "{:0>3}".format(line[i])

                    line.append(name)
                    file.write(" ".join(line) + "\n")

            print("Generating %s .. done" % gpl_file)

    # Builds ACB color palette (AutoCAD)
    def make_acb(self):
        for path in self.json_files:
            output_path = os.path.dirname(path).replace("/json", "/acb")
            file_name = os.path.basename(path).replace(".json", "")
            acb_file = output_path + "/" + file_name + ".acb"

            root = etree.Element("colorbook")

            title = etree.SubElement(root, "bookName")
            title.text = (
                file_name.title()
                if self.identifier != "pantone"
                else file_name.replace("colors", "Colors")
            )
            comment = etree.Comment(
                self.copyright.get("xml", self.default_copyright["xml"])
            )
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

            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

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

            # Creating directories for XML color palettes (if it doesn't exist already)
            os.makedirs(output_path, exist_ok=True)

            # Writing XML color palettes to disk (mirroring JSON source structure)
            tree = etree.ElementTree(root)
            tree.write(
                acb_file, xml_declaration=True, encoding="UTF-8", pretty_print=True
            )

            print("Generating %s .. done" % acb_file)

    # Builds SOC color palette (OpenOffice + LibreOffice)
    def make_soc(self):
        for path in self.json_files:
            output_path = os.path.dirname(path).replace("/json", "/soc")
            file_name = os.path.basename(path).replace(".json", "")
            soc_file = output_path + "/" + file_name + ".soc"

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
            root = etree.Element("color-table", nsmap=namespaces)
            comment = etree.Comment(
                self.copyright.get("xml", self.default_copyright["xml"])
            )
            root.insert(0, comment)

            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            for color in data:
                name = color["name"].title() if color["name"] != "" else color["code"]
                entry = etree.SubElement(root, "color")

                entry.set("name", name)
                entry.set("color", color["hex"])

            # Creating directories for XML color palettes (if it doesn't exist already)
            os.makedirs(output_path, exist_ok=True)

            # Writing XML color palettes to disk (mirroring JSON source structure)
            tree = etree.ElementTree(root)
            tree.write(
                soc_file, xml_declaration=True, encoding="UTF-8", pretty_print=True
            )

            with open(soc_file, "r", encoding="utf-8") as input:
                data = input.read()
                data = data.replace("color-table", "office:color-table")
                data = data.replace("<color", "<draw:color")
                data = data.replace("name=", "draw:name=")
                data = data.replace("color=", "draw:color=")

            with open(soc_file, "w", encoding="utf-8") as output:
                output.write(data)

            print("Generating %s .. done" % soc_file)
