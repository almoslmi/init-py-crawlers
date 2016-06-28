import BeautifulSoup
import re
import csv
import MySQLdb
import glob
import os
import traceback
import shutil
from multiprocessing import Pool, Manager
import time


def parseprivate(source):
    p=re.compile('privcapId=[0-9]+')
    lst=p.findall(source)
    writerB=csv.writer(file('1PrivateCompanyId.csv','ab'))
    #fp=open('PrivateID.txt','a')
    for each in lst:
        each=str(each).strip()
        writerB.writerow([each])
        #fp.write(each+'\n')


def parsepublic(source):
    writerB=csv.writer(file('1PublicCompanyInfo.csv','ab'))
    soup=BeautifulSoup.BeautifulSoup(source)
    raw1=soup.find('table',{'class':'table', 'width':'100%', 'cellspacing':'0','cellpadding':'0'})
    raw3=raw1.findAll('tr')
    #print raw3
    for i in range(len(raw3)):
        each=raw3[i]
        if i==0:
            continue
        txt=each.text.encode('utf-8')
        if 'No matches' in txt:
            continue
        raw4=each.findAll('td')
        #print raw4
        ticker=raw4[0].text.encode('utf-8')
        link=raw4[0].find('a')['href']
        name=raw4[1].text.encode('utf-8')
        exchange=raw4[2].text.encode('utf-8')
        country_code=raw4[3].text.encode('utf-8')
        details=[ticker,link,name,exchange,country_code]
        writerB.writerow(details)


def extract_info(files,start_index,end_index,queue):
    print "in process"
    counter = 0
    start_time = time.time()
    writerB=csv.writer(file('HooversComplete.csv','ab'))
    for i in range(start_index,end_index):
        queue.put("1")
        print str(queue.qsize())+"    "+str(time.time()-start_time)
        try:
            filename=str(files[i]).split('\\')[1]
            fp=open(files[i],'rU')
            source=fp.read()
            fp.close()
            
            soup=BeautifulSoup.BeautifulSoup(source)
            try:
                raw1=soup.find('div',{'class':'cmp-company-directory'})
                raw2=raw1.find('tbody')
                raw1=raw2.findAll('tr')
                for each in raw1:
                    try:
                        raw2=each.findAll('td')
                        name=raw2[0].text.encode('utf-8','ignore').replace('&nsb;','')
                        address=raw2[1].text.encode('utf-8','ignore').replace('&nsb;','')
                        #print name,address
                        writerB.writerow([name,address])
                    except Exception,e:
                        continue
            
            except Exception,e:
                traceback.print_exc()
                fp=open("errorfilesPublicComplete.txt","a")
                fp.write(str(files[i])+'\n')
                fp.close()
            
        except Exception,e:
            fp=open("errorfilesPublicComplete.txt","a")
            fp.write(str(files[i])+'\n')
            fp.close()
            traceback.print_exc()



if __name__=='__main__':

    files=list(glob.glob("dumps2\\*.*"))
    files2=list(glob.glob("dumps3\\*.*"))
    files3=list(glob.glob("dumps4\\*.*"))
    files=files+files2+files3
    print len(files)
    #print len(files)
    total_processes = 1
    pool = Pool(total_processes)
    total_files = len(files)
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
            print pool.apply_async(extract_info,(files,start_index,end_index,queue))
        except Exception,e:
            print str(e)
        start_index += each_slot
    #time.sleep(10)
    pool.close()
    pool.join()




