import requests
from bs4 import BeautifulSoup

homepage = requests.get('https://www.justia.com/')
g = open('categories.text', 'w')
soup = BeautifulSoup(homepage.text)

categories_div = soup.find('div', id ='research')

# print categories_div

categories = categories_div.findAll('strong')

for i in categories:
	link = 'https://www.justia.com' + i.find('a')['href']
	t = (i.text.strip(), link)
	g.write(str(t) + '\n')
	print i.text