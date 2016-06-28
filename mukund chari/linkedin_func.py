import selenium.webdriver.support.ui as ui
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import traceback
from bs4 import BeautifulSoup
class LinkedinFunctions:
	def link_sign_in(self,browser,usrnm,pwd):
		try:
			linkedin_url='https://www.linkedin.com/uas/login?goback=&trk=hb_signin'
			browser.get(linkedin_url)
			username = usrnm
			passwd = pwd

			elem = browser.find_element_by_id("session_key-login")
			elem.send_keys(username)

			ps = browser.find_element_by_id("session_password-login")
			ps.send_keys(passwd + Keys.RETURN)
			return browser
		except Exception,e:
			print "Error"

	def link_search(self,browser,key,fname,lname,countryCode):
		try:
			search="https://www.linkedin.com/vsearch/p?keywords="+key+"&firstName="+fname+"&lastName="+lname+"&openAdvancedForm=true&locationType=I&countryCode="+countryCode+"&rsid=479651031412160400834&orig=MDYS"
			browser.get(search)
			time.sleep(3)
			return browser
		except Exception,e:
				print "Error",e
				print traceback.format_exc()

	def link_profile(self,browser,l_url):
		try:
			browser.get(l_url)
			time.sleep(4)
			# self.wait.until(lambda driver: self.browser.find_element_by_id('background').is_displayed())
			# self.wait.until(lambda driver: self.browser.find_element_by_id('background').is_displayed())
			return browser
		except Exception,e:
				print "Error",e
				print traceback.format_exc()

	def link_search_parse(self,browser):
		try:
			r_count =browser.find_element_by_id("results_count")
			res_count=r_count.text[0]
			record=[]
			# print "no of results",res_count
			if res_count == '0':
				record.append({"profile_get":"failure"})
			else:
				# print res_count
				srch_results = browser.find_element_by_class_name("search-results")
				html= srch_results.get_attribute("outerHTML")
				soup = BeautifulSoup(html)
				liList = soup.findAll('li',{'class':'result'})
				# print "length of records",len(liList)
				for lis in liList:
					try:
						pro_id=lis.get('data-li-entity-id')
						pro_h3=lis.find('div',{'class','bd'}).find('h3').find('a')
						# print pro_h3
						pro_link=pro_h3.get('href') 	
						pro_tit=lis.find('div',{'class','bd'}).findAll('div',{'class','description'})
						title=""
						if len(pro_tit)!=0:
							title=pro_tit[0].text
						loctn=""
						pro_loc=lis.find('div',{'class','bd'}).findAll('dl',{'class','demographic'})
						if len(pro_loc)!=0:
							loctn=pro_loc[0].find('dd').text
						pro_str_nm=pro_h3.findAll('strong')
						pro_name=""
						for nm in pro_str_nm:
							pro_name=pro_name+nm.text+" "
						# print "title= "+title
						record.append({"id":str(pro_id),"link":pro_link,"name":pro_name,"title":title,"location":loctn,"profile_get":"success"})
					except Exception,e:
						pass
			return record

		except Exception,e:
			raise