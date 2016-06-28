import requests
from bs4 import BeautifulSoup
import time
import os
from TorCtl import TorCtl

def request(url):
    def _set_urlproxy():
        proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
    _set_urlproxy()
    request=urllib2.Request(url, None, headers)
    return urllib2.urlopen(request).read()

def get_new_id():
    conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase="innovaccer@123")
    print "Connection : " , conn
    conn.send_signal("NEWNYM")

g = open('etsy_seeds.txt', 'w')

page_count = 1

while True:
	print page_count

	get_new_id()

	r = requests.get('https://www.etsy.com/in-en/search?q=&page=' + str(page_count))
	soup = BeautifulSoup(r.text)

	divs = soup.findAll('div', {'class': 'listing-card'})
	
	if divs:
		for i in divs:
			link = i.find('a')
			g.write(link['href'] + os.linesep)
	else:
		break
	
	page_count = page_count + 1
	time.sleep(1)