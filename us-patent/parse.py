import csv
import traceback
from bs4 import BeautifulSoup
import glob

count = 0
valList = ()
# dump files
list_of_files = glob.glob("patent_dumps_new\\"+"*.html")
print len(list_of_files)
for files in list_of_files:
	try:
		count += 1
		filename = open(files,'rb')
		html_content = filename.read()
		filename.close()
		soup = BeautifulSoup(html_content,'html.parser')
		try:
			patent_id = soup.title.text
			patent_id = patent_id[patent_id.rfind(":")+1:].strip()
		except Exception,ex:
			raise

		# attribute extraction
		issue_date="-"
		us_class="-"
		cpc_class="-"
		international_class="-"

		date_tr=soup.find('td',text='Issue Date:')
		if date_tr:
			issue_date=date_tr.findNext('td').text.strip()

		us_class_tr=soup.find('td',text='Current U.S. Class:')
		if us_class_tr:
			us_class=us_class_tr.findNext('td').text.strip()

		cpc_class_tr=soup.find('td',text='Current CPC Class: ')
		if cpc_class_tr:
			cpc_class=cpc_class_tr.findNext('td').text.strip()
		
		international_class_tr=soup.find('td',text='Current International Class: ')
		if international_class_tr:
			international_class=international_class_tr.findNext('td').text.strip()
		
		# insert into db
		ins_values={"patent_id":patent_id.encode('utf-8'),"issue_date":issue_date.encode('utf-8'),"current_us_class":us_class.encode('utf-8'),"current_cpc_class":cpc_class.encode('utf-8'),"current_international_class":international_class.encode('utf-8')}
		# db.insert_db(con,cur,"patent_dump",ins_values)
		if count >= 1000:
			with open('patent_out.csv','ab+') as outf:
				writer = csv.writer(outf)
				writer.writerows(valList)
			valList = (ins_values.values(),)
		else:
			valList += (ins_values.values(),)

	except Exception,e:
		print traceback.format_exc()
