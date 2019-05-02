#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
from PIL import ImageFile
import json, shutil, os

# TODO: Making use of arguments, see https://www.tutorialspoint.com/python3/python_command_line_arguments.htm

##
# Defining sets to be filled later
##

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


##
# This function fetches RAL® colors
#
# Valid `setName` parameter:
# - 'classic',
# - 'design',
# - 'effect',
# - 'plastics'
##
def fetch(setName):
    # One baseURL to rule them all
    baseUrl = 'https://www.ral-farben.de/content/anwendung-hilfe/all-ral-colours-names/overview-ral-' + setName + '-colours.html'

    # Looping through URLs & scraping color information from HTML tables
    # for i in range(firstPage, lastPage + 1):
    html = urlopen(baseUrl)
    soup = BeautifulSoup(html, 'lxml')
    color_grids = soup.find_all('ul', {'class': 'color-grid'})

    for setCount, color_grid in enumerate(color_grids, 1):
        list_elements = color_grid.findAll('li')

        for i, list_element in enumerate(list_elements, 1):
            list_element = list_element.text.splitlines()

            # Parsing each RAL® color's background image, extracting RGB values
            slug = {
                'design': 'designplus',
                'effect': 'ral-effect'
            }

            identifier = slug.get(setName) if (setName in slug) else setName

            if setName == 'plastics':
                identifier = setName + '-p' + str(setCount)

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

            if not setName == 'plastics':
                sets[setName].append(color)
            else:
                sets[identifier].append(color)

            print('Loading ' + color['code'] + ' in set "' + setName + '" .. done')


##
# Fetching, extracting & dumping RAL® colors & sets
##

# Fetching RAL® colors
fetch('classic')
fetch('design')
fetch('effect')
fetch('plastics')

# Creating directory for RAL® color sets (if it doesn't exist already)
root_path =  './ral'
json_path = root_path + '/json'

try:
    shutil.rmtree(json_path)
except:
    print('Error while deleting directory')

os.makedirs(json_path, exist_ok=True)

# Dumping all RAL® colors
with open(root_path + '/ral.json', 'w') as file:
    file.write(json.dumps(sets, indent=4))

for set, colors in sets.items():
    if len(colors) == 0:
        break

    file_name = set + ' (' + str(len(colors)) + ' colors).json'

    # Dumping RAL® color sets to disk
    with open(json_path + '/' + file_name, 'w') as file:
        file.write(json.dumps(colors, indent=4))
    print('%s has been created.' % file_name)
