#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


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

        print('Loading page ' + str(i) + '.. done')

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
# Fetching, extracting & dumping PANTONE® colors
##

# Fetching PANTONE® colors
fetch('graphic-design', 1, 32)
fetch('fashion-design', 1, 14)
fetch('product-design', 1, 10)

# Dumping complete PANTONE® color sets
with open('./pantone.json', 'w') as file:
    file.write(json.dumps(remoteSets, indent=4))

# Extracting each PANTONE® color subset
for set, colors in remoteSets.items():
    subset = localSets[set]
    with open('./sets/' + set + ' (' + str(len(colors)) + ' colors).json', 'w') as file:
        file.write(json.dumps(colors, indent=4))
    for color in colors:
        code = color['code']
        if code[2:] == 'P ':
            if code[-2:] == ' C':
                subset['PC'].append(color)
            if code[-2:] == ' U':
                subset['PU'].append(color)
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
        if code[3:] == 'PQ-':
            subset['PQ'].append(color)

# Dumping each PANTONE® color subset
for set, subsets in localSets.items():
    for subset, colors in subsets.items():
        with open('./sets/subsets/' + set + '/' + subset + ' (' + str(len(colors)) + ' colors).json', 'w') as file:
            file.write(json.dumps(colors, indent=4))
