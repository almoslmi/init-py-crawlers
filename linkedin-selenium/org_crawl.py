import requests
from bs4 import BeautifulSoup
import csv
import glob
import re
import traceback
# import dbHandler
from db_handle import dbHandler 

def csv_writer(filename,info):
	write_item = csv.writer(open(filename,"ab+"))
	write_item.writerow(info)


def parser():
	
	db=dbHandler()
	connectionArr=db.dbConn("localhost","root","root","mukund_chari")
	con=connectionArr[0]
	cur=connectionArr[1]
	data=db.select_db(cur,"organization_details","org_name='Additional Organizations'")
	for k in data:
		ccid=str(k[0])
		lid=str(k[0])
		filename = open("consolidated\\"+str(k[0])+".html",'rb')
		html_content = filename.read()
		filename.close()
		soup = BeautifulSoup(html_content,'html.parser')
			
		#organization
		try:
			all_org_div = soup.findAll('div',{'id':re.compile('organization-.*-view')})
			#all_exp_div = soup.find('div',{'id':'experience-482311328'})
			#print 'Number of organization',len(all_org_div)
			exper =[]
			i=0

			for div in all_org_div:
				i+=1
				#print "#",i

				org=[]
				
				org.append(ccid)
				org.append(lid)
				#final_div = div.find('div',{'id':re.compile('experience-*')})
				final_div=div
				try:
					org_name = final_div.find('h4').text.encode('utf-8','replace')
					#print title
				except:
					org_name = "NA"

				if str(org_name)=='Additional Organizations':

					try:
						title = final_div.find('p').text.encode('utf-8','replace')
						#print title
					except:
						title = "NA"


					set_update={'org_name':org_name+': '+title}
					# print set_update
					db.update_db(con,cur,"organization_details",set_update,"ccid="+str(k[0])+" and org_name='Additional Organizations'")



					
		except Exception, e:
			print "hkg",traceback.format_exc()


parser()







