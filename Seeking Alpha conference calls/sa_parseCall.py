from bs4 import BeautifulSoup as Soup
import requests 
import excelHelper
import csv
from multiprocessing import Pool
import multiprocessing 
import sa_dbHandler as dbHandler
import time
import math
import traceback
import datetime

base_url =  'http://seekingalpha.com/'
headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}






def parseCall(params):

	
	total_links = params[0]

	for links in total_links:
		try:
			url = base_url + links[1]
			res = requests.get(url,headers=headers)
			print res
			soup = Soup(res.text.encode('utf8','replace'))
			ticker_div = soup.find('span',{'id':'about_primary_stocks'})
			if ticker_div:
				ticker_symbol = ticker_div.text
				company_name = ticker_div.find('a')['title'].encode('utf8','replace').strip()
			else:
				continue
			#datetime_of_call = links[5]
			datetime_of_call = datetime.datetime.strptime(str(links[5]), "%d-%m-%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
			date_div  = soup.find('div',{'class':'article_info_pos'})
			if date_div:
				date_txt = date_div.find_all('span')[0].text
				timezone = date_txt.split()[-1]
			else:
				timezone = "na"
				
				

				#quarter = "Q"+ str(int(math.ceil(float(month)/3)))
				
			quarter = links[0].encode('latin-1','replace')
			
			if 'Q1' in quarter or 'F1Q' in  quarter:
				quarter = 'Q1'
			elif 'Q2' in quarter or 'F2Q' in  quarter:
				quarter = 'Q2'
			elif 'Q3' in quarter or 'F3Q' in  quarter:
				quarter = 'Q3'
			elif 'Q4' in quarter or 'F4Q' in  quarter:
				quarter = 'Q4'
			else:
				print quarter
				quarter = 'na'




			



			participants_div = soup.find('div',{'id':'article_participants'})


			participants = []

			if participants_div:
				all_rows = participants_div.find_all('p')
				counter = 0
				
				for rows in all_rows:
					if rows.text.strip() == 'Executives':
						ex_pointer = counter
					elif rows.text.strip() =='Analysts':
						an_pointer = counter
					counter +=1
				executives = all_rows[ex_pointer:an_pointer]
				analysts = all_rows[an_pointer:]
				for ex in executives:
					ex_text = ex.text.encode('latin-1','replace')
					try:
						ex_name = ex_text.split('-')[0]
						ex_position = ex_text.split('-')[1]
					except Exception,e:
						#print str(e)
						if ex_text.strip() <> "Executives":
							ex_name = ex_text.split('?')[0]
							ex_position = ex_text.split('?')[-1]
						else:
							continue
					if ex_name.strip() <> '' and ex_name.strip() <> 'Analyst':
						participants.append([ex_name,company_name,ex_position,"executive"])
				for an in analysts:
					an_text = an.text.encode('latin-1','replace')
					try:
						an_name = an_text.split('-')[0]
						an_position = an.text.split('-')[1]
					except Exception,e:
						#print str(e)
						if an_text.strip() <> "Analysts":
							an_name = an_text.split('?')[0]
							an_position = an_text.split('?')[-1]
						else:
							continue
							
					if an_name.strip() <> '' and an_name.strip() <> 'Analyst' :
						participants.append([an_name,an_position,"Analyst","analysts"])


			content_div = soup.find('div',{'id':'article_content'})

			qna_div = soup.find('div',{'id':'article_qanda'})

			p_changeovers_index = []
			q_changeovers_index = []
			total_p_change = 0
			total_q_change = 0
			all_p  = []
			all_q = []

			counter = 0

			if content_div:
				p_changeovers = content_div.find_all('strong')
				if len(p_changeovers) > 0:
					
					total_p_change = len(p_changeovers) -1 
				else:
					total_p_change = len(p_changeovers)
				all_p = content_div.find_all('p')
				
			counter = 0
			presentation_changeover =0

			for p in all_p:
				if p.find('strong') and p.text.strip()<>'' and len(p.text.strip())<60: 
					p_changeovers_index.append(counter)
					presentation_changeover +=1
				counter +=1 
			
			if presentation_changeover >0 :
				presentation_changeover = presentation_changeover -1
				
			
			#presentation_changeover = counter

			


			if qna_div:
				q_changeovers = qna_div.find_all('strong')
				if len(q_changeovers) > 0:
					total_q_change = len(q_changeovers) -1 
				else:
					total_q_change = len(q_changeovers)
				all_q = qna_div.find_all('p')
				
			counter = 0
			qna_changeover = 0

			for q in all_q:
				if q.find('strong') and q.text.strip()<>'' and len(q.text.strip())<60:
					q_changeovers_index.append(counter)
					qna_changeover +=1
				counter +=1 
			#qna_changeover = counter
			
			if qna_changeover >0 :
				qna_changeover = qna_changeover -1
				
				
				
				

			#presentation_changeover = total_p_change

			#qna_changeover = total_q_change






			ticker_symbol = ticker_symbol.split('(')[1].split(')')[0]
			call_id = dbHandler.enterMasterDetails(ticker_symbol,company_name,quarter,datetime_of_call,timezone,presentation_changeover,qna_changeover)

			
			for participant in participants:
				try:
					participant_name = unicode(participant[0]).encode('latin-1','replace')
					participant_org = unicode(participant[1]).encode('latin-1','replace')
					participant_designation = unicode(participant[2]).encode('latin-1','replace')
					participant_type = unicode(participant[3]).encode('latin-1','replace')
					dbHandler.enterParticipantsDetails(call_id,participant_name,participant_org,participant_designation,participant_type)
				except Exception,e:
					print str(e)
					continue

			'''counter = 0

			for p in all_p:
				if p.find('strong') and p.text.strip()<>'' and len(p.text.strip())<60: 
					p_changeovers_index.append(counter)
				counter +=1 

			counter = 0

			for q in all_q:
				if q.find('strong') and q.text.strip()<>'' and len(q.text.strip())<60:
					q_changeovers_index.append(counter)
				counter +=1 '''


			changeover_data = []

			for ci in range(len(p_changeovers_index)):

				index = p_changeovers_index[ci]
				try:
					next_index = p_changeovers_index[ci+1]
				except:
					next_index = len(all_p)
				speaker_name = all_p[index].text
				speaker_content = ''
				for i in range(index,next_index):
					speaker_content = speaker_content + all_p[i].text.encode('latin-1','replace')
				speaker_content =  speaker_content.replace(speaker_name.encode('latin-1','replace'),'')
				changeover_data.append([speaker_name,speaker_content])

			for ci in range(len(q_changeovers_index)):
				index = q_changeovers_index[ci]
				try:
					next_index = q_changeovers_index[ci+1]
				except:
					next_index = len(all_q)
				speaker_name = all_q[index].text
				speaker_content = ''
				for i in range(index,next_index):
					speaker_content = speaker_content + all_q[i].text.encode('latin-1','replace')
				speaker_content =  speaker_content.replace(speaker_name.encode('latin-1','replace'),'')
				if 'Question-and-Answer Session' not in speaker_name.strip():
					changeover_data.append([speaker_name,speaker_content])


			for cd in changeover_data:
				name_of_speaker = cd[0].encode('latin-1','replace')
				speaker_text = cd[1]
				dbHandler.enterChangeoverDetails(call_id,name_of_speaker,speaker_text)
		except Exception,e:
			print str(e)
			print  traceback.print_exc()







if __name__=='__main__':
	start_page = raw_input("Enter start index:")
	end_page = raw_input("Enter end index:")
	if end_page < start_page:
	    end_page = raw_input("end page can't be less  that start indes Enter again:")
	total_process = raw_input("total no. of parallel process you want:")
	total_page =  int(end_page) - int(start_page)
	each_slot =  int(float(total_page)/float(total_process))
	print "each slot:"+str(each_slot)
	workbook_name =  'link_list.csv'
	

	full_data = list( csv.reader(open(workbook_name,"r+")))
	print len(full_data)
	full_data = full_data[:int(end_page)]

	#filename = 'proxylist.csv'
	#reader = csv.reader(open(filename, "rb"), delimiter = ',')
	#for row in reader:
	 #   proxies.append(row[0])

	#proxies = ['115.25.216.6:80','42.121.16.222:8092','221.176.14.72:80','119.233.255.60:80','124.95.165.250:80','123.134.95.131:80','61.152.108.187:82','118.195.65.243:80']
	start = 420000
	counter  = 0
	#proxy = random.choice(proxies)
	#pool = Pool(processes=int(total_process))
	#pool.map(crawl_page,(proxy,))
	pool = Pool(processes=int(total_process))
	#pool.map(crawl_page,(proxy,))
	proc = []
	sub_param = []

	for i in range(int(total_process)):
	        sub_param = []
	        counter +=1 
	        print "process no." + str(counter) + " started"
	        #proxy['http'] = proxies[counter]
	        start_index = int(start_page) + (int(each_slot)*i)
	        end_index = start_index + int(each_slot)

	        #effective_list = total_vals[start_index:end_index]
	        sub_param.append(full_data[start_index:end_index])
	        sub_param.append(counter)
	        proc.append(sub_param)
	        #end_index = sub_parts[counter+1] 
	        #p = multiprocessing.Process(target=crawl_page, args=(proxy,start_index,end_index))
	        #p.start()
	        #proc.append(p)
	        #counter +=1

	for process in proc:
	    pool.apply_async(   parseCall, args = (process, ))
	pool.close()
	pool.join()