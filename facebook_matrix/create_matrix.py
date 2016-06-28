'''
The following code takes the id's from a csv file and then generates the facebook data as per requirement.
'''
from bs4 import BeautifulSoup as Soup
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys
import requests
import selenium.webdriver.support.ui as ui
import time
import random
import csv
from selenium.webdriver.common.action_chains import ActionChains
import MySQLdb
import re
import multiprocessing 
from multiprocessing import Pool
import excelHelper
#import dbHandler

def csv_writer(filename,info):
    write_item = csv.writer(open(filename,"ab+"))
    write_item.writerow(info)

def compare1(l1,l2):
    l1 = l1.split(",")
    l2 = l2.split(",")
    score = 0
    for i in l1:
        for j in l2:
            if(i in j and i!="NULL" and j!="NULL"):
                score = score+1
    return score

def compare2(l1,l2):
    l1 = l1.split("}{")
    l2 = l2.split("}{")
    l1[0] = l1[0].replace("{","")
    l2[0] = l2[0].replace("{","")
    l1[len(l1)-1] = l1[len(l1)-1].replace("}","")
    l2[len(l2)-1] = l2[len(l2)-1].replace("}","")
    score = 0
    for i in l1:
        e1 = i.split(";;")[0]
        for j in l2:
            e2 = j.split(";;")[0]
            if(e1 in e2 and e1!="NULL" and e2!="NULL"):
                score = score+1
    return score


def compare3(l1,l2):
    l1 = l1.split("}{")
    l2 = l2.split("}{")
    l1[0] = l1[0].replace("{","")
    l2[0] = l2[0].replace("{","")
    l1[len(l1)-1] = l1[len(l1)-1].replace("}","")
    l2[len(l2)-1] = l2[len(l2)-1].replace("}","")
    score = 0
    for i in l1:
        for j in l2:
            if(i in j and i!="NULL" and j!="NULL"):
                score = score+1
    return score


data = []
with open('make adja.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)
#print data
le = len(data)
csv_writer("output_matrix.csv",["link1","link2","religion","politics","education","work","current_city","places_lived","music","movie","book","group","activity","sport","past_events","upcoming_events"])
for i in range(0,le):
    lst1 = data[i]
    for j in range(i+1,le):
        lst2 = data[j]
        output_data = []
        link1 = lst1[1]
        link2 = lst2[1]
        reli1 = lst1[8]
        reli2 = lst2[8]
        religion = compare1(reli1,reli2)
        poli1 = lst1[9]
        poli2 = lst2[9]
        politics = compare1(poli1,poli2)
        edu1 = lst1[11]
        edu2 = lst2[11]
        education = compare2(edu1,edu2)
        cur_city1 = lst1[12]
        cur_city2 = lst2[12]
        if(cur_city1 in cur_city2 and cur_city1!="NULL" and cur_city2!="NULL"):
            current_city = 1
        else:
            current_city = 0
        place1 = lst1[13]
        place2 = lst2[13]
        places_lived = compare3(place1,place2)
        work1 = lst1[14]
        work2 = lst2[14]
        work = compare2(work1,work2)
        music = compare3(lst1[15],lst2[15])
        movie = compare3(lst1[16],lst2[16])
        book = compare3(lst1[17],lst2[17])
        group = compare3(lst1[18],lst2[18])
        activity = compare3(lst1[19],lst2[19])
        sport = compare3(lst1[20],lst2[20])
        past_events = compare3(lst1[21],lst2[21])
        upcoming_events = compare3(lst1[22],lst2[22])
        csv_writer("output_matrix.csv",[link1,link2,religion,politics,education,work,current_city,places_lived,music,movie,book,group,activity,sport,past_events,upcoming_events])
print "DONE "



'''
            
# the main method
if __name__ == '__main__':
    
    total_ids = raw_input("total no. of ids:")
    sheet = raw_input("enter excel sheet no.")
    total_process = raw_input("total no. of parallel process you want:")
    #lst = [['201001149@daiict.ac.in','testonly123'],['saksham.gupta@innovaccer.com','testonly123'],['saksham_gupta@daiict.ac.in','testonly123'],["prabhat.kumar@innovaccer.com","testonly123"],["shiv.prasad@innovaccer.com","Innovation123"]]
    email1 = '201001149@daiict.ac.in'#raw_input("enter username 1:")
    pass1 = 'testonly123'#raw_input("enter password 1:")
    email2 = 'saksham_gupta@daiict.ac.in'#raw_input("enter username 2:")
    pass2 = 'testonly123'#raw_input("enter password 1:")
    lst = [[email1,pass1]]
    actual_process = len(lst) * total_process
    each_slot =  int(float(total_ids)/float(actual_process))
    print "each slot:"+str(each_slot)
    pool = Pool(processes=int(actual_process))
    print "actual_process:"+str(actual_process)
    proc = []
    sub_param = []
    start_index = 0
    end_index = 0 
    count = 0
    for x in lst:
        for i in range(1,int(total_process)+1):
                count = count + 1
                browser = "browser"
                sub_param = []
                end_index = start_index + each_slot
                browser = browser + str(count)
                sub_param.append(browser)
                sub_param.append(start_index)
                sub_param.append(end_index)
                sub_param.append(x[0])
                sub_param.append(x[1])
                sub_param.append(email2)
                sub_param.append(pass2)
                sub_param.append(sheet)
                sub_param.append(count)
                proc.append(sub_param)
                start_index = end_index
    for process in proc:
        pool.apply_async(fb_data, args= (process, ))
        time.sleep(60)
    pool.close()
    pool.join()
'''