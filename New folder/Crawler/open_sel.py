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
    counter=0
    

    filelist = glob.glob('C:/Users/Acer/Desktop/code/linkedin code/2.Crawler/Mechanize/dump1/*.html')
    print filelist
    for f in filelist:
    	lidList = []
    
        ccid=  f[f.find('\\')+1:f.find('-')]
        print ccid
        lid = f[f.find('-')+1:f.find('.html')]
        print lid   
        lidList.append(lid.strip())
    
    	fi= "file:///"+f
    	browser.get(fi)
        time.sleep(10)
        html_source=browser.page_source
        
        html_linkedin =(open("./2sept_ver2_Dump/" + ccid+"-"+lid+'.html','wb+'))
        #html_linkedin =(open("dump.html",'wb+'))
        html_linkedin.write(html_source.encode('utf8','replace'))
        

open_browser()
print "done"
