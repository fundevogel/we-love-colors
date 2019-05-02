#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json, shutil, os

# TODO: Making use of arguments, see https://www.tutorialspoint.com/python3/python_command_line_arguments.htm

##
# Defining sets & subsets to be filled later
##

sets = {
    'dulux': []
}


##
# This function fetches Dulux® colors
##
def fetch():
    # One baseURL to rule them all
    baseUrl = 'https://colour.dulux.ca/all-colors'

    # Looping through URLs & scraping color information from HTML tables
    html = urlopen(baseUrl)
    soup = BeautifulSoup(html, 'lxml')

    for color_tile in soup.find_all('a', {'class': 'all-color-tile'}):
        rgb_string = color_tile.get('style')[17:].replace(', ', ',')
        rgb_list = rgb_string[4:-1].split(',')
        rgb = [int(i) for i in rgb_list]

        color = {}
        color['code'] = color_tile.find(attrs={'class': 'color-number'}).text
        color['rgb'] = rgb_string
        color['hex'] = '#%02x%02x%02x' % tuple(rgb)
        color['name'] = color_tile.find(attrs={'class': 'color-name'}).text
        for i, entry in color.items():
            color[i] = entry.strip()

        sets['dulux'].append(color)

        print('Loading ' + color['code'] + ' in set "dulux" .. done')


##
# Fetching, extracting & dumping Dulux® colors, sets & subsets
##

# Fetching Dulux® colors
fetch()

# Creating directory for Dulux® color sets (if it doesn't exist already)
root_path =  './dulux'
json_path = root_path + '/json'

try:
    shutil.rmtree(json_path)
except:
    print('Error while deleting directory')

os.makedirs(json_path, exist_ok=True)

# Dumping all Dulux® colors
with open(root_path + '/dulux.json', 'w') as file:
    file.write(json.dumps(sets, indent=4))

for set, colors in sets.items():
    if len(colors) == 0:
        break

    file_name = set + ' (' + str(len(colors)) + ' colors).json'

    # Dumping Dulux® color sets to disk
    with open(json_path + '/' + file_name, 'w') as file:
        file.write(json.dumps(colors, indent=4))
    print('%s has been created.' % file_name)
