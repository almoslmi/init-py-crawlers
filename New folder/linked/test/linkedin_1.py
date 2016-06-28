import re
import time
import mechanize
from mechanize import Browser
from datetime import datetime
from random import randint
import cookielib
import traceback
import requests
import glob
info=[]
# info=dbHandler.fetch_link()
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
urlu="https://www.linkedin.com/vsearch/p?keywords=law%20&firstName=PHILIP&lastName=KIER&openAdvancedForm=true&locationType=I&countryCode=us&rsid=479651031412160400834&orig=MDYS"

res = browser.open(url1)
print res.code

browser.select_form(nr=0)
browser.form["session_key"] = "sandeep@innovaccer.com"
browser.form["session_password"] = "sandeep"
time.sleep(5)
results = browser.submit()
res = browser.open(urlu)
# red_source = res.read()
# p=re.compile('(https://www.linkedin.com/profile/view?id)(.*?)"')
# redlink = p.search(red_source)
# mod_source = red_source.replace("<input",",a").replace("value=","href=")
for link in browser.links():
    # ln=
    if link.base_url[:len("https://www.linkedin.com/profile/view?id")]== "https://www.linkedin.com/profile/view?id" :
        print link.base_url
    else:
        pass