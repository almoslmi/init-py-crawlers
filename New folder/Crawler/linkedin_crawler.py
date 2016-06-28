from bs4 import BeautifulSoup as Soup
from time import time
import MySQLdb
import requests
import json
import re
import os
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys
#import excelHelper
#import dbHandler
import time
#import CreateCSV
import multiprocessing 
from multiprocessing import Pool
import random
import urllib
import csv
import traceback
import dbHandler
import glob
import selenium.webdriver.support.ui as ui


#profile = webdriver.FirefoxProfile()

browser = webdriver.Firefox()
def open_browser():

    filelist = glob.glob('./Defect/*.html')
    print filelist
    lidList = []
    for f in filelist:
        print f[f.find('\\')+1:]
        lid = f[f.find('-')+1:f.find('.html')]
        print lid   
        lidList.append(lid.strip())
    print lidList

    linkedin_url='https://www.linkedin.com/uas/login?goback=&trk=hb_signin'
    browser.get(linkedin_url)
    username = 'sandeep@innovaccer.com'
    passwd = 'sandeep'
    try:
        elem = browser.find_element_by_id("session_key-login")
        elem.send_keys(username)

        ps = browser.find_element_by_id("session_password-login")
        ps.send_keys(passwd + Keys.RETURN)
    except Exception,e:
        print "Error"

    
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
                
            
                #print link[6]
                search_url=link
                time.sleep(5)
                browser.get(search_url)
                html_source=browser.page_source
                #print html_source
               
                html_linkedin =(open("./Dump/" + ccid+"-"+l_id+'.html','wb+'))
                html_linkedin.write(html_source.encode('utf8','replace'))
            else:
                print l_id + ' ignored'



        
    
        

open_browser()