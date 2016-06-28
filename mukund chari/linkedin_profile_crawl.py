import requests
import re
import os
import time
import urllib
import glob
import selenium.webdriver.support.ui as ui
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from linkedin_func import LinkedinFunctions
from db_handle import dbHandler
from bs4 import BeautifulSoup
linF=LinkedinFunctions()
db=dbHandler()
# profile = webdriver.FirefoxProfile()
# browser = webdriver.Firefox(firefox_profile=profile)
# usrnm='9sandeepg@iimahd.ernet.in'
# pwd='sandeep'

chromedriver = "c:/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
usrnm='9sandeepg@iimahd.ernet.in'
pwd='sandeep'

try:
	browser = linF.link_sign_in(browser,usrnm,pwd)
	time.sleep(4)


	connectionArr=db.dbConn("localhost","root","root","innovaccer")
	con=connectionArr[0]
	cur=connectionArr[1]

	data=db.select_db(cur,"linkedin_lawyer_output","status_flag=0 group by linkedin_id order by id")
	# # print data
	# sql_query="SELECT * FROM innovaccer.linkedin_lawyer_output where status_flag=0 group by linkedin_id order by id"
	# cur.execute(sql_query)
	# data=[]
	# for row in cur.fetchall():
	# 	data.append(row)

	
	for k in data:
		p_url = k[6].replace("\\","")
		# print p_url
		# break
		browser = linF.link_profile(browser,p_url)
		time.sleep(4)
		pageSource = browser.page_source.encode('utf8')
		soup = BeautifulSoup(pageSource,'html.parser')
		# print soup.findAll('h1')[0].text 
		try:
			if (soup.findAll('h1')[0].text=='LinkedIn is Momentarily Unavailable'):
				print 'LinkedIn is Momentarily Unavailable'
				exit()
		except Exception, e:
			sp=''

		f = open('profile_dumps//'+str(k[5])+'.html',"wb")
		f.write(pageSource)
		f.close()
		set_update={'status_flag':10}
		db.update_db(con,cur,"linkedin_lawyer_output",set_update,"id="+str(k[0]))
except Exception,e:
	raise


