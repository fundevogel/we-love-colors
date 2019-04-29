#!/usr/bin/env python3

from lxml import etree
import json, glob, os


##
# Globbing all JSON source files
##
paths = glob.glob('./json/**/*.json', recursive=True)

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

    # Creating directories for XML color palettes (if it doesn't exist already)
    output_path = os.path.dirname(path).replace('/json', '/xml')
    os.makedirs(output_path, exist_ok=True)

    # Writing XML color palettes to disk (mirroring JSON source structure)
    tree = etree.ElementTree(root)
    tree.write(output_path + '/' + file_name + '.xml', xml_declaration=True, encoding='UTF-8', pretty_print=True)
    print('%s.xml has been created.' % file_name)


    ##
    # Building GPL color palettes for GIMP/Inkscape
    ##
    title = file_name.title() if '-' in file_name else file_name.replace('colors', 'Colors')
    title = title.replace('-', ' ')

    # Creating directories for GPL color palettes (if it doesn't exist already)
    output_path = os.path.dirname(path).replace('/json', '/gpl')
    os.makedirs(output_path, exist_ok=True)

    # Writing GPL color palettes to disk (mirroring JSON source structure)
    with open(output_path + '/' + file_name + '.gpl','w') as file:
        file.write('GIMP Palette\n')
        file.write('Name: ' + title + '\n')
        file.write('##\n# PANTONE® and other Pantone LLC (https://www.pantone.com) trademarks are\n# the property of Pantone LLC, a division of X-Rite, a Danaher company. \n##\n')
        file.write('\n')

        for color in data:
            name = color['name'] if color['name'] != '' else color['code']
            line = color['rgb'][4:-1].split(',')

            for i in range(len(line)):
                line[i] = '{:0>3}'.format(line[i])

            line.append(name)
            file.write(' '.join(line) + '\n')
    print('%s.gpl has been created.' % file_name)
