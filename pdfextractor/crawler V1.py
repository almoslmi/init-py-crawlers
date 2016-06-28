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
# import excelHelper
count=0
# workbook1=[]
# workbook_name='abc.xlsx'
# start_index='0'
# end_index='0'
# workbook1=excelHelper.excelHelper().readExcel(workbook_name,start_index,end_index)
#     #f2=open('excel_ca4.txt','w') #open file in write mode and auto generated file

f3=open("output_link_new5.csv","w") #save link file###########################################################################
writerx=csv.writer(f3)
folder = './dump'

# chromedriver = "./chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver
# browser = webdriver.Chrome(chromedriver)
# browser.set_preference("browser.download.folderList",2)
# browser.set_preference("browser.download.manager.showWhenStarting",True)
# browser.set_preference("browser.download.dir",'/home/jove/AnatLecher/pdfextracter/dump')
# browser.set_preference("browser.helperApps.neverAsk.saveToDisk","application/pdf")
# browser.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
# browser.set_preference("pdfjs.disabled", True)
# browser.set_preference("browser.helperApps.neverAsk.saveToDisk","application/pdf")

#Firefox Driver
# fp = webdriver.FirefoxProfile()
# fp.set_preference("browser.download.folderList",2)
# fp.set_preference("browser.download.manager.showWhenStarting",True)
# fp.set_preference("browser.download.dir",folder)
# fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/pdf")
# fp.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
# fp.set_preference("pdfjs.disabled", True)
# fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/pdf");
# browser = webdriver.Firefox(firefox_profile=fp)

#Chrome Driver
# dc = DesiredCapabilities.CHROME
# dc['loggingPrefs'] = {'browser': 'ALL'}

chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

chrome_profile = webdriver.ChromeOptions()
profile = {"download.default_directory": "./dump",
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
# chromedriver = "./chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver
# browser = webdriver.Chrome(chromedriver)

# url1='https://www.google.co.in/'
# browser.get(url1)
# browser.sendKeys(Keys.CONTROL +"t")
# browser.get('https://facebook.com')

# exit()

# profile = webdriver.FirefoxProfile()
# browser = webdriver.Firefox(firefox_profile=profile)
login_url = 'https://shibboleth.nyu.edu/idp/Authn/UserPassword'
#accept_button = browser.find_element_by_xpath('/html/body/div[2]/div/div[1]/a')
#print accept_button
#accept_button.click()
driver = browser.get(login_url)
print"erer"
username ='sb5225'
print username
accept_button = browser.find_element_by_xpath('/html/body/div[2]/div/div[1]/a')
#print accept_button
accept_button.click()

elem = browser.find_element_by_xpath("//*[@id='netid']") # Find the query box 
elem.send_keys(username) 
passwd = 'Innovation@123'
ps = browser.find_element_by_id("password") # Find the query box 
ps.send_keys(passwd + Keys.RETURN)
time.sleep(5)
#logiun_url='http://ezproxy.library.nyu.edu:15500/eds/results?sid=75e7c435-8d93-4f48-bf47-4bd9d53cac58%40sessionmgr112&vid=4&hid=122&bquery=color&bdata=JnR5cGU9MCZzaXRlPWVkcy1saXZl'
logiun_url="http://ezproxy.library.nyu.edu:15304/eds/results?sid=e9dfcd5b-f165-4104-b399-17fc1e83341e%40sessionmgr4001&vid=6&hid=4203&bquery=color&bdata=JmNsaTA9RlQmY2x2MD1ZJnR5cGU9MCZzaXRlPWVkcy1saXZl"

browser.get(logiun_url)
time.sleep(10)
print "a"
aList = []
liList = []
for i in range(200000):
    #link1 = browser.find_element_by_xpath("//*[@id='resultListControl']/ul/li[27]/div/div/div[2]")
    liList = browser.find_elements_by_class_name('result-list-li') 
    if liList:
        for li in liList:
            try:
                a = browser.find_element_by_class_name('record-type')
                if a:
                    aList.append(a)
                    a.text
            except Exceptions,e:
                print "a Not found"
    # if i == 1 or i == 0:
    #     current_url = "http://ezproxy.library.nyu.edu:15304/eds/results?sid=d6444e5e-3730-4101-bcc8-d30eb8316a0c%40sessionmgr4001&vid=11&hid=4111&bquery=color&bdata=JnR5cGU9MCZzaXRlPWVkcy1saXZl"
    # else:
    #     current_url= browser.current_url
    current_url= browser.current_url
    print 'a', len(aList)
    if aList:
        hrefList = []
        for a in aList:
            # print "entering main loop"
            #get handle of current main window
            #main_window = browser.current_window_handle
            #print a.get_attribute('href')
            pdf= a.get_attribute('href')
            print pdf
            hrefList.append(pdf)
    print 'href', len(hrefList)
    # if hrefList:
    #     for href in hrefList:
    #         browser.get(href)
        
    #         time.sleep(10)
                # break
            #browser.find_element_by_id('downloadLink').click()
            #time.sleep(5)


            #browser.switch_to_window(main_window)
            #print "focus shifted"

            #print a.text
            # count=count+1
    aList = []
    hrefList = []  
    time.sleep(10)
    browser.get(current_url)
    
    # writerx.writerow([link1])
    # for j in range(i):
    for j in range(2):
        wait.until(lambda driver: driver.find_element_by_class_name('next').is_displayed())
        next1=browser.find_element_by_class_name('next')
        # next1=browser.find_element_by_link_text('Next')
        next1.click()

# html = browser.page_source
#print html

# soup = BeautifulSoup(html)
# soup = Soup(html)  
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


