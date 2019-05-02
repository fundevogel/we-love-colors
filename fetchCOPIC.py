#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json, shutil, os

# TODO: Making use of arguments, see https://www.tutorialspoint.com/python3/python_command_line_arguments.htm

##
# Defining sets to be filled later
##

sets = {
    'copic': []
}


##
# This function fetches Copic® colors
##
def fetch():
    # One baseURL to rule them all
    baseUrl = 'https://www.copicmarker.com/collections/collect'

    # Looping through URLs & scraping color information from HTML tables
    html = urlopen(baseUrl)
    soup = BeautifulSoup(html, 'lxml')

    for color_tile in soup.find('div', {'class': 'collection-color--desktop'}).find_all('div', {'class': 'product-item-hex'}):
        data_name = color_tile['data-name']
        data_list = data_name.split(' ')

        hexadecimal = color_tile['style'][12:-8]
        rgb_list = tuple(int(hexadecimal.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        rgb = [str(i) for i in rgb_list]

        color = {}
        color['code'] = data_list.pop(0)
        color['rgb'] = 'rgb(' + ','.join(rgb) + ')'
        color['hex'] = hexadecimal.upper()
        color['name'] = ' '.join(data_list)

        sets['copic'].append(color)

        print('Loading ' + color['code'] + ' in set "copic" .. done')


##
# Fetching, extracting & dumping Copic® colors, sets & subsets
##

# Fetching Copic® colors
fetch()

# Creating directory for Copic® color sets (if it doesn't exist already)
root_path =  './copic'
json_path = root_path + '/json'

try:
    shutil.rmtree(json_path)
except:
    print('Error while deleting directory')

os.makedirs(json_path, exist_ok=True)

# Dumping all Copic® colors
with open(root_path + '/copic.json', 'w') as file:
    file.write(json.dumps(sets, indent=4))

for set, colors in sets.items():
    if len(colors) == 0:
        break

    file_name = set + ' (' + str(len(colors)) + ' colors).json'

    # Dumping Copic® color sets to disk
    with open(json_path + '/' + file_name, 'w') as file:
        file.write(json.dumps(colors, indent=4))
    print('%s has been created.' % file_name)
