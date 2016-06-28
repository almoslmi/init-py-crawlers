import os
import re
import MySQLdb
try:
    con = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test_db')
    for filename in os.listdir('C:\\Users\\Acer\\Desktop\\UT\\clinical_trials\\htmls'):
        try:
            plain_text = open('C:\\Users\\Acer\\Desktop\\UT\\clinical_trials\\htmls\\'+filename,'r').read()
            match = re.findall(r"[\w\.-]+@[\w\.-]+", plain_text)
            for em in match:
                try:
                    print filename
                    print em
                    cat = em.decode('utf-8').encode('latin1','replace')
                    cur = con.cursor()
                    cur.execute('INSERT INTO mails (file_name,email) values (%s,%s)',(filename,cat))
                    con.commit()
                    print cat
                except Exception, e:
                    raise
        except Exception, ex:
            raise
    
    con.close()
except Exception, e:
    raise