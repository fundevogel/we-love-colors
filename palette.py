#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# Imports
# For more information, see https://www.python.org/dev/peps/pep-0008/#imports
##

import os
import glob
import json

from lxml import etree


class Palette:
    def __init__(self):
        os.makedirs(self.json_path, exist_ok=True)


    ##
    # Dumps fetched colors as JSON
    ##
    def save(self, output_filename=''):
        if output_filename == '':
            output_filename = self.identifier

        json_path = self.json_path + '/' + output_filename + '.json'

        with open(json_path, 'w') as file:
            file.write(json.dumps(self.sets, indent=4))

        print('Saving "' + json_path + '" .. done')


    ##
    # Creates JSON files for each color set
    ##
    def create_json(self, input_filename=''):
        if input_filename == '':
            input_filename = self.identifier

        with open(self.json_path + '/' + input_filename + '.json', 'r') as file:
            data = json.load(file)

        for set, colors in data.items():
            if len(colors) == 0:
                break

            # Creating subdirectory
            file_path = self.json_path + '/sets'
            os.makedirs(file_path, exist_ok=True)

            json_path = file_path + '/' + set + '_' + str(len(colors)) + '-colors.json'

            # Dumps color sets as JSON
            with open(json_path, 'w') as file:
                file.write(json.dumps(colors, indent=4))

            print('Generating %s .. done' % json_path)


    ##
    # Makes color palettes in various formats
    ##
    def make_palettes(self):
        # Copyright notices
        default_copyright = {
            'xml': '\n    For copyright and other legal information,\n    please refer to "README.md" in the root of this project\n  ',
            'gpl': '##\n# For copyright and other legal information, please refer to "README.md" in the root of this project\n##\n',
        }

        # Globbing all JSON source files
        paths = glob.glob('./palettes/' + self.identifier + '/json/*/*.json', recursive=True)

        for path in paths:
            file_name = os.path.basename(path).replace('.json', '')

            with open(path, 'r') as file:
                data = json.load(file)


            ##
            # Building XML color palettes for Scribus
            ##
            root = etree.Element('SCRIBUSCOLORS')
            comment = etree.Comment(self.copyright.get('xml', default_copyright['xml']))
            root.insert(0, comment)
            for color in data:
                rgb = color['rgb'][4:-1].split(',')
                name = color['name'].title() if color['name'] != '' else color['code']
                entry = etree.SubElement(root, 'COLOR')
                entry.set('NAME', name)
                entry.set('SPACE', 'RGB')
                entry.set('R', rgb[0])
                entry.set('G', rgb[1])
                entry.set('B', rgb[2])

            # Creating directories for XML color palettes (if it doesn't exist already)
            output_path = os.path.dirname(path).replace('/json', '/xml')
            os.makedirs(output_path, exist_ok=True)

            # Writing XML color palettes to disk (mirroring JSON source structure)
            xml_file = output_path + '/' + file_name + '.xml'
            tree = etree.ElementTree(root)
            tree.write(xml_file, xml_declaration=True, encoding='UTF-8', pretty_print=True)

            print('Generating %s .. done' % xml_file)


            ##
            # Building GPL color palettes for GIMP/Inkscape
            ##
            title = file_name.title() if self.identifier != 'pantone' else file_name.replace('colors', 'Colors')

            # Creating directories for GPL color palettes (if it doesn't exist already)
            output_path = os.path.dirname(path).replace('/json', '/gpl')
            os.makedirs(output_path, exist_ok=True)

            # Writing GPL color palettes to disk (mirroring JSON source structure)
            gpl_file = output_path + '/' + file_name + '.gpl'

            with open(gpl_file, 'w') as file:
                file.write('GIMP Palette\n')
                file.write('Name: ' + title + '\n')
                file.write(self.copyright.get('xml', default_copyright['xml']))
                file.write('\n')

                for color in data:
                    name = color['name'].title() if color['name'] != '' else color['code']
                    line = color['rgb'][4:-1].split(',')

                    for i in range(len(line)):
                        line[i] = '{:0>3}'.format(line[i])

                    line.append(name)
                    file.write(' '.join(line) + '\n')

            print('Generating %s .. done' % gpl_file)
