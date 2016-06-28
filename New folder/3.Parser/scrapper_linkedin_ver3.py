from bs4 import BeautifulSoup as Soup
from time import time
import MySQLdb
import requests
import json
import re
import os
#import excelHelper

import time
#import CreateCSV
import multiprocessing 
from multiprocessing import Pool
import random
import urllib
import csv
import traceback
import dbHandler
from selenium import webdriver 

import glob

#profile = webdriver.FirefoxProfile()

#browser = webdriver.Firefox(firefox_profile=profile)

def read_static(params):
    from bs4 import BeautifulSoup as Soup
    from time import time
    import MySQLdb
    import requests
    import json
    import re
    import os
    #import excelHelper
    #import dbHandler
    import time
    #import CreateCSV
    import multiprocessing 
    from multiprocessing import Pool
    import random
    import urllib
    import csv
    import traceback
    #import dbHandler
    from selenium import webdriver 

    import glob
    #7137737

    #list_of_files = glob.glob("C:\\Users\\Acer\\Desktop\\code\\linkedin code\\2.Crawler\\Dump\\10000-153324087.html")
    list_of_files = glob.glob("C:\\Users\\Acer\\Desktop\\code\\linkedin code\\2.Crawler\\dump\\dump2\\*.html")
    #C:\Users\Acer\Desktop\code\linkedinproject\crawler\next1000
    ##print list_of_files

    process_name = params[2]
    start_index = params[0]
    end_index = params[1]
    effective_list = list_of_files[int(start_index):int(end_index)]
    
    file_counter =0
    
    for files in effective_list:
        try:
            file_counter += 1
            ##print 'Process No.:'+ process_name+' -parsing file no:' + str(file_counter)+":"
            #file_r=open("103-174319117.html").read()
            #soup = Soup(file_r, 'html.parser')
            # #print soup
            filename = open(files,'rb')
            #print "filename ",filename
            #linkedin_id = ''.join(files.split('y\\')[5].split('.')[:-1])
            employer_of = "n/a"
            ##print linkedin_id
            f=files
            #lid = f[f.find('y\\')+2:f.find('.html')]
            ccid =f[f.find('ump2\\')+5:f.find('-')]
            lid =f[f.find('-')+1:f.find('.html')]
            #print ccid
            #lid = f[:f.find('.html')]
            print ccid,"-",lid
            html_content = filename.read()
            ##print 
            filename.close()

            soup = Soup(html_content,'html.parser')
            #print soup
            #print "soup done"
            current_position_date = "N/A"

        # General Details
            try:
                print "General"
                #main_div  = soup.find("div",{"id":"body"}).find("div",{"id":"profile"})
                #top_card = main_div.find("div",{"id":"top-card"}).find("div",{"class":"profile-top-card"}).find("div",{"class":"profile-card"}).find("div",{"class":"profile-overview"}).find("div",{"class":"profile-overview-content"}).find("div",{"class":"masthead"}).find("div",{"data-li-template":"p2_basic_info"}).find("div",{"id":"name_container"})
                ##print main_div.text
                #top_card = main_div.find("span",{"class":"full-name"})
                ##print top_card.text
                gen_det=[]
                
                gen_det.append(ccid)
                gen_det.append(lid)
                
                try:
                    employee_name = soup.findAll('span',{'class':'full-name'})[0].text.encode('utf-8','replace')
                    # [0].text.encode('utf-8','replace')
                    print employee_name
                    #et=soup.findAll('span',{'class':'full-name'})

                    #print  "ename ",employee_name
                except Exception,e:
                    print traceback.format_exc()
                    employee_name = 'NA'
                    #continue
                print employee_name
                gen_det.append(employee_name)
                try:
                    current_title = soup.find("div",{"id":"headline"}).find("p",{"class":"title"}).text.encode('utf-8','replace')
                    
                    try:
                        current_position = current_title.split(' at ')[0].encode('utf-8','replace')
                        
                    except:
                        current_position = 'NA'
                    #print "current_position",current_position
                    try:
                        current_company = current_title.split(' at ')[1].encode('utf-8','replace')
                    except:
                        current_company= 'NA'
                    #print "current_company : ",current_company
                except:
                    current_title = "NA"
                #print "title",current_title
                gen_det.append(current_title)
    	# Location Details
                
                all_loc_div = soup.findAll('div',{'id':'demographics'})
                #all_exp_div = soup.find('div',{'id':'experience-482311328'})
                #print 'Location',len(all_loc_div)
                
                i=0

                for div in all_loc_div:
                    i+=1
                    #print "#",i
                    loc=[]
                    #final_div = div.find('div',{'id':re.compile('experience-*')})
                    final_div=div
                    
                    try:    
                        loc_div = final_div.findAll('span',{'class':'locality'})
                        
                        ##print len(loc_div)
                        loc_name = loc_div[0].findAll('a')
                        ##print major_name[1].text
                        if len(loc_name) >1:
                            loc_name1 = loc_name[0].text
                            loc_name2 = loc_name[1].text
                            location_name = loc_name1 +" ,"+loc_name2
                        else:
                            loc_name1 = loc_name[0].text
                            location_name = loc_name1
                            #field_name2 = field_div[1].find('a').text.encode('utf-8','replace')
                            ##print field_name2
                    except Exception,e:
                        #print str(e)
                        location_name = "N/A"
                    ##print "Location ",location_name

                    loc.append(location_name)
                    try:    
                        ind_div = final_div.findAll('dd',{'class':'industry'})
                        ind=[]
                        ##print len(ind_div)
                        ind_name = ind_div[0].findAll('a')
                        ##print major_name[1].text
                        if len(ind_name) >1:
                            ind_name1 = ind_name[0].text
                            loc_name2 = ind_name[1].text
                            industry_name = ind_name1 +" ,"+ind_name2
                        else:
                            ind_name1 = ind_name[0].text
                            industry_name = ind_name1
                            #field_name2 = field_div[1].find('a').text.encode('utf-8','replace')
                            ##print field_name2
                    except Exception,e:
                        #print str(e)
                        industry_name = "N/A"
                    #print "Industry ",industry_name
                    ind.append(industry_name)
                gen_det.append(location_name)
                gen_det.append(industry_name)
                #print gen_det

                #current prvious edu     
                     
                curr_div = soup.find('tr',{'id':re.compile('overview-summary-current')})
                curr=[]
                if curr_div is not None:
                    
                    stri_c =""
                    final_div = curr_div.findAll('a')                
                    for k in final_div:
                        
                        try :
                            c = k.text
                        except:
                            c = NA
                        p=c.find('Edit ')
                        if  p!=-1 :
                            pass
                        else:
                            #stri=""+c
                            curr.append(c)
                else :
                    stri_c =""
                    curr.append("NA")
                    curr.append("NA")
                for i in range(1,len(curr)):
                    if i == len(curr)-1:
                        stri_c +=curr[i]
                    else:
                        stri_c+=curr[i]+","
                gen_det.append(stri_c)
                #print 


                prev_div = soup.find('tr',{'id':re.compile('overview-summary-past')})
                prev=[]
                if prev_div is not None:
                    
                    stri_p=""
                    final_div = prev_div.findAll('a')                
                    for k in final_div:
                        try:
                            c=k.text
                        except:
                            c= NA
                        p=c.find('Edit ')
                        if  p!=-1 :
                            pass
                        else:
                            #stri=""+c
                            prev.append(c)

                else :
                    stri_p = ""
                    prev.append("NA")
                    prev.append("NA")
                #print prev
                for i in range(1,len(prev)):
                    if i == len(prev)-1:
                        stri_p +=prev[i]
                    else:
                        stri_p +=prev[i]+","
                gen_det.append(stri_p)

                        
                    #gen_det(stri)
                educa_div = soup.find('tr',{'id':re.compile('overview-summary-education')})
                educa=[]
                if educa_div is not None:
                    
                    stri_e=""
                    final_div = educa_div.findAll('a')                
                    for k in final_div:
                        
                        try :
                            c = k.text
                        except:
                            c = NA
                        p=c.find('Edit ')
                        if  p!=-1 :
                            pass
                        else:
                            #stri=""+c
                            educa.append(c)    
                else :
                    stri_e =""
                    educa.append("NA")
                    educa.append("NA")
                for i in range(1,len(educa)):
                    if i == len(educa)-1:
                        stri_e+=educa[i]
                    else:
                        stri_e+=educa[i]+","
                #educ=stri.encode('utf-8','replace')
                gen_det.append(stri_e) 
                print gen_det
                dbHandler.addsgendata(gen_det)



                # ExperienceDetails
                all_exp_div = soup.findAll('div',{'id':re.compile('experience-.*-view')})
                #all_exp_div = soup.find('div',{'id':'experience-482311328'})
                #print 'experience',len(all_exp_div)

                i=0

                for div in all_exp_div:
                    i+=1
                    #print "#",i
                    pos=[]
                    
                    pos.append(ccid)
                    pos.append(lid)
                    #final_div = div.find('div',{'id':re.compile('experience-*')})
                    final_div=div
                    try:
                        title = final_div.find('h4').text.encode('utf-8','replace')
                        ##print title
                    except:
                        title = "N/A"
                    #print "title ",title
                    pos.append(title)
                    try:	
                        company_div = final_div.find('header').find_all('h5')
                        if len(company_div) >1:
                            company_name = company_div[1].find('a').text.encode('utf-8','replace')
                        else:
                            company_name = company_div[0].find('a').text.encode('utf-8','replace')
                        

                    except Exception,e:
                        #print str(e)
                        company_name = "N/A"
                    #print "company_name ",company_name
                    pos.append(company_name)

                    try:
                        date_s = final_div.find('span',{'class':'experience-date-locale'})
                        try:

                            loc = date_s.find('span',{'class':'locality'}).text.encode('utf-8','replace')
                        except:
                            loc = "NA"
                        try:

                            date_span =date_s.text.encode('utf-8','replace')
                            ds =date_span.decode('utf-8').split(u'\u2013')
                        
                            end= ds[1].replace(loc,"")
                        except:
                            ds = ["N/A"]
                            end = "NA"


                    except:
                        loc = "NA"
                        ds = ["N/A"]
                        end = "NA"
                        
                    
                    #print "date_span ",ds
                    
                    
                    pos.append(ds[0])

                    pos.append(end)
                    pos.append(loc)
                    
                    #print "exp no:",i,pos
                    #exper.append(pos)
                    #dbHandler.addsexpdata(pos)

               
                    #dbHandler.addPosDetails( linkedin_id, p[1], p[0], p[2])
                #dbHandler.addEmployeeDetails( linkedin_id, employee_name, employer_of, current_company, current_position, current_position_date)


                    #dbHandler.addPosDetails( linkedin_id, company_name, title, date_span)
                    ##print title

               
                    
            except  Exception,e:
                print "hjsfd",str(e)
                print traceback.format_exc()
            # Education detials

            try:
                all_edu_div = soup.findAll('div',{'id':re.compile('education-.*-view')})
                #all_exp_div = soup.find('div',{'id':'experience-482311328'})
                #print 'Number of education',len(all_edu_div)
                exper =[]
                i=0

                for div in all_edu_div:
                    i+=1
                    #print "#",i
                    edu=[]
                    
                    edu.append(ccid)
                    edu.append(lid)
                    #final_div = div.find('div',{'id':re.compile('experience-*')})
                    final_div=div
                    try:
                        title = final_div.find('h4').text.encode('utf-8','replace')
                        ##print title
                    except:
                        title = "N/A"
                    #print "School ",title
                    edu.append(title)
                    try:    
                        degree_div = final_div.find('header').find_all('h5')
                        if len(degree_div) >1:
                            degree_name = degree_div[1].find('span',{'class':'degree'}).text.encode('utf-8','replace')
                        else:
                            degree_name = degree_div[0].find('span',{'class':'degree'}).text.encode('utf-8','replace')
                      

                    except Exception,e:
                        ##print str(e)
                        degree_name = "N/A"
                    #print "Degree  ",degree_name
                    edu.append(degree_name)
                    try:    
                        field_div = final_div.findAll('span',{'class':'major'})
                        major_name = field_div[0].findAll('a')
                        ##print major_name[1].text
                        if len(major_name) >1:
                            field_name1 = major_name[0].text
                            field_name2 = major_name[1].text
                            field_name = field_name1 +" ,"+field_name2
                        else:
                            field_name1 = major_name[0].text
                            field_name = field_name1
                            #field_name2 = field_div[1].find('a').text.encode('utf-8','replace')
                            ##print field_name2
                        

                    except :
                        field_name = "N/A"
                    ##print "Major ",field_name
                    edu.append(field_name)

                    try:
                        date_span  = final_div.find('span',{'class':'education-date'}).text.encode('utf-8','replace')
                        ds =date_span.decode('utf-8').split(u'\u2013')
                        if len(ds) ==1:
                            ds.append("NA")

                    except:
                        ds = ["NA","NA"]
                    
                    
                    start = ds[0].encode('utf-8','replace')
                    end=ds[1].encode('utf-8','replace')
                    #print ds
                    #print end
                    edu.append(start)
                    edu.append(end)

                    #print len(edu)
                   # #print "Date_span ",date_span
                    #edu.append(date_span.decode('ascii','ignore'))
                    #print "education no:",i,edu
                    #dbHandler.addsedudata(edu)
                    #print " row entered"

                
            except Exception, e:
                print traceback.format_exc()

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
                    try:
                        title = final_div.find('h5').text.encode('utf-8','replace')
                        #print title
                    except:
                        title = "NA"
                    #print "Org name ",org_name
                    #rint "title ",title

                    org.append(str(org_name))
                    org.append(str(title))
                    
                    try:
                        date_span  = final_div.find('span',{'class':'organizations-date'}).text.encode('utf-8','replace')
                        print len(date_span)
                        try:
                            if len(date_span)== 0:
                                ds=["NA","NA"]
                            else:
                                ds =date_span.decode('utf-8').split(u'\u2013')
                                #ds=str(d_span)
                        except:
                            ds = ["NA","NA"]
                    except:
                        date_span = "NA"
                        ds = ["NA","NA"]
                    #print "date_span ",ds
                    
                    d1=str(ds[0].encode('utf-8','replace'))
                    org.append(d1)
                    #print ds[1]
                    #d2=str(ds[1].encode('utf-8','replace'))
                    #org.append(d2)
                    org.append(ds[1].encode('utf-8','replace'))

                    #org.append(date_span.decode('ascii','ignore'))
                    #print "Organization no:",i,org
                    #dbHandler.addsorgdata(org)
                    #print "entered"
                
            except Exception, e:
                print "hkg",traceback.format_exc()
        except Exception,e:
            err.append(filename)
            #print "errorfile",err
            pass

                
if __name__ == '__main__':
    #params = [0,427,'1']
    #read_static(params)
        #start_page = raw_input("Enter start index:")
        start_page=0
        end_page=13410
        #end_page = raw_input("Enter end index:")
        if int(end_page) < int(start_page):
            end_page = raw_input("end page can't be less  that start indes Enter again:")
        #total_process = raw_input("total no. of parallel process you want:")
        total_process=1
        total_page =  int(end_page) - int(start_page)
        each_slot =  int(float(total_page)/float(total_process))
        #print "each slot:"+str(each_slot)
        
          
        pool = Pool(processes=int(total_process))
        proc = []
        sub_param = []
        for i in range(int(total_process)):
                sub_param = []
                #proxy['http'] = proxies[counter]
                start_index = int(start_page) + (int(each_slot)*i)

                end_index = start_index + int(each_slot)
                sub_param.append(start_index)
                sub_param.append(end_index)
                sub_param.append(str(i))
                proc.append(sub_param)
                #print start_index
                #print end_index
                
        
        for process in proc:
            pool.apply_async(read_static, args = (process, ))
        pool.close()
        pool.join()
