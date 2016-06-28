import os
from bs4 import BeautifulSoup
import re
import csv
cnew = csv.writer(open('clinical_trial.csv','wb+'))
cnew.writerow(["File-Name","Emails"])
try:
    for filename in os.listdir('C:\\Users\\Acer\\Desktop\\UT\\clinical_trials\\htmls'):
        try:
            plain_text = open('C:\\Users\\Acer\\Desktop\\UT\\clinical_trials\\htmls\\'+filename,'r').read()
            # plain_text=f.read
            match = re.findall(r"[\w\.-]+@[\w\.-]+", plain_text)
            print 'h'
            for em in match:
                try:
                    print filename
                    print em
                    cat = em.decode('utf-8').encode('latin1','replace')
                    cnew.writerow([filename,cat])
                    print cat
                except Exception, e:
                    pass
        except Exception, ex:
            pass
except Exception, e:
    pass