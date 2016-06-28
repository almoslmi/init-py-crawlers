from bs4 import BeautifulSoup as Soup
from time import time
import MySQLdb
import requests
import json
import re
import os
# import excelHelper
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
# import dbHandler as db 
import glob
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains

#profile = webdriver.FirefoxProfile()
profile = webdriver.FirefoxProfile()
browser = webdriver.Firefox(firefox_profile=profile)

# def open_browser():
try:
	linkedin_url='https://www.linkedin.com/uas/login?goback=&trk=hb_signin'
	browser.get(linkedin_url)
	username = 'sandeep@innovaccer.com'
	passwd = 'sandeep'

	elem = browser.find_element_by_id("session_key-login")
	elem.send_keys(username)

	ps = browser.find_element_by_id("session_password-login")
	ps.send_keys(passwd + Keys.RETURN)
except Exception,e:
		print "Error"
keywords=["law, attorney"]
for key in keywords:
	try:

		search="https://www.linkedin.com/vsearch/p?keywords="+key+"&firstName=PHILIP&lastName=KIER&openAdvancedForm=true&locationType=I&countryCode=us&rsid=479651031412160400834&orig=MDYS"
		browser.get(search)
		time.sleep(2)
		r_count =browser.find_element_by_id("results_count")
		res_count=r_count.text[0]
		print "no of results",res_count
		if res_count == '0':
			print "no result"
			#rowcounter+=1
		else:
			print res_count
	except Exception,e:
			print "Error",e
			print traceback.format_exc()
# open_browser()