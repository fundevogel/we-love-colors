#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json, shutil, os, re

# TODO: Making use of arguments, see https://www.tutorialspoint.com/python3/python_command_line_arguments.htm

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

        ##
        # Pastels & Neons (Coated & Uncoated)
        # https://www.pantone.com/products/graphics/pastels-neons
        ##

        # Neons
        'NC': [],
        'NU': [],

        # Pastels
        'PAC': [],
        'PAU': [],

        ##
        # Metallics (Coated)
        # https://www.pantone.com/products/graphics/metallics-guide
        ##
        'MC': [],
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
    'custom-palettes': {
        'color-of-the-year': []
        # IDEA: Palettes created around CotY
    }
}


##
# This function applies a natural sort order to dictionaries inside the
# list passed as first argument by the key specified as second argument
# See https://stackoverflow.com/a/8940266
##
def natural_sort(list, key='code'):
    def get_alphanum_key_func(key):
        convert = lambda text: int(text) if text.isdigit() else text
        return lambda s: [convert(c) for c in re.split('([0-9]+)', key(s))]
    sort_key = get_alphanum_key_func(lambda x: x[key])
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

            print('Loading ' + color['code'] + ' in set "' + setName + '" .. done')


##
# Fetching, extracting & dumping PANTONE® colors, sets & subsets
##

# Fetching PANTONE® colors
# fetch('graphic-design', 1, 32)
# fetch('fashion-design', 1, 14)
# fetch('product-design', 1, 10)

# Creating directory for PANTONE® color sets (if it doesn't exist already)
root_path =  './pantone'
json_path = root_path + '/json'

try:
   shutil.rmtree(json_path)
except:
   print('Error while deleting directory')

os.makedirs(json_path, exist_ok=True)

# Dumping all PANTONE® colors
# with open(root_path + '/pantone.json', 'w') as file:
#     file.write(json.dumps(remoteSets, indent=4))
with open(root_path + '/pantone.json', 'r') as file:
    data = json.load(file)

# Defining base pastels
base_pastels_coated = [
    'Yellow 0131 C',
    'Red 0331 C',
    'Magenta 0521 C',
    'Violet 0631 C',
    'Blue 0821 C',
    'Green 0921 C',
    'Black 0961 C',
]
base_pastels_uncoated = [color.replace(' C', ' U') for color in base_pastels_coated]

##
# Defining PANTONE® colors of the year
# https://www.pantone.com/color-intelligence/color-of-the-year/color-of-the-year-2019
##
colors_of_the_year = [
    '15-4020',
    '17-2031',
    '19-1664',
    '14-4811',
    '17-1456',
    '15-5217',
    '13-1106',
    '19-1557',
    '18-3943',
    '14-0804',
    '15-5519',
    '18-2120',
    '17-1463',
    '17-5641',
    '18-3224',
    '18-1438',
    '15-3919',
    '13-1520',
    '15-0343',
    '18-3838',
    '16-1546',
]

# Looping through PANTONE® color sets
for set, colors in data.items():
    subset = localSets[set]

    # Extracting each PANTONE® color subset
    for i, color in enumerate(colors):
        code = color['code']

        if code[0:7] in colors_of_the_year:
            code = code[0:7]
            color['year'] = 2000 + colors_of_the_year.index(code)
            localSets['custom-palettes']['color-of-the-year'].append(color)

        if code[0:2] == 'P ':
            if code[-2:] == ' C':
                subset['PC'].append(color)
            if code[-2:] == ' U':
                subset['PU'].append(color)
        else:
            if code[-2:] == ' C':
                if len(code) == 5:
                    if ('801 C' <= code <= '814 C') or ('901 C' <= code <= '942 C'):
                        subset['NC'].append(color)
                        continue
                    if '871 C' <= code <= '877 C':
                        subset['MC'].append(color)
                        continue
                if len(code) == 6:
                    if ('8001 C' <= code <= '8965 C'):
                        subset['MC'].append(color)
                        continue
                    if ('9020 C' <= code <= '9603 C') or (code in base_pastels_coated):
                        subset['PAC'].append(color)
                        continue
                if len(code) == 7 and ('10101 C' <= code <= '10399 C'):
                        subset['MC'].append(color)
                        continue
                subset['C'].append(color)
            if code[-2:] == ' U':
                if len(code) == 5:
                    if ('801 U' <= code <= '814 U') or ('901 U' <= code <= '942 U'):
                        subset['NU'].append(color)
                        continue
                    if '871 U' <= code <= '877 U':
                        # TODO: There are no uncoated Metallics, skipping ..
                        continue
                if (len(code) == 6 and ('9020 U' <= code <= '9603 U')) or (code in base_pastels_uncoated):
                    subset['PAU'].append(color)
                    continue
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
    if len(subsets) == 0:
        break

    # Creating directories for PANTONE® color subsets (if they don't exist already)
    file_path = json_path + '/' + set
    os.makedirs(file_path, exist_ok=True)

    # Dumping PANTONE® color subsets to disk
    for subset, colors in subsets.items():
        # Applying natural sort order to all 'Graphics' PANTONE® Color System subsets
        if set == 'graphic-design':
            natural_sort(colors, 'code')
        if set == 'custom-palettes':
            colors.sort(key=lambda k: k['year'])

        if subset == 'color-of-the-year':
            subset = 'CotY'

        file_name = subset + ' (' + str(len(colors)) + ' colors).json'
        with open(file_path + '/' + file_name, 'w') as file:
            file = open(file_path + '/' + file_name, 'w')
            file.write(json.dumps(colors, indent=4))
        print('%s has been created.' % file_name)
