import shutil
import glob
import os
import time
import urllib2
import csv
import xlrd
import xlwt
from selenium import webdriver 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys 
from bs4 import BeautifulSoup as Soup
import selenium.webdriver.support.ui as ui
#import beautifullsoup
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()

count=3
# destfolder = './dump2/'
srcfolder = './dump1/'

chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

chrome_profile = webdriver.ChromeOptions()
profile = {"download.default_directory": "./dump1",
           "download.prompt_for_download": False,
           "download.directory_upgrade": True,
           "plugins.plugins_disabled": ["Chrome PDF Viewer"]}
chrome_profile.add_experimental_option("prefs", profile)

#Helpful command line switches
# http://peter.sh/experiments/chromium-command-line-switches/
chrome_profile.add_argument("--disable-extensions")

browser = webdriver.Chrome(chromedriver,chrome_options=chrome_profile)
                               # desired_capabilities=dc)


wait = ui.WebDriverWait(browser,30)

login_url = 'https://shibboleth.nyu.edu/idp/Authn/UserPassword'
#accept_button = browser.find_element_by_xpath('/html/body/div[2]/div/div[1]/a')
#print accept_button
#accept_button.click()
driver = browser.get(login_url)
print"erer"
username ='sb5225'
print username
wait.until(lambda driver: driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/a").is_displayed())
accept_button = browser.find_element_by_xpath('/html/body/div[2]/div/div[1]/a')
#print accept_button
accept_button.click()
wait.until(lambda driver: driver.find_element_by_xpath("//*[@id='netid']").is_displayed())
elem = browser.find_element_by_xpath("//*[@id='netid']") # Find the query box 
elem.send_keys(username) 
passwd = 'Innovation@123'
ps = browser.find_element_by_id("password") # Find the query box 
ps.send_keys(passwd + Keys.RETURN)
time.sleep(5)
#logiun_url='http://ezproxy.library.nyu.edu:15500/eds/results?sid=75e7c435-8d93-4f48-bf47-4bd9d53cac58%40sessionmgr112&vid=4&hid=122&bquery=color&bdata=JnR5cGU9MCZzaXRlPWVkcy1saXZl'
logiun_url="http://ezproxy.library.nyu.edu:15500/eds/results?sid=05f541cf-fdf9-4a07-84e2-5108acb1657a%40sessionmgr112&vid=7&hid=119&bquery=color&bdata=JmNsaTA9RlQmY2x2MD1ZJnR5cGU9MCZzaXRlPWVkcy1saXZl"

browser.get(logiun_url)
time.sleep(10)
print "a"
aList = []
liList = []
for i in range(200000):
    #Skip Logic
    if i == 0:
        for j in range(700):
            wait.until(lambda driver: driver.find_element_by_class_name('next').is_displayed())
            next1=browser.find_element_by_class_name('next')
            # next1=browser.find_element_by_link_text('Next')
            next1.click()
    #link1 = browser.find_element_by_xpath("//*[@id='resultListControl']/ul/li[27]/div/div/div[2]")
    # liList = browser.find_elements_by_class_name('result-list-li') 
    current_url= browser.current_url
    html = browser.page_source
    # print html
    soup = BeautifulSoup(html)
    soup = Soup(html, 'html.parser')  
    aList = soup.find_all('a', {'class' : 'record-type pdf-ft'})
    print 'a', len(aList)
    for a in aList:
        # print a
        href = a['href']
        print href
        browser.get(href)
        time.sleep(15)
        #To transfer files
        # fileList = glob.glob('/home/jove/Projects/AnatLecher/pdfextracter/dump1')
        # print fileList
        # if fileList:
        #     for f in fileList:
        #         destFile = destfolder + str(count) + '.pdf'
        #         # shutil.move(f, destFile)
        #         print f
        #         print destFile
        #         os.rename(f, destFile)
        #         count += 1



    aList = []
    time.sleep(10)
    browser.get(current_url)
    
    # writerx.writerow([link1])
    # for j in range(i):
    for j in range(2):
        wait.until(lambda driver: driver.find_element_by_class_name('next').is_displayed())
        next1=browser.find_element_by_class_name('next')
        # next1=browser.find_element_by_link_text('Next')
        next1.click()


#print soup
# tableList=soup.find_all('div',{'class':'record-formats-wrapper externalLinks'})
# for table in tableList:
#     a=table.find('a')


# print table1


#t1=soup.find('record-formats-wrapper externalLinks')
#t2=t1.find_all('href').text
#print t2
#print tag
#link2 = soup.find_elements_by_class_name('record-formats-wrapper externalLinks')
#print link2
#for each in link2:
#   link3 = each.find_elements_by_class_name('record-formats-wrapper externalLinks')
#   print link3

#table1=Soup.find('div',{'id':'results-col'})
#print "b"

#table2=Soup.find('div',{'id':'results-container'})
#table3=Soup.find_all('li',{'class':'mod result idx0 company'})
#print table3

#find1=browser.find_element_by_class_name('description hover')
#print find1.text
#print "c"


