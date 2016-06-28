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

linF=LinkedinFunctions()
db=dbHandler()
profile = webdriver.FirefoxProfile()
browser = webdriver.Firefox(firefox_profile=profile)
usrnm='9sandeepg@iimahd.ernet.in'
pwd='sandeep'
try:
	browser = linF.link_sign_in(browser,usrnm,pwd)
	time.sleep(4)


	connectionArr=db.dbConn("localhost","root","root","innovaccer")
	con=connectionArr[0]
	cur=connectionArr[1]

	# data=db.select_db(cur,"linkedin_lawyer_output","status_flag=0")
	# print data
	# sql_query="select distinct(linkedin_id) from linkedin_lawyer_output where id>3385"
	# cur.execute(sql_query)
	# data=[]
	# for row in cur.fetchall():
	# 	data.append(row)

	list_of_files = glob.glob("demo_dumps\\"+"*.html")
	
	for files in list_of_files:
		filename = open(files,'rb')
		nm=filename.name
		nm=nm[len("demo_dumps\\"):]
		nm=nm[:nm.find('.html')]
		# print nm
		sze=os.path.getsize(files)

		if sze>100000:
			continue

		sql_query="select linkedin_url from linkedin_lawyer_output where linkedin_id="+nm+" limit 1"
		cur.execute(sql_query)
		data=[]
		for row in cur.fetchall():
			data.append(row)

		# print 
		# exit()
		p_url=(data[0][0]).replace("\\","")
		browser = linF.link_profile(browser,p_url)
		time.sleep(4)
		pageSource = browser.page_source.encode('utf8')
		f = open('demo_dumps//'+nm+'.html',"w")
		f.write(pageSource)
		f.close()
		# set_update={'status_flag':10}
		# db.update_db(con,cur,"linkedin_profile_demo_dump",set_update,"id="+str(k[0]))
except Exception,e:
	raise


