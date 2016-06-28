import requests
from bs4 import BeautifulSoup
import time
import os
import json

g = open('trendhunter.txt', 'w')

page_count = 1

while True:
	print page_count

	r = requests.get('http://www.trendhunter.com/magazine-new-ajax?page=' + str(page_count) + '&var1=&var2=&var3=0&view=magazine&type=trends&score=0&search=&ajax=true&action=getContent')
	json_formatted = json.loads(r.text)

	data_from_json = json_formatted['data'].encode('utf-8')
	
	soup = BeautifulSoup(data_from_json)

	links = soup.findAll('a')
	# print "LINKS:"
	# print links
	# print
	# print

	if links[0]['href'] == 'http://www.trendhunter.com/trendreports':
		exit()
				
	if links:
		count = 0
		for link in links:
			count = count + 1
			if 'href' in link.attrs.keys():
				if link['href'] == 'http://www.trendhunter.com/trendreports':
					break
				else:
					print link['href']
					g.write(link['href'] + os.linesep)
	else:
		break

	page_count = page_count + 1
	time.sleep(1)