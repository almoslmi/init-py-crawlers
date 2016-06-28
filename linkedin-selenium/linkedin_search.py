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
chromedriver = "c:/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
usrnm='9sandeepg@iimahd.ernet.in'
pwd='sandeep'
try:
	browser = linF.link_sign_in(browser,usrnm,pwd)
	countryCode="us"

	time.sleep(4)
	connectionArr=db.dbConn("localhost","root","root","innovaccer")
	con=connectionArr[0]
	cur=connectionArr[1]

	data=db.select_db(cur,"linkedin_lawyer_input1","status_flag=0")

	# print data
	keywords = ['patent law','patent lawyer','patent attorney','patent counsel','patent agent']
	for (innovaccer_id,lawyer_id,name,freq,status_flag) in data:
		# print innovaccer_id
		if(name.find(" ")!=-1):
			fname=name[:(name.find(" "))]
			lname=name[(name.rfind(" ")+1):]
		else:
			fname=name
			lname=""
		for key in keywords:
			
			browser = linF.link_search(browser,key,fname,lname,countryCode)
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
			f = open('new_search_pages//'+str(innovaccer_id)+'-'+key+'.html',"wb")
			f.write(pageSource)
			f.close()
			record=linF.link_search_parse(browser)
			for rec in record:
				if(rec['profile_get']=='failure'):
					pass
				else:
					# print rec['title']
					ins_values={"innovaccer_id":str(innovaccer_id),"lawyer_id":str(lawyer_id),"name":name,"keyword":key,"linkedin_id":rec["id"],"linkedin_url":rec["link"],"linkedin_name":rec["name"],"current_title":rec["title"],"current_location":rec['location'],"status_flag":str(0)}
					db.insert_db(con,cur,"linkedin_lawyer_output1",ins_values)

					# cur,tbl_nm,set_update,whre)
		set_update={'status_flag':1}
		db.update_db(con,cur,"linkedin_lawyer_input1",set_update,"innovaccer_id="+str(innovaccer_id))
except Exception,e:
	raise


