
import requests
import json
import excelHelper
import csv
import sys, string, os, traceback
import urllib
import json
import os
from bs4 import BeautifulSoup as Soup
import pp


def linkedin(parameters):
    import requests
    import json
    import excelHelper
    import csv
    import sys, string, os, traceback
    import urllib
    import json
    import os
    from bs4 import BeautifulSoup as Soup
    import pp
    import dbHandler

    try:
        start_index = int(parameters[0])
        end_index = int(parameters[1])
        process_num = int(parameters[2])

        print 'process ' + str(process_num) + 'started. Start : ' + str(start_index) + ' and End : ' + str(end_index)

        workbook_access ='AccessToken.xlsx'
        queries1 =  excelHelper.excelHelper().readExcel(workbook_access,0,34,0)
        #print queries1
        i = process_num - 1
        at = []
        at = [x[1] for x in queries1]
        print at
        acces_token = at[i]
        print i, acces_token
        workbook_name = 'inn_ucla.xlsx'
        queries =  excelHelper.excelHelper().readExcel(workbook_name,start_index,end_index,0)

        rowcounter = 0

        while rowcounter < len(queries):
            query_string = queries[rowcounter]
            CCID=query_string[0]
            first_name = query_string[2].strip()

            last_name = query_string[3].strip()
            print first_name,last_name,CCID
            keywords = "University of California, Los Angeles"
            base_url = 'https://api.linkedin.com/v1/people-search:(people:(id,public-profile-url,first-name,last-name,industry,location,positions,educations,api-standard-profile-request))?first-name=%s&last-name=%s&school-name=%s&sort=relevance&format=json&oauth2_access_token=%s'%(first_name,last_name,keywords.encode('utf8'),acces_token)
            #print base_url
            #base_url = 'https://api.linkedin.com/v1/people-search:(people:(id,public-profile-url,first-name,last-name,industry,location,positions,school,api-standard-profile-request))?first-name=%s&last-name=%s&school-name=%s&sort=relevance&format=json&oauth2_access_token=%s'%(first_name,last_name,keywords,acces_token)
            r = requests.get(base_url)
            cont = r.text
            print cont.encode('utf8')
            #print cont
            data = json.loads(cont)
            #print data
            if  data.has_key('errorCode'):
                print "error in key"
                i += 2
                acces_token = at[i]

                
            else:
                rowcounter += 1
                try:
                    dat = data['people']
                    count=dat['_total']
                    #print count
                    vals = dat['values']
                    #This loop is for multiple profile with same name
                    for i in range(len(vals)):
                        dicti = vals[i]
                        firstname=dicti['firstName']
                        lastname=dicti['lastName']
                        #location = dicti['location']['name']
                        position_details = dicti['positions']
                        pid = dicti['id']
                        public_url =   dicti['apiStandardProfileRequest']
                        header_val = public_url['headers']['values'][0]['value']
                        #print header_val
                        public_ur = str(public_url['url'])
                        public_ur = public_ur + '?format=json&oauth2_access_token=%s'%(acces_token)
                        pub = public_ur.replace('http','https')
                        print pub
                        r = requests.get(pub,headers={"x-li-auth-token":header_val})
                        last_mile = json.loads(str(r.text))
                        req = str(last_mile['siteStandardProfileRequest']['url'])
                        print req
                        print dicti
                        
                        try:
                            location = dicti['location']['name']
                            #name = loaction_details['values'][0]['school-name'].encode('utf8','replace')
                        except Exception, e:
                            print "error in location:",str(e)
                            country='NA'
                            code ='NA'
                        pos_count=position_details['_total']
                        
                        
                        # try for postion field 
                        try:
                                        
                            if pos_count <> 0: 
                            #store multiple positions in pos file                   
                                for j in range(pos_count):
                                    data_pos =[]
                                    data_pos.append(CCID)
                                    data_pos.append(firstname)
                                    data_pos.append(lastname)
                                    data_pos.append(position_details['values'][j]['company']['name'].encode('utf8','replace'))
                                    data_pos.append(position_details['values'][j]['title'].encode('utf8','replace'))
                                    data_pos.append(str(position_details['values'][j]['isCurrent']))
                                    data_pos.append(req)
                                    #dbHandler.addsposdata(data_pos)
                                    #p.writerow(data_pos)                
                        except Exception, e:
                            raise e
                            data_pos.append(NA)
                            data_pos.append(NA)
                            data_pos.append(NA)
                        
                        
                        data_det =[]
                        data_det.append(CCID)
                        data_det.append(firstname.encode('utf8','replace'))
                        data_det.append(lastname.encode('utf8','replace'))
                        data_det.append(location)
                        data_det.append(str(count))
                        data_det.append(str(pos_count))
                                  
                        data_det.append(req)
                        #dbHandler.addsprofiledata(data_det)
                        #c.writerow(data_det)
                        
                except Exception,e:
                     print "error:",str(e)
                     print "Person not Found"
                     data_det=[]
                     data_det.append(CCID)
                     data_det.append(first_name.encode('utf8','replace'))
                     data_det.append(last_name.encode('utf8','replace'))
                     #data_det.append(str(traceback.format_exc()))
                     data_det.append(str(count))
                     if count==0:
                        data_det.append("Not Found")

                     else:
                        data_det.append("Private Profile")

                     #dbHandler.adderrdata(data_det)
                     #err.writerow(data_det)
    except Exception,E:
        print traceback.format_exc()

        parameters.append(str(traceback.format_exc))
        #index_details=[str(each) for each in parameters]
        #dbHandler.addsindexdata(index_details)
        
        with open("index_details.csv",'wb') as f:
            writer = csv.writer(f)
            writer.writerow(parameters)
        

if __name__ == '__main__':

    try:
        startPage = 6145
        endPage = 6150
        if endPage < startPage:
            print"end page can't be less  that start index Enter again:"
        totalProcess = 1
        totalPage =  int(endPage) - int(startPage)+1
        eachSlot =  int(float(totalPage)/float(totalProcess))
        print "each slot:"+str(eachSlot)
        job_server = pp.Server()
        job_server.set_ncpus(int(totalProcess))

        proc = []
        sub_param = []
        for i in range(int(totalProcess)):
                sub_param = []
                print "process no." + str(i +1) + " started"
                startIndex = int(startPage) + (int(eachSlot)*i)
                endIndex = startIndex + int(eachSlot)
                sub_param.append(int(startIndex))
                sub_param.append(int(endIndex))
                sub_param.append(str(i + 1))
                proc.append(sub_param)

                #end_index = sub_parts[counter+1] 
                #p = multiprocessing.Process(target=crawl_page, args=(proxy,start_index,end_index))
                #p.start()
                #proc.append(p)
                #counter +=1
        jobs = []
        for process in proc:
            #Calling the function to be multiprocessed
            jobs.append(job_server.submit(linkedin, (process,)))

        for job in jobs:
            print job()
    except Exception,e:
        print traceback.format_exc()