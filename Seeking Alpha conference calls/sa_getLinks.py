from bs4 import BeautifulSoup as Soup
import requests 
import excelHelper
import csv
from multiprocessing import Pool
import multiprocessing 
import json
import datetime

base_url =  'http://seekingalpha.com/analysis/transcripts/all/'
headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
c = csv.writer(open("link_list.csv","w+"))
demo_url  = "http://seekingalpha.com/analysis/transcripts/all/1"
res = requests.get(demo_url,headers=headers)
	#print res.text
response  = res.json()
total_pages  = response['page_count']
print total_pages
#total_pages = 3



for i in range(1,total_pages):
	try:
		url  = base_url + str(i)
		res = requests.get(url,headers=headers)
		#print res.text
		response  = res.json()
		#response = json.loads(response)
		#print response['html'].encode('utf8')

		soup = Soup(response['html'].encode('utf8'))

		total_items = soup.find_all('li')
		print len(total_items)
		

		for items in total_items:
			#print items
			try:
				title_a = items.find('a',{'class':'article_title'})
				#print title_a
				article_link = title_a['href'].encode('utf8','replace')

				article_source = title_a['sasource']
				
				article_title = title_a.text.encode('ascii','replace')
				#print article_title
			

				date_div =  items.find('div',{'class':'date show-hide-info'})
				if date_div:
					author = date_div.find_all('a')[-2].text.encode('ascii','replace')

					author_link = date_div.find_all('a')[-2]['href'].encode('ascii','replace')


					date = date_div.text
					date = date.replace(author,'')
					date = date.replace('Comment!','')
					date = date.encode('ascii','replace')
					date = date.replace('?','')
					date = date.strip()

					dt = ' '.join(date.split()[1:]).split('Comment')[0]
					
					#dt_cl = dt.split('AM')[0]
					#dt_cl = dt.split('PM')[0]
					
					if 'PM' in dt:
						dt = dt.split('PM')[0] +"PM"
					if 'AM' in dt:
						dt = dt.split('AM')[0] +"AM"
					#print dt
					company_ticker = date.split()[0]
					
					day = dt.split(',')[0]
					day_time = dt.split(',')[1]
					if day.lower() == 'today':
						dt_date = str(datetime.datetime.now().date())
						
						day_date =datetime.datetime.strptime(dt_date, "%Y-%m-%d").strftime("%d-%m-%Y") + day_time
						day_date = datetime.datetime.strptime(day_date, "%d-%m-%Y %I:%M %p").strftime("%d-%m-%Y %H:%M")
					elif day.lower() == "yesterday":
						dt_date = str((datetime.datetime.now().date()) - datetime.timedelta(1))
						day_date = datetime.datetime.strptime(dt_date, "%Y-%m-%d").strftime("%d-%m-%Y") + day_time
						day_date = datetime.datetime.strptime(day_date,"%d-%m-%Y %I:%M %p").strftime("%d-%m-%Y %H:%M")
					else:
						#print dt
						try:
							day_date = datetime.datetime.strptime(dt, "%a, %b. %d, %I:%M %p").strftime("%d-%m-2014 %H:%M")
							#print day_date
						except:
							day_date = datetime.datetime.strptime(dt, "%b. %d, %Y, %I:%M %p").strftime("%d-%m-%Y %H:%M")
							#print day_date
					print day_date
							
				else:
					date = "na"
					author = "na"
					author_link = "na"




				summary = items.find('span',{'class':'analysis_summary'})
				if summary:

					summary = summary.text.encode('ascii','replace')
					summary = summary.replace('?','')
					summary = summary.strip()
				else:
					summary = "na"

				c.writerow([article_title,article_link,article_source.strip(),author,author_link,day_date,company_ticker.strip()])
			except Exception,e:
				print str(e)
				continue
	except Exception,e:
		print str(e),":", res.text





