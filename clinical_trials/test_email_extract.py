import requests
from bs4 import BeautifulSoup
import codecs
import re
import csv
toUtf8=codecs.getencoder('UTF8')

def clinical_trials(page):
	url="http://ctri.nic.in/Clinicaltrials/pmaindet2.php?trialid="+str(page)
	source_code=requests.get(url)
	plain_text=source_code.text
	match = re.findall(r'[\w\.-]+@[\w\.-]+', plain_text)
	# match=np.unique(match)
 	# f = open('clinical_trial.csv','rb+')
	# c =  csv.reader(f)
	cnew = csv.writer(open('clinical_trial.csv','wb+'))
	for em in match:
	 	print em
		cat = em.decode('utf-8').encode('latin1','replace')
		cnew.writerow([cat])
		print cat
 	
clinical_trials(3)