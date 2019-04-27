from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

sets = {
	'graphic-design': [],
	'fashion-design': [],
	'product-design': [],
}

for i in range(1, 2):
	html = urlopen('https://www.numerosamente.it/pantone-list/graphic-designers/' + str(i))
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
		for localElement in sets['graphic-design']:
			if color['name'] != '' and color['name'] == localElement['name']:
				found_same_name = True

		if not found_same_name:
			sets['graphic-design'].append(color)

for i in range(1, 2):
	html = urlopen('https://www.numerosamente.it/pantone-list/fashion-and-interior-designers/' + str(i))
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
		for localElement in sets['fashion-design']:
			if color['name'] != '' and color['name'] == localElement['name']:
				found_same_name = True

		if not found_same_name:
			sets['fashion-design'].append(color)


for i in range(1, 2):
	html = urlopen('https://www.numerosamente.it/pantone-list/industrial-designers/' + str(i))
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
		for localElement in sets['product-design']:
			if color['name'] != '' and color['name'] == localElement['name']:
				found_same_name = True

		if not found_same_name:
			sets['product-design'].append(color)

result = open('./pantone.json', 'w')
json.dump(sets, result, indent=4)
