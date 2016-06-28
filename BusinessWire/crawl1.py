import requests
from bs4 import BeautifulSoup
import csv

def csv_writer(filename,info):
	write_item = csv.writer(open(filename,"ab+"))
	write_item.writerow(info)

def saver():
	url="http://www.library.hbs.edu/databases/completelist.html"
	source_code=requests.get(url)
	plain_text=source_code.text
	fw=open("lister.html",'w')
	fw.write(plain_text.encode('utf-8'))
	fw.close()


def parser():
	i=1
	while i<=39:
		filename = open("Dump\\dump-page"+str(i)+".html",'rb')
		html_content = filename.read()
		filename.close()
		soup = BeautifulSoup(html_content,'html.parser')
		for link in soup.findAll('h3'):
			name=[(link.find('a').text).encode("utf-8"),link.find('a').get('href')]

			# print name
			csv_writer("name_list.csv",name)
		i=i+1
# csv_writer("name_list.csv",["article-title","article-link"])
# parser()












# soup=BeautifulSoup(plain_text)
# for link in soup.findAll('h3'):
# 	name=[link.find('a').text]
# 	print name
	# csv_writer("name_list.csv",name)
	

