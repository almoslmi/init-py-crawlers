from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import traceback


def citations(query):
	search = driver.find_element_by_class_name('search-page-input')
	search.clear()
	search.send_keys(query + Keys.RETURN)

	wait = ui.WebDriverWait(driver,120)
	ulist = driver.find_elements_by_class_name('user-list-meta')
	result = []
	for each in ulist:
		result.append(each.text.replace("\n", "|").replace("Joined on ",""))
		result.append("##")
	wait = ui.WebDriverWait(driver,300)
	return result
			
if __name__ == '__main__':
	GITHUB_UNAME = 'rajul'
	GITHUB_PASS = 'p1234567'
	profile = webdriver.FirefoxProfile()
	driver = webdriver.Firefox(firefox_profile=profile)

	login = 'https://github.com/login'
	driver.get(login)
	print "login successful"

	un = driver.find_element_by_id("login_field")
	un.send_keys(GITHUB_UNAME)
	pun = driver.find_element_by_id("password")
	pun.send_keys(GITHUB_PASS + Keys.RETURN)
	print "keys send"

	login_url = "https://github.com/search?q=random&ref=searchresults&type=Users"
	driver.get(login_url)

	fout = open("result.txt","w")
	error = open("error.txt","w")
	with open("data.csv") as data:
		reader = csv.reader(data)
		count = 0
		for rox in reader:
			count += 1
			print count
			if count > 1000:
				if count%25 == 0:
					print "Waiting"
					time.sleep(150)
				try:
					name = rox[2]
					query = name.strip()
					res = citations(query)
					res = [str(x) for x in res]
					res = "|".join(res)
					fout.write(query + "|" + res + "\n")
				except:
					error.write(query + "\n")
					continue
