import string
import requests
from bs4 import BeautifulSoup
import nltk
import nltk.data






f=open('stopwords.txt','w')

stopwords = set(nltk.corpus.stopwords.words())
for sw in stopwords:
	try:
		f.write(sw+",")
	except:
		pass
f.close()
exit()
source_code=requests.get("http://www.thehindu.com/todays-paper/cm-expresses-concern-over-extensive-damage-to-crops/article6505031.ece")
html=source_code.text
soup = BeautifulSoup(html,'html.parser')
art=soup.find('div',{'class':'article-body'})
article_text=""
article_head=soup.find('h1',{'class':'detail-title'}).text.encode("utf-8")

if art!=None:
	for pp in art.findAll('p',{'class':'body'}):
		article_text=article_text+(pp.text)
else:
	art=soup.find('div',{'class':'article-text'})
	for pp in art.findAll('p',{'class':'body'}):
		article_text=article_text+(pp.text)

if article_text.strip()=="":
	article_text="No Body To Display"
	
if article_text!="No Body To Display":
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	sentences=sent_detector.tokenize(article_text)
	title=[]
	title_text=article_head.replace("-"," ")
	title_temp=title_text.split()

	for tt in title_temp:
		if tt not in stopwords:
			title.append(string.lower(tt))
	# print title
	print set(article_text)