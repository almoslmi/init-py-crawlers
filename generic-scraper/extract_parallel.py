import urllib2
from lxml import etree
from bs4 import BeautifulSoup
import csv
import os
import shutil
import pp
import logging
import datetime
import json

def parallel_extract(start_index, end_index):
	import json
	import extract
	
	files = os.listdir('data_files')
	g = open('config.json', 'r')
	config_str = g.read()
	config = json.loads(config_str)

	for filename in files[start_index:end_index]:
		print filename
		extractor = extract.DataExtract(config, filename)
		extractor.parse_doc()

if __name__ == '__main__':
	logging.basicConfig(filename='parallel.log', 
				level=logging.DEBUG,
			)
	logger = logging.getLogger(__name__)

	logger.info('Start Time: %s'%(str(datetime.datetime.now())))
	
	files = os.listdir('data_files')
	total_files = len(files)

	start_val = 0
	end_val = total_files

	total_process = raw_input("total no. of parallel process you want:")
	each_slot =  int(float(total_files)/float(total_process))

	print "each slot:"+str(each_slot)
	job_server = pp.Server(secret='dummy')
	job_server.set_ncpus(int(total_process))

	start = 420000
	counter  = 0

	proc = []
	sub_param = []

	for i in range(int(total_process)):
		sub_param = []
		print "process no." + str(counter +1) + " started"

		start_index = int(start_val) + (int(each_slot)*i)
		end_index = start_index + int(each_slot)
	  
		sub_param.append(int(start_index))
		sub_param.append(int(end_index))
		sub_param.append(str(i))
		proc.append(sub_param)

		counter = counter + 1

		print sub_param
		print proc

	jobs = []
	for process in proc:
		logger.info("%s, %s, Time : %s"%('PROCESS', str(process), str(datetime.datetime.now())))
		jobs.append(job_server.submit(parallel_extract, (process[0],process[1])))

	for job in jobs:
		print job()
	
	logger.info('End Time: %s'%(str(datetime.datetime.now())))