#!/usr/bin/env python3

from lxml import etree
import glob
import json
import os


##
# Globbing all JSON source files
##
paths = glob.glob('./sets/**/*.json', recursive=True)

##
# Processing source files
##
for path in paths:
    # ./path/to/file.json >> file
    file_name = os.path.basename(path).replace('.json', '')

    # Loading PANTONE® colors from each JSON file as object
    with open(path, 'r') as file:
        data = json.load(file)

    ##
    # Building XML color palettes for Scribus
    ##
    root = etree.Element('SCRIBUSCOLORS')
    comment = etree.Comment('PANTONE® and other Pantone LLC (https://www.pantone.com) trademarks are\n the property of Pantone LLC, a division of X-Rite, a Danaher company.')
    root.insert(0, comment)
    for color in data:
        rgb = color['rgb'][4:-1].split(',')
        name = color['name'] if color['name'] != '' else color['code']
        entry = etree.SubElement(root, 'COLOR')
        entry.set('NAME', name)
        entry.set('SPACE', 'RGB')
        entry.set('R', rgb[0])
        entry.set('G', rgb[1])
        entry.set('B', rgb[2])

    # Writing XML content to file, mirroring source's folder structure
    tree = etree.ElementTree(root)
    output_path = os.path.dirname(path).replace('/sets', '/xml')
    tree.write(output_path + '/' + file_name + '.xml', xml_declaration=True, encoding='UTF-8', pretty_print=True)


    ##
    # Building GPL color palettes for GIMP/Inkscape
    ##
    output_path = os.path.dirname(path).replace('/sets', '/gpl')
    title = file_name.title() if '-' in file_name else file_name.replace('colors', 'Colors')
    title = title.replace('-', ' ')
    with open(output_path + '/' + file_name + '.gpl','w') as file:
        file.write('GIMP Palette\n')
        file.write('Name: ' + title + '\n')
        file.write('##\n# PANTONE® and other Pantone LLC (https://www.pantone.com) trademarks are\n# the property of Pantone LLC, a division of X-Rite, a Danaher company. \n##\n')
        file.write('\n')

        for color in data:
            rgb = color['rgb'][4:-1].split(',')
            name = color['name'] if color['name'] != '' else color['code']
            file.write('{:0>3}'.format(rgb[0]) + ' ' + '{:0>3}'.format(rgb[1]) + ' ' + '{:0>3}'.format(rgb[2]) + ' ' + name + '\n')
