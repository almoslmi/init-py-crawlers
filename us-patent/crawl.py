import requests
from bs4 import BeautifulSoup
import csv
import traceback

def csv_writer(filename,info):
	write_item = csv.writer(open(filename,"ab+"))
	write_item.writerow(info)

def saver(i,limit):
	try:
		while(i<=limit):
			patentNum = str(i)
			lenPatent = len(str(i))
			if lenPatent == 6:
				patentNum = '0' + patentNum
			# print patentNum
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
			# proxy = {'http' : 'http://217.12.113.114:8080'}
			url="http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&d=PALL&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.htm&r=1&f=G&l=50&s1="+patentNum+".PN.&OS=PN/"+patentNum+"&RS=PN/"+patentNum
			# source_code=requests.get(url,headers = headers, proxies=proxy) 
			source_code=requests.get(url,headers = headers) 
			plain_text=source_code.text
			fw=open("patent_dumps_new\\"+patentNum+".html",'w')
			fw.write(plain_text.encode('utf-8'))
			fw.close()
			i=i+1
	except Exception,e:
		print traceback.format_exc()

# def parser():
# 	filename = open("lister.html",'rb')
# 	html_content = filename.read()
# 	filename.close()
# 	soup = BeautifulSoup(html_content,'html.parser')
# 	for link in soup.findAll('h3'):
# 		name=[link.find('a').text]
# 		# print name
# 		csv_writer("name_list.csv",name)

saver(747187,2228000)

# soup=BeautifulSoup(plain_text)
# for link in soup.findAll('h3'):
# 	name=[link.find('a').text]
# 	print name
	# csv_writer("name_list.csv",name)
	

