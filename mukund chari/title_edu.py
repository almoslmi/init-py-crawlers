import glob
from db_handle import dbHandler
import traceback
from bs4 import BeautifulSoup

db=dbHandler()
connectionArr=db.dbConn("localhost","root","root","innovaccer")
con=connectionArr[0]
cur=connectionArr[1]


list_of_files = glob.glob("search_pages\\"+"*.html")
	
for files in list_of_files:
	filename = open(files,'rb')
	nm=filename.name
	nm=nm[len("search_pages\\"):]
	nm=nm[:nm.find('.html')]	
	key=nm.split('-')[1]
	nm=nm.split('-')[0]

	# print key

	html_content = filename.read()
	filename.close()
	soup = BeautifulSoup(html_content,'html.parser')

	liList = soup.findAll('li',{'class':'result'})
	# print "length of records",len(liList)
	for lis in liList:
		try:
			pro_id=lis.get('data-li-entity-id')
			# pro_h3=lis.find('div',{'class','bd'}).find('h3').find('a')
			# # print pro_h3
			# pro_link=pro_h3.get('href') 	
			pro_tit=lis.find('div',{'class','bd'}).findAll('div',{'class','description'})
			title=""
			if len(pro_tit)!=0:
				title=pro_tit[0].text
			# loctn=""
			# pro_loc=lis.find('div',{'class','bd'}).findAll('dl',{'class','demographic'})
			# if len(pro_loc)!=0:
			# 	loctn=pro_loc[0].find('dd').text
			# pro_str_nm=pro_h3.findAll('strong')
			# pro_name=""
			# for nm in pro_str_nm:
			# 	pro_name=pro_name+nm.text+" "


			past_text= ""
			summary_text= ""
			current_text= ""
			education_text=""

			snip=lis.find('dl',{'class','snippet'})



			if snip:


				past= snip.find('dt',text='Past')
				summary= snip.find('dt',text='Summary')
				current= snip.find('dt',text='Current')
				education= snip.find('dt',text='Education')

				if past:
					past_text=past.findNext('dd').text
					# print past_text
				if summary:
					summary_text=summary.findNext('dd').text
					# print summary_text
				if current:
					current_text=current.findNext('dd').text
					# print current_text
				if education:
					education_text=education.findNext('dd').text
					# print education_text



			set_update={'past':past_text, 'current': current_text, 'summary':summary_text, 'education': education_text,'current_title':title}
			db.update_db(con,cur,"linkedin_lawyer_output",set_update,"linkedin_id="+str(pro_id))
			# print "id= "+pro_id
			# print "title= "+title
			# print "edu="
			# record.append({"id":str(pro_id),"link":pro_link,"name":pro_name,"title":title,"location":loctn,"profile_get":"success"})
		except Exception,e:
			raise