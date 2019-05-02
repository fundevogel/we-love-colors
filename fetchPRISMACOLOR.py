#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json, shutil, os

# TODO: Making use of arguments, see https://www.tutorialspoint.com/python3/python_command_line_arguments.htm

##
# Defining sets to be filled later
##

sets = {
    'premier': []
}


##
# This function fetches Prismacolor® colors
#
# Valid `setName` parameter:
# - 'premier', currently 150 colors
##
def fetch(setName):
    # One baseURL to rule them all
    baseUrl = 'https://kredki.eu/pl/p/Prismacolor-Colored-Pencils-Kredki-Art-150-Kol/75'

    # Looping through URLs & scraping color information from HTML tables
    html = urlopen(baseUrl)
    soup = BeautifulSoup(html, 'lxml')

    for list_element in soup.find('div', {'class': 'resetcss'}).findAll('li')[1:]:
        color_list = []
        line = list_element.text

        color = {}

        if not line[0:2] == 'PC':
            continue

        line = line.split(':')
        code_name = line[0][0:-4].split(' ')
        rgb_string = line[1][:-4].replace(', ', ',')
        rgb_list = rgb_string.split(',')
        rgb = [int(i) for i in rgb_list]
        hexadecimal = '#%02x%02x%02x' % tuple(rgb)

        color['code'] = ' '.join([code_name.pop(0), code_name.pop(0)])
        color['rgb'] = 'rgb(' + rgb_string.strip() + ')'
        color['hex'] = hexadecimal.upper()
        color['name'] = ' '.join(code_name)

        sets[setName].append(color)

        print('Loading ' + color['code'] + ' in set "' + setName + '" .. done')


##
# Fetching, extracting & dumping Prismacolor® colors, sets & subsets
##

# Fetching Prismacolor® colors
fetch('premier')

# Creating directory for Prismacolor® color sets (if it doesn't exist already)
root_path =  './prismacolor'
json_path = root_path + '/json'

try:
    shutil.rmtree(json_path)
except:
    print('Error while deleting directory')

os.makedirs(json_path, exist_ok=True)

# Dumping all Prismacolor® colors
with open(root_path + '/prismacolor.json', 'w') as file:
    file.write(json.dumps(sets, indent=4))

for set, colors in sets.items():
    if len(colors) == 0:
        break

    file_name = set + ' (' + str(len(colors)) + ' colors).json'

    # Dumping Prismacolor® color sets to disk
    with open(json_path + '/' + file_name, 'w') as file:
        file.write(json.dumps(colors, indent=4))
    print('%s has been created.' % file_name)
