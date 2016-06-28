import requests
from bs4 import BeautifulSoup
import time
import os

THRESHOLD = 5

categories = ['design', 'tech', 'style', 'travel', 'culture', 'food-drink']

for category in categories:
	g = open(category + '.txt', 'w')
	flag = 0
	error_count = 0

	page_count = 1
	print category
	
	while True:
		g.write(str(page_count) + os.linesep)
		print page_count

		r = requests.get('http://www.coolhunting.com/' + category + '?page=' + str(page_count))
		# print r.text
		soup = BeautifulSoup(r.text)

		divs = soup.findAll('div', {'class': 'article'})
		# print divs
		
		if divs:
			for i in divs:
				header = i.find('h1')
				# print header
				link = header.find('a')
				g.write(link['href'] + os.linesep)
		else:
			break
		
		page_count = page_count + 1
		time.sleep(1)