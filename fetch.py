#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json, os, re


##
# Defining sets & subsets to be filled later
##

remoteSets = {
    'graphic-design': [],
    'fashion-design': [],
    'product-design': [],
}

localSets = {
    ##
    # Pantone Color Systems - Graphics
    # Pantone Matching System - PMS
    # For more information, see https://www.pantone.com/color-systems/for-graphic-design
    # or visit their shop: https://www.pantone.com/graphics
    ##
    'graphic-design': {
        # TODO: Solid/Spot Colors (Coated & Uncoated) - Link?
        'C': [],
        'U': [],

        ##
        # CMYK Color Guide (Coated & Uncoated)
        # https://www.pantone.com/products/graphics/cmyk-coated-uncoated
        ##
        'PC': [],
        'PU': [],

        ##
        # Color Bridge Set (Coated & Uncoated)
        # https://www.pantone.com/products/graphics/color-bridge-coated-uncoated
        ##
        'CP': [], # https://www.pantone.com/products/graphics/color-bridge-coated
        'UP': [], # https://www.pantone.com/products/graphics/color-bridge-uncoated

        ##
        # Extended Gamut Coated Guide
        # https://www.pantone.com/products/graphics/extended-gamut-coated-guide
        ##
        'XGC': [],

        # TODO: Pastels & Neons (C+U), see https://www.pantone.com/products/graphics/pastels-neons
        # TODO: Metallics, see https://www.pantone.com/products/graphics/metallics-guide
    },

    ##
    # Pantone Color Systems - Fashion
    # Fashion, Home + Interiors - FHI
    # For more information, see https://www.pantone.com/color-systems/for-fashion-design
    # or visit their shop: https://www.pantone.com/fashion-home-interiors
    ##
    'fashion-design': {
        # TODO: 'Textile Paper eXtended'
        'TPX': [],

        # TODO: 'Textile Paper Green'
        'TPG': [],

        # TODO: 'Textile Cotton eXtended'
        'TCX': [],

        ##
        # Nylon Brights Set
        # https://www.pantone.com/products/fashion-home-interiors/nylon-brights-set
        ##
        'TN': [],

        ##
        # Pantone SkinTone™ Guide
        # https://www.pantone.com/products/fashion-home-interiors/pantone-skintone-guide
        ##
        'SP': [],
    },

    ##
    # Pantone Color Systems - Product
    # Plastic Standards
    # For more information, see https://www.pantone.com/color-systems/for-product-design
    # or visit the shop: https://www.pantone.com/plastics
    ##
    'product-design': {
        'PQ': [], # https://www.pantone.com/color-intelligence/articles/technical/did-you-know-pantone-plastics-standards-explained

        # TODO: 'Textile Cotton eXtended'
        'TCX': [],
    },
}


##
# This function applies a natural sort order to dictionaries inside the
# list passed as first argument by the key specified as second argument
# See https://stackoverflow.com/a/8940266
##
def natural_sort(list, key=lambda x: x['code']):
    def get_alphanum_key_func(key):
        convert = lambda text: int(text) if text.isdigit() else text
        return lambda s: [convert(c) for c in re.split('([0-9]+)', key(s))]
    sort_key = get_alphanum_key_func(key)
    list.sort(key=sort_key)


##
# This function fetches PANTONE® colors
#
# Valid `setName` parameter:
# - 'graphic-design', currently 15870 colors (pp 1-32)
# - 'fashion-design', currently 2443 colors (pp 1-14)
# - 'product-design', currently 4967 colors (pp 1-10)
##
def fetch(setName, firstPage, lastPage):
    # One baseURL to rule them all
    baseUrl = 'https://www.numerosamente.it/pantone-list/'

    # Translating setName to valid URL path name via `dict.get()`
    setUrl = {
        'graphic-design': 'graphic-designers/',
        'fashion-design': 'fashion-and-interior-designers/',
        'product-design': 'industrial-designers/',
    }

    # Looping through URLs & scraping color information from HTML tables
    for i in range(firstPage, lastPage + 1):
        html = urlopen(baseUrl + setUrl.get(setName) + str(i))
        soup = BeautifulSoup(html, 'lxml')

        print('Loading page ' + str(i) + ' .. done')

        for remoteElement in soup.findAll('tr')[1:]:
            color = {}
            color['code'] = remoteElement.findAll('td')[0].text
            color['rgb'] = remoteElement.findAll('td')[1].text
            color['hex'] = remoteElement.findAll('td')[2].text
            color['name'] = remoteElement.findAll('td')[3].text

            # Checking if a fetched element already exists ..
            found_same_name = False
            for localElement in remoteSets[setName]:
                if color['name'] != '' and color['name'] == localElement['name']:
                    found_same_name = True

            # .. if not, adding it is da real MVP
            if not found_same_name:
                remoteSets[setName].append(color)


##
# Fetching, extracting & dumping PANTONE® colors, sets & subsets
##

# Fetching PANTONE® colors
fetch('graphic-design', 1, 32)
fetch('fashion-design', 1, 14)
fetch('product-design', 1, 10)

# Dumping all PANTONE® colors
with open('./pantone.json', 'w') as file:
    file.write(json.dumps(remoteSets, indent=4))

# Creating directory for PANTONE® color sets (if it doesn't exist already)
file_path = './json'
os.makedirs(file_path, exist_ok=True)

# Looping through PANTONE® color sets
for set, colors in remoteSets.items():
    file_name = set + ' (' + str(len(colors)) + ' colors).json'

    # Dumping PANTONE® color sets to disk
    with open(file_path + '/' + file_name, 'w') as file:
        file.write(json.dumps(colors, indent=4))
    print('%s.json has been created.' % file_name)

    subset = localSets[set]

    # Extracting each PANTONE® color subset
    for color in colors:
        code = color['code']
        if code[0:2] == 'P ':
            # print(code)
            if code[-2:] == ' C':
                # print(code)
                subset['PC'].append(color)
            if code[-2:] == ' U':
                subset['PU'].append(color)
                # print(code)
        else:
            if code[-2:] == ' C':
                subset['C'].append(color)
            if code[-2:] == ' U':
                subset['U'].append(color)
        if code[-3:] == ' CP':
            subset['CP'].append(color)
        if code[-3:] == ' UP':
            subset['UP'].append(color)
        if code[-3:] == 'XGC':
            subset['XGC'].append(color)
        if code[-3:] == 'TCX':
            subset['TCX'].append(color)
        if code[-3:] == 'TPG':
            subset['TPG'].append(color)
        if code[-3:] == 'TPX':
            subset['TPX'].append(color)
        if code[-3:] == ' TN':
            subset['TN'].append(color)
        if code[-3:] == ' SP':
            subset['SP'].append(color)
        if code[0:3] == 'PQ-':
            subset['PQ'].append(color)

# Looping through PANTONE® color subsets
for set, subsets in localSets.items():
    # Creating directories for PANTONE® color subsets (if they don't exist already)
    file_path = './json/' + set
    os.makedirs(file_path, exist_ok=True)

    # Dumping PANTONE® color subsets to disk
    for subset, colors in subsets.items():
        # Applying natural sort order to all 'Graphics' PANTONE® Color System subsets
        if set == 'graphic-design':
            natural_sort(colors)

        file_name = subset + ' (' + str(len(colors)) + ' colors).json'
        with open(file_path + '/' + file_name, 'w') as file:
            file = open(file_path + '/' + file_name, 'w')
            file.write(json.dumps(colors, indent=4))
        print('%s.json has been created.' % file_name)
