#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

# Fetching color sets from https://www.numerosamente.it/pantone-list/
#
# Valid options:
# - 'graphic-design', currently 15870 colors (pp 1-32)
# - 'fashion-design', currently 2443 colors (pp 1-14)
# - 'product-design', currently 4967 colors (pp 1-10)

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

        print(i)

        for sourceElement in soup.findAll('tr')[1:]:
            color = {}
            color['code'] = sourceElement.findAll('td')[0].text
            color['rgb'] = sourceElement.findAll('td')[1].text
            color['hex'] = sourceElement.findAll('td')[2].text
            color['name'] = sourceElement.findAll('td')[3].text
            color['category'] = sourceElement.findAll('td')[4].text

            found_same_name = False
            for localElement in sets[setName]:
                if color['name'] != '' and color['name'] == localElement['name']:
                    found_same_name = True

            if not found_same_name:
                sets[setName].append(color)


sets = {
    'graphic-design': [],
    'fashion-design': [],
    'product-design': [],
}

fetch('graphic-design', 1, 32)
fetch('fashion-design', 1, 14)
fetch('industrial-design', 1, 10)

result = open('./pantone.json', 'w')
json.dump(sets, result, indent=4)
