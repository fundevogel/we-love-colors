#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# Imports
# For more information, see https://www.python.org/dev/peps/pep-0008/#imports
##

import os
import json

from urllib.request import urlopen
from bs4 import BeautifulSoup
from PIL import ImageFile

from palette import Palette


class Ral(Palette):
    # Dictionary holding fetched colors
    sets = {
        'classic': [],
        'design': [],
        'effect': [],
        'plastics-p1': [],
        'plastics-p2': [],
        # IDEA: Merging them together?
        # 'plastics' {
        #   'p1': [],
        #   'p2': [],
        # }
    }

    # Identifier
    identifier = 'ral'

    # Global JSON path
    json_path = './palettes/' + identifier + '/json'

    # Copyright notices
    copyright = {
        'xml': '\n    RAL® and related trademarks are the property of\n    RAL gGmbH (https://www.ral-farben.de) (non-profit LLC) or\n    RAL Deutsches Institut für Gütesicherung und Kennzeichnung e. V. (https://www.ral.de)\n  ',
        'gpl': '##\n# RAL® and related trademarks are the property of\n# RAL gGmbH (https://www.ral-farben.de) (non-profit LLC) or\n# RAL Deutsches Institut für Gütesicherung und Kennzeichnung e. V. (https://www.ral.de)\n##\n',
    }


    def __init__(self):
        super().__init__()


    ##
    # Fetches RAL® colors
    #
    # Valid `set_name` parameter:
    # - 'classic',
    # - 'design',
    # - 'effect',
    # - 'plastics'
    ##
    def fetch(self, set_name):
        # One baseURL to rule them all
        base_url = 'https://www.ral-farben.de/content/anwendung-hilfe/all-ral-colours-names/overview-ral-' + set_name + '-colours.html'

        # Scraping RAL® colors from HTML
        html = urlopen(base_url)
        soup = BeautifulSoup(html, 'lxml')
        color_grids = soup.find_all('ul', {'class': 'color-grid'})

        for set_count, color_grid in enumerate(color_grids, 1):
            list_elements = color_grid.findAll('li')

            for i, list_element in enumerate(list_elements, 1):
                list_element = list_element.text.splitlines()

                # Parsing each RAL® color's background image, extracting RGB values
                slug = {
                    'design': 'designplus',
                    'effect': 'ral-effect'
                }

                identifier = slug.get(set_name) if (set_name in slug) else set_name

                if set_name == 'plastics':
                    identifier = set_name + '-p' + str(set_count)

                # See https://stackoverflow.com/a/2271015
                imageUrl = 'https://www.ral-farben.de/out/ralfarben/img/thumbs/' + identifier + '-' + str(i) + '.png'
                image = urlopen(imageUrl)
                parser = ImageFile.Parser()
                while 1:
                    s = image.read(1024)
                    if not s:
                        break
                    parser.feed(s)
                im = parser.close()
                result = im.getpixel((0,0))
                rgb = [str(i) for i in result]

                # Converting to hexadecimal color code, see https://stackoverflow.com/a/3380739
                hexadecimal = '#%02x%02x%02x' % result

                color = {}
                color['code'] = list_element[1].strip()
                color['rgb'] = 'rgb(' + ','.join(rgb) + ')'
                color['hex'] = hexadecimal.upper()
                color['name'] = ''

                if len(list_element) > 2:
                    color['name'] = list_element[2] if len(list_element) == 3 else list_element[3]

                if not set_name == 'plastics':
                    self.sets[set_name].append(color)
                else:
                    self.sets[identifier].append(color)

                print('Loading ' + color['code'] + ' in set "' + set_name + '" .. done')
