import requests
import json
from bs4 import BeautifulSoup as Soup
import csv
import dbHandler
import datetime

def csv_writer(filename,info):
    #write info (type-list) to the mentioned file
    write_item = csv.writer(open(filename,"ab+"))
    write_item.writerow(info)


def get_total_pagecnt(url,id):
    #get total pages returned from the ebay api according to category id
    #total items = total pages * 100 (assuming 100 items per page)
    url += "&categoryId="+str(id)
    url += "&paginationInput.entriesPerPage=100"
    try:
        response = requests.get(url)
        if(response.status_code == 200):
            #interpreting the json response
            text = response.text
            j = json.loads(text)
            paginationOutput = j['findItemsByCategoryResponse'][0]['paginationOutput'][0]
            total_pages = paginationOutput['totalPages'][0]
            total_entries = paginationOutput['totalEntries'][0]
            print total_entries, id 
        else:
            total_pages = -1
        return total_pages
    except:
        return -1

def get_item_specifics(item_url,item_id):
    #function to screen scrape the values of item specifics
    merchant = "Null"
    value = "Null"
    type = "Null"
    valid_location = "Null"
    item_cond = "Null"
    item_specifics = []
    item_page_flag = 1
    description1 = "Null"
    description2 = "Null"
    while(item_page_flag == 1):
        try:
            item_page = requests.get(item_url)
            item_page_flag = 0
        except Exception,e:
            item_page_flag = 1
    if(item_page.status_code == 200 and item_page_flag == 0):
        soup = Soup(item_page.text,"html.parser")
        try:
            item_cond1 = soup.find("div",{"id":"vi-itm-cond"})
            item_cond = item_cond1.text.encode("utf-8","replace")
            item_cond = item_cond.replace("--","")
        except:
            item_cond = "Null"
        try:
            item_des = soup.find("div",{"id":"readMore"})
            description1 = item_des.text.encode("utf-8","replace")
            description1 = description1.replace("\n","")
        except:
            description1 = "Null"
        try:
            item_des = soup.find("div",{"id":"desc_div"})
            description2 = item_des.text.encode("utf-8","replace")
            description2 = description2.replace("\n","")
        except:
            description2 = "Null"
        try:
            item_specifics = soup.find("div",{"class":"itemAttr"})
            table = item_specifics.find("table")
            td = table.findAll("td")
            mer = 0
            val = 0
            typ = 0
            vloc = 0
            for t in range(0,len(td)):
                if(t%2==0):
                    te = td[t].text.encode("utf-8","replace")
                    if("Merchant" in str(te) and mer == 0):
                        merchant = td[t+1].text.encode("utf-8","replace").rstrip(" ")
                        mer = 1
                        merchant = merchant.strip(' ')
                        merchant = merchant.replace("\n","")
                    elif("Value" in str(te) and val == 0):
                        value = td[t+1].text.encode("utf-8","replace").rstrip(" ")
                        val = 1 
                        value = value.strip(' ')
                        value = value.replace("\n","")
                    elif("Type" in str(te) and typ == 0):
                        type = td[t+1].text.encode("utf-8","replace").rstrip(" ")
                        typ = 1
                        type = type.strip(' ')
                        type = type.replace("\n","")
                    elif("Valid" in str(te) and vloc == 0):
                        valid_location = td[t+1].text.encode("utf-8","replace").rstrip(" ")
                        vloc = 1
                        valid_location = valid_location.strip(' ')
                        valid_location = valid_location.replace("\n","")
                    else:
                        pass
                else:
                    pass
        except Exception,e:
            pass
    else:
        pass
    item_specifics = [merchant,value,type,valid_location,item_cond,description1,description2]
    return item_specifics


def get_bid_history(item_id,date):
    #function to screen scrape the values of bids
    # today = datetime.date.today()
    # date = today.isoformat()
    filename2 = "./csvdump/all_bid_info"+ str(date)+".csv"
    bid_url = "http://offer.ebay.com/ws/eBayISAPI.dll?ViewBids&item="+str(item_id)+"&showauto=true"
    try:
        bid_history = []
        start_price = ""
        get_bid_page = 1
        while (get_bid_page == 1):
            try:
                bid_page = requests.get(bid_url)
                if(bid_page.status_code == 200):
                    get_bid_page = 0
            except:
                get_bid_page = 1
        if(get_bid_page == 0):
            soup1 = Soup(bid_page.text)
            try:
                start = soup1.find("tr",{"id":"viznobrd"})
                start_price = start.find("td",{"align":"left"})
                start_price = start_price.text.encode('utf-8','replace').replace("\t","")
                start_price = start_price.replace("\n","").rstrip(' ').strip(' ')
                start1 = start_price.split("$")
                start_price = start1[1]
            except:
                start_price = "Null"
            try:
                div = soup1.find("div",{"id":"vizrefdiv"})
                table = div.find("table")
                try:
                    tr_auto = table.findAll("tr",{"class":"newcontentValueFont","bgcolor":"#ffffff"})
                    tr_auto_flag = 0
                except:
                    tr_auto_flag = 1
                try:
                    tr = table.findAll("tr",{"class":"","bgcolor":"#ffffff"})
                    tr_flag = 0
                except:
                    tr_flag = 1
                flag = 0
            except:
                flag = 1

            if(flag == 0):
                if(tr_auto_flag == 0):
                    try:
                        answer_count = dbHandler.bid_history_fetch(item_id,"true","true")
                    except Exception,e:
                        print str(e)
                    range_value = int(len(tr_auto)) - int(answer_count)
                    for tr1 in range(0,range_value):
                        try:
                            name = tr_auto[tr1].find("td",{"class":"newcontentValueFont","align":""})
                            bidder_name = name.text.encode("utf-8","replace")
                            bidder_name = bidder_name.strip()
                        except:
                            bidder_name = "Null"
                        try:
                            value = tr_auto[tr1].findAll("td",{"class":"newcontentValueFont","align":"left"})
                            bid_amount = value[0].text.encode("utf-8","replace")
                            bid_amount = bid_amount.split("US")[1]
                            bid_time = value[1].text.encode("utf-8","replace")
                        except:
                            bid_amount = "Null"
                            bid_time = "Null"
                        bid = []
                        automatic_bid = "true"
                        bid_history_found = "true"
                        bid = [item_id,bid_url,bidder_name,bid_amount,bid_time,automatic_bid,bid_history_found]
                        write_bid = csv.writer(open(filename2,"ab+"))
                        write_bid.writerow(bid)
                        bid_history.append(bid)
                        try:
                            dbHandler.bid_history_insert(item_id,bid_url,bidder_name,bid_amount,bid_time,automatic_bid,bid_history_found)
                        except Exception,e:
                            print str(e)
                else:
                    bid = []
                    bid = [item_id,bid_url,"no auto bid history found"]
                    write_bid = csv.writer(open(filename2,"ab+"))
                    write_bid.writerow(bid)
                    bid_history.append(bid)
                    bid_history_found = "false"
                    try:
                        dbHandler.bid_history_insert(item_id,bid_url,"Null","Null","Null","Null",bid_history_found)
                    except Exception,e:
                        print str(e)
                if(tr_flag == 0):
                    try:
                        answer_count = dbHandler.bid_history_fetch(item_id,"false","true")
                    except Exception,e:
                        print str(e)
                    range_value = int(len(tr_auto)) - int(answer_count)
                    for tr1 in range(0,range_value):
                        try:
                            name = tr[tr1].find("td",{"class":"onheadNav","align":""})
                            bidder_name = name.text.encode("utf-8","replace")
                            bidder_name = bidder_name.strip()
                        except:
                            bidder_name = "Null"
                        try:
                            value = tr[tr1].findAll("td",{"class":"contentValueFont","align":"left"})
                            bid_amount = value[0].text.encode("utf-8","replace")
                            bid_amount = bid_amount.split("US")[1]
                            bid_time = value[1].text.encode("utf-8","replace")
                        except:
                            bid_amount = "Null"
                            bid_time = "Null"
                        bid = []
                        bid = [item_id,bid_url,bidder_name,bid_amount,bid_time,"false"]
                        write_bid = csv.writer(open(filename2,"ab+"))
                        write_bid.writerow(bid)
                        bid_history.append(bid)
                        bid_history_found = "true"
                        automatic_bid = "false"
                        try:
                            dbHandler.bid_history_insert(item_id,bid_url,bidder_name,bid_amount,bid_time,automatic_bid,bid_history_found)
                        except Exception,e:
                            print str(e)    
                else:
                    bid = []
                    bid = [item_id,bid_url,"no bid history found"]
                    write_bid = csv.writer(open(filename2,"ab+"))
                    write_bid.writerow(bid)
                    bid_history.append(bid)
                    bid_history_found = "false"
                    try:
                        dbHandler.bid_history_insert(item_id,bid_url,"Null","Null","Null","Null",bid_history_found)
                    except Exception,e:
                        print str(e)
            else:
                bid = []
                bid = [item_id,bid_url,"no bid history found"]
                write_bid = csv.writer(open(filename2,"ab+"))
                write_bid.writerow(bid)
                bid_history.append(bid) 
                bid_history_found = "false"
                try:
                    dbHandler.bid_history_insert(item_id,bid_url,"Null","Null","Null","Null",bid_history_found)
                except Exception,e:
                    print str(e)
        else:
            start_price = "Null"
            try:
                dbHandler.bid_history_insert(item_id,bid_url,"Null","Null","Null","Null","false")
            except:
                print str(e)
    except:
        start_price = "Null"
        try:
            dbHandler.bid_history_insert(item_id,bid_url,"Null","Null","Null","Null","false")
        except:
            print str(e)
    return start_price
