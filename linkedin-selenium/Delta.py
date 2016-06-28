from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import time
import re
import requests
import traceback
from selenium.webdriver.common.action_chains import ActionChains

class getIteration:

    def __init__(self):
        try:
            print "Initiated"
            self.profile = webdriver.FirefoxProfile()
            self.browser = webdriver.Firefox(firefox_profile = self.profile)
            self.wait = ui.WebDriverWait(self.browser,30)
        except Exception,e:
            print traceback.format_exc()

    def sendRequest(self,url):
        print "Sending Request", url
        try:
            r=requests.get(url, headers  ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/28.0'})
            html = r.text.encode('utf8') 
            # print html

        except Exception,e:
            print traceback.format_exc()

    def seleniumInit(self,url,sourceCity,destCity,goingDate,returningDate):
        print "browser init"
        try:
            self.browser.get(url)

            self.wait.until(lambda driver: self.browser.find_element_by_id('originCity').is_displayed())
            #giving input parameters
            fromCity= self.browser.find_element_by_id('originCity')
            fromCity.clear()
            fromCity.send_keys(sourceCity)

            toCity = self.browser.find_element_by_id('destinationCity')
            toCity.clear()
            toCity.send_keys(destCity)

            #DATE mm-dd-yyyy
            depDate= self.browser.find_element_by_id('departureDate')
            depDate.send_keys(goingDate)

            retDate= self.browser.find_element_by_id('returnDate')
            retDate.send_keys(returningDate)

            searchButton= self.browser.find_element_by_id('findFlightsSubmit')
            searchButton.click()
        
        except Exception,e:
            print traceback.format_exc()

    def extractInfo(self, flight):
        values=[]
        #finding flight operator
        #flightOperator= row.find('div',attrs={'class':"operatedByData"})
        #operator='Delta'
        #try:
        #    operator= flightOperator.find('span').text
        #except:
        #    pass
        #print operator

        #flight_no
        flight_no_wrap = flight.find_all('div', attrs={'class':"fltDetailsWrap"})[3]
        # print flight_no_wrap
        flight_no_text = flight_no_wrap.find('div', attrs = {'class':"fltDetailsText"})
        flight_no_html = flight_no_text.find('a', attrs = {'class':"fareFlyout"})
        flight_det_list = flight_no_html.text.encode('utf8').strip().split(' ')
        # print flight_det_list
        flight_no = flight_det_list[0] + ' ' + flight_det_list[1][0:-1]
        print flight_no
        
        #departure and arrival ports
        ports=flight.find_all('a', attrs={'class':"fareFlyout airportCode"})
        src_port= str((ports[0].text)[:3])
        dest_port=str((ports[1].text)[:3])

        #departure and arrival times
        time= flight.find_all('div', attrs={'class':"fltDetailsText"})
        time_src= time[1].text.split(' ')[0]
        time_dest=time[2].text.split(' ')[0]

        values=[src_port, time_src, dest_port, time_dest]
        print values


    #flightTypeCheck
    def getDetails(self, direction):
        try:
            try:
                wait = ui.WebDriverWait(self.browser,30)
                wait.until(lambda driver: driver.find_element_by_id('sortType').is_displayed())
            except:
                print traceback.format_exc()

            print "parsing the page"
            soup=BeautifulSoup(self.browser.page_source)

            flightDetails= soup.find('div', attrs={'id':"itin_summary_columns_tmplHolder"})
            flights= flightDetails.find_all('div', attrs={'class':"resultWrap"})

            flag=0            
            for row in flights:
                #determine flight type- Non Stop or 1 stop
                flag=0

                flightType=str((row.find('div', attrs={'class':"stopType"})).text)
                
                if flightType != 'Nonstop':
                    flag=1

                priceBlock=row.find('div', attrs={'class':"threeColBlockResult bgNonBasicFare_bgNonBasicFareCell"})
                priceButton=priceBlock.find('div', attrs={'class':"priceBtnText"})
                price=str(priceButton.text)
                #print price

                #flight info
                flightInfo= row.find_all('div', attrs={'class':"threeColSlideDownLeft"})
                self.extractInfo(flightInfo[0])

                if flag==1:
                    print "Connecting Flight"
                    self.extractInfo(flightInfo[1])


        except:
            print traceback.format_exc()

            
if __name__=='__main__':

    try:
#       print "reading excel file..."
#       f= xlReader.excelHelper()
#       elements= f.readExcel('data.xlsx', 3,24,0)
#       print "finished reading the file!"
    
#       markets=[]
    
#       for row in elements:
#           markets.append(row[1])
                                        
        #create an object of the class
        objGetI= getIteration()
        dDate='09/15/2014'
        rDate='09/18/2014'

#       source, dest= markets[0].split('-')
        source= 'LGA'
        dest= 'BUF'
#       source='DFW'
#       dest='DFW'
        plStartUrl='http://www.delta.com/'
        x='resultPerPage-departure-lowest'
        y='resultPerPage-return-lowest'
        
        objGetI.seleniumInit(plStartUrl,source,dest,dDate,rDate)
        #departure, put 0 for departure
        print "departure"
        objGetI.getDetails(0)
        
        #objGetI.browser.find_element_by_name('departing').click()
        
        #print
        #print "return"
        #objGetI.getDetails(y,1)

    except Exception,e:
        print traceback.format_exc()