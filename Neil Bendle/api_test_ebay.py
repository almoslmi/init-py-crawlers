import requests
import json
from bs4 import BeautifulSoup as Soup
import csv
import dbHandler
import pp
import addtlFunc
import datetime
import time

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
date = str(st.replace(' ','-').replace(':','-'))
print date

filename1 = "./csvdump/all_item_info"+ str(date) +".csv"
print filename1

def get_item_details_api(params):
    import requests
    import json
    from bs4 import BeautifulSoup as Soup
    import csv
    import dbHandler
    import addtlFunc
    import datetime
    import time

    # today = datetime.date.today()
    # date = today.isoformat()

    # ts = time.time()
    # st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    # date = str(st.replace(' ','-').replace(':','-'))

    #Finally making it a variable passed from main()
    date = params[-1]

    filename1 = "./csvdump/all_item_info"+ str(date) +".csv"
    # filename1 = "all_item_info.csv"

    url = params[2]
    url += "&categoryId="+str(params[3])
    start_page = params[0]
    end_page = params[1]
    for page in range(start_page,end_page):
        try:
            url1 = url
            url1 += "&paginationInput.pageNumber="+str(page)
            url1 += "&paginationInput.entriesPerPage=100"
            url1 += "&outputSelector(0)=SellerInfo"
            flag_page = 0
            while(flag_page == 0):
                try:
                    response = requests.get(url1)
                    if(response.status_code == 200):
                        flag_page = 1
                    else:
                        print "retrying for page"+str(page)
                except:
                    print "retrying for page"+str(page)
                    flag_page = 0
            if(flag_page == 1):
                text = response.text
                j = json.loads(text)
                findItemsByCategoryResponse = j['findItemsByCategoryResponse'][0]
                searchResult = findItemsByCategoryResponse['searchResult']
                item = searchResult[0]['item']
                cnt = 0
                for i in item:
                    try:
                        cnt = cnt+1
                        item_information = []
                        try:
                            title = i['title'][0].encode("utf-8","replace")
                        except:
                            title = "Null"
                        try:
                            item_id = i['itemId'][0].encode("utf-8","replace")
                        except:
                            item_id = "Null"
                        try:    
                            category_name = i['primaryCategory'][0]['categoryName'][0].encode("utf-8","replace")
                        except:
                            category_name = "Null"
                        try:
                            category_id = i['primaryCategory'][0]['categoryId'][0].encode("utf-8","replace")
                        except:
                            category_id = "Null"
                        try:
                            item_url = i['viewItemURL'][0].encode("utf-8","replace")
                        except:
                            item_url = "Null"
                        try:
                            payment = i['paymentMethod'][0].encode("utf-8","replace")
                        except:
                            payment = "Null"
                        try:
                            location = i['location'][0].encode("utf-8","replace")
                            split = location.split(",")
                            if(len(split)==3):
                                city = split[0]
                                state = split[1]
                                country = split[2]
                            else:
                                country = location
                                state = "Null"
                                city = "Null"
                        except:
                            location = "Null"
                            country = "Null"
                            state = "Null"
                            city = "Null"
                        try:
                            shipping_info = i['shippingInfo']
                            try:
                                shipping_cost = shipping_info[0]['shippingServiceCost'][0]['__value__'].encode("utf-8","replace")
                            except:
                                shipping_cost = "Null"
                            try:
                                currency = shipping_info[0]['shippingServiceCost'][0]['@currencyId'].encode("utf-8","replace")
                            except:
                                currency = "Null"
                            try:
                                shipping_type = shipping_info[0]['shippingType'][0].encode("utf-8","replace")
                            except:
                                shipping_type = "Null"
                            try:
                                ship_locations = shipping_info[0]['shipToLocations'][0].encode("utf-8","replace")
                            except:
                                ship_locations = "Null"
                            try:
                                handling_time = shipping_info[0]['handlingTime'][0].encode("utf-8","replace")
                            except:
                                handling_time = "Null"
                        except:
                            ship_locations = "Null"
                            shipping_type = "Null"
                            shipping_cost = "Null"
                            currency = "Null"
                            handling_time = "Null"
                        try:
                            selling_status = i['sellingStatus']
                            try:
                                current_price = selling_status[0]['convertedCurrentPrice'][0]['__value__'].encode("utf-8","replace")
                            except:
                                current_price = "Null"
                            try:
                                bid_count = selling_status[0]['bidCount'][0].encode("utf-8","replace")
                            except:
                                bid_count = "Null"
                            try:
                                time_left = selling_status[0]['timeLeft'][0].encode("utf-8","replace")
                            except:
                                time_left = "Null"
                        except:
                            current_price = "Null"
                            bid_count = "Null"
                            time_left = "Null"
                        try:
                            listing_info = i['listingInfo']
                            try:
                                buyItNowAvailable = listing_info[0]['buyItNowAvailable'][0].encode("utf-8","replace")
                            except:
                                buyItNowAvailable = "Null"
                            try:
                                start_time = listing_info[0]['startTime'][0].encode("utf-8","replace")
                            except:
                                start_time = "Null"
                            try:
                                end_time = listing_info[0]['endTime'][0].encode("utf-8","replace")
                            except:
                                end_time = "Null"
                        except:
                            buyItNowAvailable = "Null"
                            start_time = "Null"
                            end_time = "Null"
                        try:
                            seller_info = i['sellerInfo']
                            try:
                                seller_username = seller_info[0]['sellerUserName'][0].encode("utf-8","replace")
                            except:
                                seller_username = "Null"
                            try:
                                feedback_score = seller_info[0]['feedbackScore'][0].encode("utf-8","replace")
                            except:
                                feedback_score = "Null"
                            try:
                                positive_feedback_percent = seller_info[0]['positiveFeedbackPercent'][0].encode("utf-8","replace")
                            except:
                                positive_feedback_percent = "Null"
                        except:
                            seller_username = "Null"
                            feedback_score = "Null"
                            positive_feedback_percent = "Null"
                        try:
                            item_specifics = addtlFunc.get_item_specifics(item_url,item_id)
                            merchant = item_specifics[0]
                            value = item_specifics[1]
                            type = item_specifics[2]
                            valid_location = item_specifics[3]
                            item_cond = item_specifics[4]
                            description1 = item_specifics[5]
                            description2 = item_specifics[6]
                        except:
                            merchant = "Null"
                            value = "Null"
                            type = "Null"
                            valid_location = "Null"
                            item_cond = "Null"
                            description1 = "Null"
                            description2 = "Null"
                        try:    
                            start_price = addtlFunc.get_bid_history(item_id,date)
                        except:
                            start_price = "Null"
                        bid_url = "http://offer.ebay.com/ws/eBayISAPI.dll?ViewBids&item="+str(item_id)+"&showauto=true"
                        item_information = [title, item_id, category_name,seller_username,item_url,payment,location,ship_locations,shipping_type,shipping_cost,currency,handling_time,bid_count, current_price,buyItNowAvailable,time_left,merchant, value, type, valid_location, item_cond,description1,description2,start_price,bid_url,category_id,start_time,end_time,feedback_score,positive_feedback_percent,city,state,country]
                        addtlFunc.csv_writer(filename1,item_information)
                        try:
                            dbHandler.item_specifics_insert(title, item_id, category_name,seller_username,item_url,payment,location,ship_locations,shipping_type,shipping_cost,currency,handling_time,bid_count, current_price,buyItNowAvailable,time_left,merchant, value, type, valid_location, item_cond,description1,description2,start_price,bid_url,category_id,start_time,end_time,feedback_score,positive_feedback_percent,city,state,country)
                        except Exception,e:
                            lst = []
                            lst =[item_id,str(e)]
                            addtlFunc.csv_writer("./csvdump/problem_db_insert"+ str(date) +".csv",lst)
                            item_information = [title, item_id, category_name,seller_username,item_url,payment,location,ship_locations,shipping_type,shipping_cost,currency,handling_time,bid_count, current_price,buyItNowAvailable,time_left,merchant, value, type, valid_location, item_cond,description1,description2,start_price,bid_url,category_id,start_time,end_time,feedback_score,positive_feedback_percent,city,state,country]
                            addtlFunc.csv_writer(filename1,item_information)
                    except Exception,e:
                        log = [page,str(e),params[3],i]
                        addtlFunc.csv_writer("error_ipage_get_in.csv",log)
                        print "problem ALERT"
                        break
            else:
                pass
        except Exception,e:         
            log = [page,str(e),params[3]]
            addtlFunc.csv_writer("error_ipage_get_notext.csv",log)
    print "done "+str(params[3])


if __name__ == '__main__':

    total_process = 27
    MyAppID = "innovacc-8908-4d12-8232-5a7ca043de0d"
    url = "http://svcs.ebay.com/services/search/FindingService/v1"
    url += "?OPERATION-NAME=findItemsByCategory"
    url += "&SERVICE-VERSION=1.0.0"
    url += "&SECURITY-APPNAME="+str(MyAppID)
    url += "&GLOBAL-ID=EBAY-US"
    url += "&RESPONSE-DATA-FORMAT=JSON"
    url += "&REST-PAYLOAD"
    category = [172009,172010,172010,172010,31411,172036,176950]
    total_pages = []
    header = []
    header = ['title', 'item_id', 'category_name','seller_username','item_url','payment','location','ship_locations','shipping_type','shipping_cost','currency','handling_time','bid_count', 'current_price','buyItNowAvailable','time_left','merchant', 'value', 'type', 'valid_location', 'item_cond','description1','description2','start_price','bid_url','category_id','start_time','end_time']
    addtlFunc.csv_writer(filename1,header)
    cnt = 0
    for i in category:
        url1 = url
        if(cnt==1):
            url1 += "&itemFilter(0).name=ListingType"
            url1 += "&itemFilter(0).value(0)=Auction"
        if(cnt==2):
            url1 += "&itemFilter(0).name=ListingType"
            url1 += "&itemFilter(0).value(0)=AuctionWithBIN"
        if(cnt==3):
            url1 += "&itemFilter(0).name=ListingType"
            url1 += "&itemFilter(0).value(0)=FixedPrice" 
        cnt = cnt + 1
        page_entry_flag = 0
        while(page_entry_flag==0):
            total_page = addtlFunc.get_total_pagecnt(url1,i)
            if(total_page!=-1):
                page_entry_flag = 1
                total_pages.append(total_page)
            else:
                pass
    print total_pages
    jobServer = pp.Server()
    jobServer.set_ncpus(int(total_process))
    # pool = Pool(processes=int(total_process))
    proc = []
    process_per_category = [6,5,5,5,4,1,1]
    for j in range(0,len(category)):
        increement = int(total_pages[j])/int(process_per_category[j])
        start = 1
        end = 0
        for i in range(int(process_per_category[j])):
            url1=url
            sub_param = []
            start_page = start
            end_page = start + increement
            start = end_page
            print "process no." + str(i +1) + " started for category "+str(category[j])
            sub_param.append(start_page)
            sub_param.append(end_page)
            if(j==1):
                url1 += "&itemFilter(0).name=ListingType"
                url1 += "&itemFilter(0).value(0)=Auction"
            if(j==2):
                url1 += "&itemFilter(0).name=ListingType"
                url1 += "&itemFilter(0).value(0)=AuctionWithBIN"
            if(j==3):
                url1 += "&itemFilter(0).name=ListingType"
                url1 += "&itemFilter(0).value(0)=FixedPrice" 
            sub_param.append(url1)
            sub_param.append(category[j])
            sub_param.append(date)
            proc.append(sub_param)

    jobs = []
    for process in proc:
        jobs.append(jobServer.submit(get_item_details_api, (process,)))

    for job in jobs:
        print job()
    #   pool.apply_async(get_item_details_api, args = (process, ))
    # pool.close()
    # pool.join()
    print "main DONE!!"
