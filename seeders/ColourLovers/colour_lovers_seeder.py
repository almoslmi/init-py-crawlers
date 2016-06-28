# Importing libraries
import requests
from bs4 import BeautifulSoup
import time
import os

# This shall create a file in the current directory for saving the seeds
g = open('colour_lovers_seeds.txt', 'w')

# Identifying the last page_number
r = requests.get('http://www.colourlovers.com/blog')
soup = BeautifulSoup(r.text)
paging = soup.find('div', {'class' : 'paging'})

last_page_number = int(paging.findAll('a')[-2].text)

# Last processed page number
h = open('last_processed_page.txt', )
exit()

page_count = 1

while True:
	print page_count

	r = requests.get('http://www.colourlovers.com/blog?page=' + str(page_count))
	soup = BeautifulSoup(r.text)

	divs = soup.findAll('div', {'class': 'padded-bordered-content'})
	
	if divs:
		for i in divs:
			header = i.find('h1')
			link = header.find('a')
			g.write(link['href'] + os.linesep)
	else:
		break
	
	page_count = page_count + 1
	time.sleep(1)
