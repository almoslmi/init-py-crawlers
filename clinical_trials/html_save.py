import requests
from bs4 import BeautifulSoup
import codecs
toUtf8=codecs.getencoder('UTF8')

def clinical_trials(max_pages):
	page=1
	while page <= max_pages:
		try:
			url="http://ctri.nic.in/Clinicaltrials/pmaindet2.php?trialid="+str(page)
			source_code=requests.get(url)
			plain_text=source_code.text
			ch=0
			try:
				po=plain_text.index('Invalid Request!!!')
			except Exception, ex:
				# print 'check it'
				ch=1
			if ch==1:
				fw=open("htmls\\trialid="+str(page)+".html",'w')
				fw.write(plain_text.encode('utf-8'))
				fw.close()
				print "done"+str(page)
			else:
				print "skipped"+str(page)
		except Exception, e:
			print "err"+str(page)
			# raise
		page+=1

clinical_trials(10050)