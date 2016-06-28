import re
import time
import mechanize
from mechanize import Browser
from datetime import datetime
from random import randint
import cookielib
import traceback
import requests
import dbHandler
import glob
info=[]
info=dbHandler.fetch_link()
# Browser
browser = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
browser.set_cookiejar(cj)

# Browser options
browser.set_handle_equiv(True)
browser.set_handle_gzip(True)
browser.set_handle_redirect(mechanize.HTTPRedirectHandler)
browser.set_handle_referer(True)
browser.set_handle_robots(False)

# User-Agent
browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#Proxies
# browser.set_proxies({"http": "http://218.104.148.59:3128/"})

## For requests
#Proxies
# proxy = {"http": "http://218.104.148.59:3128/"}

# r = requests.get('http://vk.com/search?c[q]=%D0%A7%D0%B5%D1%80%D0%BD%D0%BE%D0%B3%D0%BE%D1%80%D0%B8%D1%8F&c[section]=statuses',headers  ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/28.0'} ,proxies = proxy)
# print r
##

url1 = "https://www.linkedin.com/uas/login?goback=&trk=hb_signin"
#urlu = "https://www.linkedin.com/profile/view?id=273196863&authType=NAME_SEARCH&authToken=wS4H&locale=en_US&srchid=479651031407137652257&srchindex=1&srchtotal=2&trk=vsrp_people_res_name&trkInfo=VSRPsearchId%3A479651031407137652257%2CVSRPtargetId%3A273196863%2CVSRPcmpt%3Aprimary"
res = browser.open(url1)
print res.code

browser.select_form(nr=0)
browser.form["session_key"] = "sandeep@innovaccer.com"
browser.form["session_password"] = "sandeep"
time.sleep(5)
results = browser.submit()
# time.sleep(20)
filename = ".//dump1//afterlogin.html"
f = open(filename,"wb")
f.write(results.read())
f.close()

# for page in range(1,5)
# linkss=["https://www.linkedin.com/profile/view?id=273196863&authType=NAME_SEARCH&authToken=wS4H&locale=en_US&srchid=479651031407137652257&srchindex=1&srchtotal=2&trk=vsrp_people_res_name&trkInfo=VSRPsearchId%3A479651031407137652257%2CVSRPtargetId%3A273196863%2CVSRPcmpt%3Aprimary","https://www.linkedin.com/profile/view?id=83776393&authType=NAME_SEARCH&authToken=niVL&locale=en_US&srchid=479651031407130333489&srchindex=1&srchtotal=1&trk=vsrp_people_res_name&trkInfo=VSRPsearchId%3A479651031407130333489%2CVSRPtargetId%3A83776393%2CVSRPcmpt%3Aprimary","http://www.linkedin.com/profile/view?id=315625372&authType=name&authToken=vLY0&trk=api*a250300*s258157*"]
filelist = glob.glob('./defect1/*.html')
#print filelist
lidList = []
for f in filelist:
    print f[f.find('1\\')+2:]
    lid = f[f.find('-')+1:f.find('.html')]
    #print lid   
    lidList.append(lid.strip())
#print lidList
filelist1 = glob.glob('./dump1/*.html')
print filelist1
lidList1 = []
for f1 in filelist1:
    print f1[f1.find('1\\')+2:]
    lid1 = f1[f1.find('-')+1:f1.find('.html')]
    #print lid1   
    lidList1.append(lid1.strip())
#print lidList1
linkss=["http://www.linkedin.com/profile/view?id=315625372&authType=name&authToken=vLY0&trk=api*a250300*s258157*"]
for i in range(len(linkss)):
    urlu = linkss[i]
    print urlu
    time.sleep(10)
    res = browser.open(urlu)
    time.sleep(5)
    str1='id'
    str2='&a'
    pos_s=urlu.find(str1)
    pos_e=urlu.find(str2)
    if pos_s != -1 :
        l_id=urlu[pos_s+3:pos_e]
        print l_id
        time.sleep(5)
        f = open("./dump1/" +l_id+'.html',"wb")
        f.write(res.read())
        f.close()
    #f = open('./priv_dump/urlu.html',"wb")
    #f.write(res.read())
    #f.close()

info=[]
info=dbHandler.fetch_link()
for i in range(len(info)):
    ccid=info[i][0]
    link= info[i][1]
    print link
    
    str1='id'
    str2='&a'
    pos_s=link.find(str1)
    pos_e=link.find(str2)
    if pos_s != -1 :
        l_id=link[pos_s+3:pos_e]
        print l_id
        if l_id in lidList:
            if l_id in lidList1:
                print "already in dump1"
            else:
               
                urlu = link
                time.sleep(10)
                res = browser.open(urlu)
                time.sleep(5)


                time.sleep(5)
                f = open("./dump1/" + ccid+"-"+l_id+'.html',"wb")
                f.write(res.read())
                f.close()

        else:
            print l_id + ' ignored'

#browser.follow_link(res)


