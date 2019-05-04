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

from palette import Palette


class Dulux(Palette):
    # Dictionary holding fetched colors
    sets = {
        'dulux': []
    }

    # Identifier
    identifier = 'dulux'

    # Global JSON path
    json_path = './palettes/' + identifier + '/json'

    # Copyright notices
    copyright = {
        'xml': '\n    Dulux® and related trademarks are the property of\n    AkzoNobel N.V. (https://www.akzonobel.com) (joint-stock company) (worldwide) or\n    DuluxGroup (https://www.dulux.com.au) (Australia & New Zealand) \n  ',
        'gpl': '##\n# Dulux® and related trademarks are the property of\n# AkzoNobel N.V. (https://www.akzonobel.com) (joint-stock company) (worldwide) or\n# DuluxGroup (https://www.dulux.com.au) (Australia & New Zealand) \n##\n',
    }


    def __init__(self):
        super().__init__()


    ##
    # Fetches Dulux® colors
    # Valid `set_name` parameter:
    # - 'dulux', currently 1768 colors
    ##
    def fetch(self, set_name):
        # One baseURL to rule them all
        base_url = 'https://colour.dulux.ca/all-colors'

        # Scraping Dulux® colors from HTML
        html = urlopen(base_url)
        soup = BeautifulSoup(html, 'lxml')

        for color_tile in soup.find_all('a', {'class': 'all-color-tile'}):
            rgb_string = color_tile.get('style')[17:].replace(', ', ',')
            rgb_list = rgb_string[4:-1].split(',')
            rgb = [int(i) for i in rgb_list]

            color = {}
            color['code'] = color_tile.find(attrs={'class': 'color-number'}).text
            color['rgb'] = rgb_string
            color['hex'] = '#%02x%02x%02x' % tuple(rgb) # Converting to hexadecimal color code, see https://stackoverflow.com/a/3380739
            color['name'] = color_tile.find(attrs={'class': 'color-name'}).text

            for i, entry in color.items():
                color[i] = entry.strip()

            self.sets[set_name].append(color)

            print('Loading ' + color['code'] + ' in set "' + set_name + '" .. done')
