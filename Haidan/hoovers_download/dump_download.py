import requests
import csv
import traceback
import re
import codecs
import sys
import time
from multiprocessing import Pool, Manager
import math
import time
import os

headers  ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/28.0'}


def extract_info(start_index,end_index,queue):
    print "in process"
    counter = 0
    start_time = time.time()
    fp=open('error2.txt','rU')
    companies=list(fp.readlines())
    fp.close()

    for i in range(start_index,end_index):
        try:
            queue.put("1")
            print str(queue.qsize())+"    "+str(time.time()-start_time)
            company=companies[i]
            company1=str(company).strip()
            company=str(company).strip().replace(' ','%20').replace('(','%28').replace(')','%29').replace('&','%26').replace('!','%21').replace('!','%21').replace('+',' ').replace('-',' ').replace('/',' ').replace(","," ")
            link='http://www.hoovers.com/company-information/company-search.html?term='+company
            pr=requests.get(link,headers=headers)
            time.sleep(1)
            prtxt=pr.text.encode('utf-8','ignore')
    
            fp=open('dumps4\\'+str(i)+'.html','w')
            fp.write(str(prtxt))
            fp.close()
        except Exception,e:
            traceback.print_exc()
            fp=open('error3.txt','a')
            fp.write(str(company1)+'\n')
            fp.close()
        

    


if __name__=='__main__':
    fp=open('error2.txt','rU')
    companies=fp.readlines()
    fp.close()

    total_processes = 2
    pool = Pool(total_processes)
    total_files = len(list(companies))
    print total_files
    each_slot = total_files/total_processes
    start_index = 0
    end_index = 0
    manager = Manager()
    queue = manager.Queue()
    for i in range(total_processes):
        end_index += each_slot
        if i == total_processes - 1:
            end_index = total_files
        try:
            print pool.apply_async(extract_info,(start_index,end_index,queue))
        except Exception,e:
            print str(e)
        start_index += each_slot
    #time.sleep(10)
    pool.close()
    pool.join()
    

    


