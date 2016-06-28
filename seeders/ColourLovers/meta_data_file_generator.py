# Importing libraries
import requests
from bs4 import BeautifulSoup
import time
import os
import ConfigParser

class WebsiteMetaDataFile:
	def __init__(self, base_page_url):
		self.config = ConfigParser.RawConfigParser()
		self.base_page_url = base_page_url

	def get_last_page(self):
		r = requests.get(self.base_page_url)
		soup = BeautifulSoup(r.text)
		paging = soup.find('div', {'class' : 'paging'})

		last_page_number = int(paging.findAll('a')[-2].text)

		return last_page_number

	def write_to_config_file(self):
		self.config.add_section('Paging')
		last_page_number = self.get_last_page()
		self.config.set('Paging', 'last_page', last_page_number)

		with open('example.cfg', 'wb') as configfile:
		    self.config.write(configfile)

if __name__ == '__main__':
	x = WebsiteMetaDataFile('http://www.colourlovers.com/blog')
	x.write_to_config_file()