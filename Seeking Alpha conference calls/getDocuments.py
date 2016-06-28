from bs4 import BeautifulSoup as Soup
import requests 
import excelHelper
import csv
from multiprocessing import Pool
import multiprocessing 



def getCalls(params):
	
	#for rows in csv.reader(open(workbook_name,"r+")):
	try:
		links = params[0]
		pid = str(params[1])
		fname = "992_"+pid+".csv"
		c = csv.writer(open(fname,"w+"))
		for rows in links:
			try:
				link = rows[4]
				date = rows[3]
				cik = rows[2]
				company_name = rows[0]
				#print link
				res = requests.get(link)
				soup = Soup(res.text)
				table = soup.find('table',{'class':'tableFile'})

				all_rows = table.find_all('tr')

				for row in all_rows:
					all_divs = row.find_all('td')
					c = 0
					for divs in all_divs:
						c +=1
						if divs.text == "EX-99.2":
							print "found xoxo:",cik
							c.writerow(rows)
				print "not found :(",cik
			except Exception,e:
				print str(e)
				continue
	except Exception,e:
		print str(e)



if __name__=='__main__':
	start_page = raw_input("Enter start index:")
	end_page = raw_input("Enter end index:")
	if end_page < start_page:
	    end_page = raw_input("end page can't be less  that start indes Enter again:")
	total_process = raw_input("total no. of parallel process you want:")
	total_page =  int(end_page) - int(start_page)
	each_slot =  int(float(total_page)/float(total_process))
	print "each slot:"+str(each_slot)
	workbook_name =  '8k_links.csv'
	

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
	    pool.apply_async(  getCalls, args = (process, ))
	pool.close()
	pool.join()