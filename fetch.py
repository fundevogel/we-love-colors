from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


def fetchOneSet(baseUrl, firstPage, lastPage, setName):
   
	for i in range(firstPage, lastPage+1):
		html = urlopen(baseUrl + str(i))
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

fetchOneSet('https://www.numerosamente.it/pantone-list/graphic-designers/',1,32,'graphic-design') 
fetchOneSet('https://www.numerosamente.it/pantone-list/fashion-and-interior-designers/',1,14,'fashion-design')
fetchOneSet('https://www.numerosamente.it/pantone-list/industrial-designers/',1,10,'product-design')


result = open('./pantone.json', 'w')
json.dump(sets, result, indent=4)
