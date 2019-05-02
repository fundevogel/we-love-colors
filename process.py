#!/usr/bin/env python3

from lxml import etree
import json, glob, os


##
# Globbing all JSON source files
##
paths = glob.glob('./*/json/**/*.json', recursive=True)


##
# Copyright notices
##
copyright = {
    # Default notice
    'default_xml': '\n    For copyright and other legal information,\n    please refer to "README.md" in the root of this project\n  ',
    'default_gpl': '##\n# For copyright and other legal information, please refer to "README.md" in the root of this project\n##\n',

    # Owner's notice
    'pantone': {
        'xml': '\n    PANTONE® and related trademarks are the property of\n    Pantone LLC (https://www.pantone.com), a division of X-Rite, a Danaher company\n  ',
        'gpl': '##\n# PANTONE® and related trademarks are the property of\n# Pantone LLC (https://www.pantone.com), a division of X-Rite, a Danaher company\n##\n'
    },
    'ral': {
        'xml': '\n    RAL® and related trademarks are the property of\n    RAL gGmbH (https://www.ral-farben.de) (non-profit LLC) or\n    RAL Deutsches Institut für Gütesicherung und Kennzeichnung e. V. (https://www.ral.de)\n  ',
        'gpl': '##\n# RAL® and related trademarks are the property of\n# RAL gGmbH (https://www.ral-farben.de) (non-profit LLC) or\n# RAL Deutsches Institut für Gütesicherung und Kennzeichnung e. V. (https://www.ral.de)\n##\n',
    },
    'dulux': {
        'xml': '\n    Dulux® and related trademarks are the property of\n    AkzoNobel N.V. (https://www.akzonobel.com) (joint-stock company) (worldwide) or\n    DuluxGroup (https://www.dulux.com.au) (Australia & New Zealand) \n  ',
        'gpl': '##\n# Dulux® and related trademarks are the property of\n# AkzoNobel N.V. (https://www.akzonobel.com) (joint-stock company) (worldwide) or\n# DuluxGroup (https://www.dulux.com.au) (Australia & New Zealand) \n##\n',
    },
    'copic': {
        'xml': '\n    Copic® and related trademarks are the property of\n    Too Marker Corporation (https://www.toomarker.co.jp/en)\n  ',
        'gpl': '##\n# Copic® and related trademarks are the property of\n# Too Marker Corporation (https://www.toomarker.co.jp/en)\n##\n',
    },
    'prismacolor': {
        'xml': '\n    Prismacolor® and related trademarks are the property of\n    Berol Corporation (http://www.berol.co.uk), owned by Sanford L.P. (http://www.sanfordb2b.com),\n    a Newell Brands (https://www.newellbrands.com) company\n  ',
        'gpl': '##\n# Prismacolor® and related trademarks are the property of\n# Berol Corporation (http://www.berol.co.uk), owned by Sanford L.P. (http://www.sanfordb2b.com),\n# a Newell Brands (https://www.newellbrands.com) company\n##\n',
    },
}


##
# Processing source files
##
for path in paths:
    # ./path/to/file.json >> path
    identifier = path.split('/')[1]

    # ./path/to/file.json >> file
    file_name = os.path.basename(path).replace('.json', '')

    # Loading PANTONE® colors from each JSON file as object
    with open(path, 'r') as file:
        data = json.load(file)


    ##
    # Building XML color palettes for Scribus
    ##
    root = etree.Element('SCRIBUSCOLORS')
    comment = etree.Comment(copyright[identifier].get('xml', copyright['default_xml']))
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
    tree = etree.ElementTree(root)
    tree.write(output_path + '/' + file_name + '.xml', xml_declaration=True, encoding='UTF-8', pretty_print=True)
    print('%s.xml has been created.' % file_name)


    ##
    # Building GPL color palettes for GIMP/Inkscape
    ##
    title = file_name.title() if identifier != 'pantone' else file_name.replace('colors', 'Colors')

    # Creating directories for GPL color palettes (if it doesn't exist already)
    output_path = os.path.dirname(path).replace('/json', '/gpl')
    os.makedirs(output_path, exist_ok=True)

    # Writing GPL color palettes to disk (mirroring JSON source structure)
    with open(output_path + '/' + file_name + '.gpl','w') as file:
        file.write('GIMP Palette\n')
        file.write('Name: ' + title + '\n')
        file.write(copyright[identifier].get('gpl', copyright['default_gpl']))
        file.write('\n')

        for color in data:
            name = color['name'].title() if color['name'] != '' else color['code']
            line = color['rgb'][4:-1].split(',')

            for i in range(len(line)):
                line[i] = '{:0>3}'.format(line[i])

            line.append(name)
            file.write(' '.join(line) + '\n')
    print('%s.gpl has been created.' % file_name)
