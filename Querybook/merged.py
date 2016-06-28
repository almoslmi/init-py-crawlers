'''
More tolerance - more results, more flexible, less accurate (line 188)

Notes: multiprocessing may generally not show error, to debug: put the suspected code in
try:
    ..
except e:
    print str(e) 

To run the code without UI,comment the lines 325 to 330 and uncomment 332 to 340

Result file is generated in same location as code
'''


import os
import csv
import bz2
import time
import multiprocessing
import multiprocessing.pool
import math
from sys import argv
import logging
#Creates the parent process as non-daemon
class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess


#Returns the time valeu for record
def totime(record):
    return int(record[25:29].encode('hex'),16)


#Searches for all recrods with Symbol in given time range    
def binary_search(seq, start, end, symbol,tt):
    
    records = []
    size = 69
    min_element = 0
    max_element = (len(seq)/69) - 1
   
   #Basic Binary Search
    while True:

        min_record = seq[size*min_element:size*min_element+size]
        max_record = seq[size*max_element:size*max_element+size]      

        if totime(max_record) < totime(min_record):
            return []

        mid = (min_element+max_element)/2
        mid_record = seq[size*mid:size*mid+size]

        if totime(mid_record) < start:
            min_element = mid + 1

        elif totime(mid_record) > end:
            max_element = mid - 1

        elif totime(mid_record) >= start and totime(mid_record) <= end:
            if mid_record[10:21].encode('hex').strip('0') == symbol:
                records.append(mid_record)
                       

            #Sequentially checks the prior and next records of the record found
            #for all records lying in the given range with the mentioned symbol     
            p = mid - 1
            prev = seq[size*p:size*p+size]
            try:
                while totime(prev) >= start and totime(prev) <= end and p>=0:
                    if prev[10:21].encode('hex').strip('0') == symbol:
                        records.append(prev)
                       
                    p -= 1
                    prev = seq[size*p:size*p+size]
            except Exception,e:
                a = 2
            n = mid + 1
            nex = seq[size*n:size*n+size]
            
            try:
                while totime(nex) >= start and totime(nex) <= end and n<=max_element:
                    if nex[10:21].encode('hex').strip('0') == symbol:
                        records.append(nex)
                        
                    n += 1
                    nex = seq[size*n:size*n+size]
            except  Exception,e:
                a = 2
                
            return records

#Custom adaptive fleixble search algorithm
#Returns records at the given time inmterval with adjustable tolerance(flexibility) of results 
def search(data,start_index,seek_time,temp_index,seeker,tolerance,iterations,lastflag):
    
    if iterations < 10000:
        if int(math.fabs(totime(data[temp_index]) - seek_time)) <= tolerance:
            return [data[temp_index],temp_index]
        elif iterations > 10 and (math.fabs(totime(data[temp_index]) - totime(data[start_index])) <= tolerance or math.fabs(totime(data[temp_index]) - totime(data[start_index]))==lastflag):
            return [None,None]
        else:
            if temp_index >= len(data):
                temp_index = len(data) - 1

        
            if totime(data[temp_index])-totime(data[start_index]) == 0:
                
                temp_index += 20
                if temp_index >= len(data) - 1:
                    temp_index = len(data) - 1
                    
                
            try:
                seeker = int(math.ceil(seeker * (seek_time - totime(data[temp_index]))/(totime(data[temp_index])-totime(data[start_index]))))
            except:
                seeker = seeker + 10

            if seeker == 0:
                seeker = 1

            if temp_index + seeker > len(data) - 1:
                new_seek = len(data) -  1
            elif temp_index + seeker < 0:
                new_seek = 0
            else:
                new_seek = temp_index + seeker
            
               
            return search(data,temp_index,seek_time,new_seek,seeker,tolerance,iterations + 1,math.fabs(totime(data[temp_index]) - totime(data[start_index])))
   
    else:
        return [None,None]


#Processes the records for each date broken down into chunks
def mapper(i,slots,total_processes,symbol,start,end,date,freq,file_name,tt,code_path):
    
    p_no = i
    # try:
    f = bz2.BZ2File(file_name)

    #Checks if each chunk lies in the time range
    f.seek(i*slots*69)
    start_chunk = f.read(69)

    st_time = totime(start_chunk)
    f.seek(i*slots*69+(69*slots)-69)
    end_chunk = f.read(69)
    end_time = totime(end_chunk)

    # print 'chunk',p_no,'timings:',st_time,end_time
    pid = os.getpid()
    if st_time > end:
        return []
    if end_time < start:
        return []
        

    f.seek(i*slots*69)
    chunk = f.read(slots*69)
    orig_symbol = symbol
    symbol=symbol.encode('hex').strip('0')
    
    #Retreives records in time range with the ticker symbol
    records = binary_search(chunk,start,end,symbol,tt)
    print 'records',len(records)
    # except Exception,e:
    #     print str(e)


    if len(records) > 0:
        records.sort()

        final = [records[0]]
        i = 1
        while(totime(records[i]) == totime(records[0])):
            final.append(records[i])
            i += 1

        timestamp = totime(records[i - 1])
        end_record = records[-1]

        #Searches in records for desired time interval
        flag = i - 1

        #tolerance of time match is set to half of frequency in order to get one data point for each time desired
        tolerance = freq/2 + 1
      
        #self adapative search which works faster on sorted array of data
        while(timestamp <=  totime(end_record) and flag+1 < len(records)):

            timestamp = timestamp+freq
            
            element,new_flag = search(records,flag,timestamp,flag+1,1,tolerance,10,math.fabs(totime(records[flag+1]) - totime(records[flag])))
           
            if element:
                final.append(element)
                try:
                    i = 1
                    while math.fabs(totime(records[new_flag]) - totime(records[new_flag - i]) <= tolerance): 
                        final.append(records[new_flag - i])
                        i -= 1
                except:
                    z = 1
                try:
                    i = 1
                    while math.fabs(totime(records[new_flag]) - totime(records[new_flag + i]) <= tolerance): 
                        final.append(records[new_flag + i])
                        i += 1
                except:
                    z = 1
                flag = new_flag
            else:
                flag += 1
            
    else:
        print 'no records'
    final.sort()
    print 'final',len(final)
    
    #Writes results to individual file
    r = open(code_path+'results/'+str(date)+'_'+str(p_no)+'.csv','wb')
    writer = csv.writer(r)
    for corrected_data in final:
        msgSeqNum =str(int(corrected_data[0:4].encode('hex'),16))
        MsgType =str(int(corrected_data[4:6].encode('hex'),16))
        SendTime =str(int(corrected_data[6:10].encode('hex'),16))
        MsgSize =str(int(corrected_data[21:23].encode('hex'),16))
        SecurityIndex=str(int(corrected_data[23:25].encode('hex'),16))
        starTime = str(totime(corrected_data))
        souceTimeMicro =str(int(corrected_data[29:31].encode('hex'),16))
        QuoteCondition=str(int(corrected_data[31:32].encode('hex'),16))
        TradingStatus=corrected_data[32:33]
        SourceSeqNumber=str(int(corrected_data[33:37].encode('hex'),16))
        SourceSessionId=str(int(corrected_data[37:38].encode('hex'),16))
        PriceScaleCode=str(int(corrected_data[38:39].encode('hex'),16))
        PriceNumerator=str(int(corrected_data[39:43].encode('hex'),16))
        Volume=str(int(corrected_data[43:47].encode('hex'),16))
        ChgQty=str(int(corrected_data[47:51].encode('hex'),16))
        NumOrders=str(int(corrected_data[51:53].encode('hex'),16))
        Side= str(corrected_data[53:54])
        Filler1= str(corrected_data[54:55])
        ReasonCode=str(corrected_data[55:56])
        Filler2=str(corrected_data[56:57])
        LinkID1=str(int(corrected_data[57:61].encode('hex'),16))
        LinkID2=str(int(corrected_data[61:65].encode('hex'),16))
        LinkID3=str(int(corrected_data[65:69].encode('hex'),16))
        
        row = [date,orig_symbol,starTime,msgSeqNum,MsgType,SendTime,MsgSize,SecurityIndex,souceTimeMicro,QuoteCondition,TradingStatus,SourceSeqNumber,SourceSessionId,PriceScaleCode,PriceNumerator,ChgQty,Volume,NumOrders,Side,Filler1,ReasonCode,Filler2,LinkID1,LinkID2,LinkID3]
        
        writer.writerow(row)
           
#Searches for file in each given date
def pass_data_to_search(symbol,path,start_time_seconds,end_time_seconds,date,time_interval,tt,code_path):

    jobs=[]
    dic_files={}
    lis=[]
    slot_results=[]
    
    file_name = path+'b'+date+'.l.bz2'
    # file_name = path + date+'/'+dic_files[lis[index]]+'.bz2'
        
    size=os.path.getsize(file_name)
    total_rows=size/69
    total_processes1=40
    slots=total_rows/total_processes1

    #Multiprocessing each file as chunk
    # mapper(0,slots,total_processes1,symbol,start_time_seconds,end_time_seconds,date,time_interval,file_name,tt,code_path)
    # mapper(1,slots,total_processes1,symbol,start_time_seconds,end_time_seconds,date,time_interval,file_name,tt,code_path)
    
    pool = multiprocessing.Pool(total_processes1)
    

    for i in range(total_processes1):

        pool.apply_async(mapper, args = (i,slots,total_processes1,symbol,start_time_seconds,end_time_seconds,date,time_interval,file_name,tt,code_path))
        
    pool.close()
    pool.join()    

if __name__ == "__main__":

    #SET LOGGER FOR MAINTAINING LOGS
    # logpath = 'query.log'
    # logfile = open(logpath,'a')

    # logging.getLogger('').handlers = []

    # logging.getLogger().setLevel(logging.DEBUG)
    # fh = logging.FileHandler(logpath)
    # fh.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(message)s')
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)
    # logging.basicConfig(filename=logpath,format='%(asctime)s %(message)s',filemode='a',level=logging.DEBUG)

    code_path = '/home/ubuntu-0001/anant/lyle/datas/'
    openbook_path = '/home/ubuntu-0001/anant/lyle/datas/'
    # code_path = '/kellogg/data/nyse/EQY_US_NYSE_BOOK_AGGR/'
    # openbook_path = '/kellogg/data/nyse/EQY_US_NYSE_BOOK_AGGR/'
    #Step 1 - REMOVING TEMPORARY FILES
    try:
        os.remove(code_path+'finalresult_all.csv')
    except:
        pass
    try:
        os.system('rm '+code_path+'results/*')
    except:
        pass
    try:
        os.system('rm '+code_path+'final/*')
    except:
        pass

    #STEP 2 - PARSING INPUT ARGUMENTS
    script_name,entered_text,date_list,from_hours,from_min,from_sec,to_hours,to_min,to_sec,time_interval = argv

    # print entered_text,from_hours,from_min,from_sec,to_hours,to_min,to_sec,time_interval,date_list
        
    entered_text = entered_text.split(',')
    date_list = date_list.split(',')
    time_interval = int(time_interval)

    total_seconds=(int(to_hours)-int(from_hours))*3600*1000+(int(to_min)-int(from_min))*60*1000+(int(to_sec)-int(from_sec))*1000+(int('0')-int('0'))
    
    start_time_seconds= int(from_hours)*3600*1000+int(from_min)*60*1000+int(from_sec)*1000+int('0')
    end_time_seconds= int(to_hours)*3600*1000+int(to_min)*60*1000+int(to_sec)*1000+int('0')        
    # print 'test'
    # print entered_text,from_hours,from_min,from_sec,to_hours,to_min,to_sec,time_interval,date_list

    # logstring = 'Time of Query: ' + time.asctime( time.localtime(time.time()) ) + '; Time Interval: ' + time_interval + '; Start Time: ' + start_time_seconds + '; End Time: ' + end_time_seconds + '; Ticker Symbols: ' + entered_text + '; Dates: ' + date_list

    # logfile.write(logstring)

    print '----------'
    print 'time_interval',time_interval
    print 'start_time',start_time_seconds
    print 'end_time',end_time_seconds
    print 'symbol',entered_text
    print 'date',date_list
    print 'path',openbook_path

    if not os.path.exists(code_path+'results'): os.makedirs(code_path+'results')
    if not os.path.exists(code_path+'final'): os.makedirs(code_path+'final')
    

    #STEP 3 - QUERYING DATA USING MAPPER
    try:
        for date in date_list:

            openbook_path = openbook_path+'EQY_US_NYSE_BOOK_AGGR_'+date[:4]+'/'

            for i in range(len(entered_text)):
                
                start = time.time()
                pass_data_to_search(entered_text[i],openbook_path,start_time_seconds,end_time_seconds,date,time_interval,time.time(),code_path)

                os.system("cat "+code_path+"results/*.csv > "+code_path+"final/"+date+"_"+str(i)+".csv")
                
                with open(code_path+'final/'+date+'_'+str(i)+'.csv','rb') as csvfile:
                    reader =csv.reader(csvfile,delimiter=',')
                    data = [row for row in reader]

                header = ['Date','Symbol','sourceTime','msgSeqNum','MsgType','SendTime','MsgSize','SecurityIndex','souceTimeMicro','QuoteCondition','TradingStatus','SourceSeqNumber','SourceSessionId','PriceScaleCode','PriceNumerator','ChgQty','Volume','NumOrders','Side','Filler1','ReasonCode','Filler2','LinkID1','LinkID2','LinkID3']

                k = open(code_path+'final/'+date+'_'+str(i)+'.csv','w+')
                writer = csv.writer(k)
                writer.writerow(header)
                writer.writerows(data)
                print time.time()-start
    except Exception,e:
        print str(e)
        # logfile.write("Time of Query: " + time.asctime( time.localtime(time.time())) + "; Error: "+err)

    #STEP 4 - TRANSFERRING DATA TO CLIENT MACHINE
    try:
        os.system('cat '+code_path+'final/* > '+code_path+'finalresult_all.csv')
    except Exception,e:
        print str(e)
        # logfile.write("Time of Query: " + time.asctime( time.localtime(time.time())) + "; Error: "+err)
    while not(os.path.isfile(code_path+'finalresult_all.csv')):
        1