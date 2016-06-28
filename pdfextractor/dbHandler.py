import MySQLdb
import os
import datetime


def addNgramDetails(rows):
    print 'in db handler'
    con = MySQLdb.connect(host='192.168.1.4', user='root', passwd='password', db='ingram')
    cur = con.cursor()
    each_slot = len(rows)/10
    print each_slot
    for i in range(10):
        start = i*each_slot
        end = start + each_slot
        nr = rows[start:end]
        try:
            cur.executemany('INSERT INTO han_names_clean(han_id,han_name,han_name_clean,ngram) values (%s,%s,%s,%s)',nr) 
            con.commit()
            print 'enterd'
        except Exception,e:
            print str(e)

    con.close()


def getCompanyName(company_name):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='app_zoom')
    cur = con.cursor()
    
    cur.execute('select * from master_company_data where company_name COLLATE latin1_swedish_ci like %s COLLATE latin1_swedish_ci',(company_name+'%'))
    c = 0 
    data = []
    for row in cur.fetchall():
        data.append(row[1])
    
    return data


def getAppUrl(app_id):
    con = MySQLdb.connect(host='192.168.1.86', user='root', passwd='password', db='app_shopper')
    cur = con.cursor()
    
    cur.execute('select url from static_details where app_id = %s',(app_id))
    for row in cur.fetchall():
        data = row[0]
    return data

def getParsedFile():
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='app_rank_data')
    cur = con.cursor()
    
    cur.execute('select distinct app_store,date from rank_details ')
    
    data = []
    for row in cur.fetchall():
        data.append(row)
    
    con.close()
    return data

def getParsedFile2():
    con = MySQLdb.connect(host='192.168.1.55', user='root', passwd='password', db='app_shopper')
    cur = con.cursor()
    
    cur.execute('select distinct app_id from app_details')
    
    data = []
    for row in cur.fetchall():
        data.append(row)
    
    con.close()
    return data

def getParsedFile3():
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='app_shopper')
    cur = con.cursor()
    
    cur.execute('select distinct url from app_details_2')
    
    data = []
    for row in cur.fetchall():
        data.append(row)
    
    con.close()
    return data

def addLinkDetails(case_id,case_no,):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='app_shopper')
    cur = con.cursor()
    
    cur.execute('INSERT INTO links_from_google(app_name,appid,url) values (%s,%s,%s)',(app_name,appid,url)) 
    con.commit()
    con.close()
def addZoominfo(job,company_searched,ind_keyword,city,zip,link,name,designation,company,email,phone_number,date):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='dbzoom')
    cur = con.cursor()
    
    cur.execute('INSERT INTO zoomtable_zip(job,company_searched,ind_keyword,city,zip,link,name,designation,company,email,phone_number,date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(job,company_searched,ind_keyword,city,zip,link,name,designation,company,email,phone_number,date)) 
    con.commit()
    con.close()

def addZoominfo1(job,company_searched,ind_keyword,city,zip,link,name,designation,company,email,phone_number,date):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='dbzoom')
    cur = con.cursor()
    
    cur.execute('INSERT INTO zoomtable_zip(job,company_searched,ind_keyword,city,zip,link,name,designation,company,email,phone_number,date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(job,company_searched,ind_keyword,city,zip,link,name,designation,company,email,phone_number,date)) 
    con.commit()
    con.close()
def addCaseDetails(link, name, case_no, judge, court, filed_date, close_date, plaintiff, counter_claimant, plan_attorney, plan_LawFirm, defendant, counter_defendant, defend_attorney, defend_LawFirm, product):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='maxwel')
    cur = con.cursor()
    
    cur.execute('INSERT INTO casedetails(link, name, case_no, judge, court, filed_date, close_date, plaintiff, counter_claimant, plan_attorney, plan_LawFirm, defendant, counter_defendant, defend_attorney, defend_LawFirm, product) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(link, name, case_no, judge, court, filed_date, close_date, plaintiff, counter_claimant, plan_attorney, plan_LawFirm, defendant, counter_defendant, defend_attorney, defend_LawFirm, product)) 
    con.commit()
    mid = cur.lastrowid
    con.close()
    return mid
    

def addPatentDetails(cid, link, patentno, inventors, issuedate, expdate, current_assignee, patent_maker):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='maxwel')
    cur = con.cursor()
    
    cur.execute('INSERT INTO patentdetails(cid, link, patentno, inventors, issuedate, expdate, current_assignee, patent_maker) values (%s,%s,%s,%s,%s,%s,%s,%s)',(cid, link, patentno, inventors, issuedate, expdate, current_assignee, patent_maker)) 
    con.commit()
    
    con.close()



def addRankDetails(app_url,rank_data,category):
    con = MySQLdb.connect(host='192.168.1.55', user='root', passwd='password', db='app_annie_rank')
    cur = con.cursor()
    
    cur.execute('INSERT INTO rank_data(app_url,rank_data,category) values (%s,%s,%s)',(app_url,rank_data,category)) 
    con.commit()
    con.close()


def addMetacriticTVDetails(tv_name, tv_link, total_critic_review, total_user_review, metascore, userscore, summary, network, seasons, genre, released_date, start_url):
    con = MySQLdb.connect(host='192.168.1.55', user='root', passwd='password', db='metacritic_data')
    cur = con.cursor()
    cur.execute('INSERT INTO tv_details (tv_name, tv_link, total_critic_review, total_user_review, metascore, userscore, summary,network, seasons, genre, released_date, start_url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(tv_name, tv_link, total_critic_review, total_user_review, metascore, userscore, summary, network, seasons, genre, released_date, start_url)) 
    tid = cur.lastrowid
    con.commit()
    con.close()
    return tid

def addMetacriticDetails(movie_name,movie_link,total_critic_review,total_user_review,metascore,userscore,summary,runtime,ratng,production,official_site,genre,countries,languages,home_released_date,start_url):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='metacritic_data')
    cur = con.cursor()
    cur.execute('INSERT INTO movie_details_new (movie_name,movie_link,total_critic_review,total_user_review,metascore,userscore,summary,runtime,ratng,production,official_site,genre,countries,languages,home_released_date,start_url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(movie_name,movie_link,total_critic_review,total_user_review,metascore,userscore,summary,runtime,ratng,production,official_site,genre,countries,languages,home_released_date,start_url)) 
    mid = cur.lastrowid
    con.commit()
    con.close()
    return mid
	
def addTvShowReviewDetails(tv_name,review_title,author,author_link,review_text,review_up_count,review_down_count,review_rating,review_date,today_date):
	con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', db='tv_db')
	cur = con.cursor()
	cur.execute('INSERT INTO tv_reviews_table (tv_name,review_title,author,author_link,review_text,review_up_count,review_down_count,review_rating,review_date,today_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(tv_name,review_title,author,author_link,review_text,review_up_count,review_down_count,review_rating,review_date,today_date)) 
	mid = cur.lastrowid
	con.commit()
	con.close()
	return mid

def handleTvError(tv_name,app_url,error):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', db='tv_db')
    cur = con.cursor()
    cur.execute('INSERT INTO tv_error_table (tv_name,app_url,error) values (%s,%s,%s)',(tv_name,app_url,error)) 
    mid = cur.lastrowid
    con.commit()
    con.close()
    return mid

def addTVUserReview(review_id,movie_id,movie_name,date_of_review,review,review_score,reviewed_by,reviewer_link,review_grade,review_grade_type,review_value,thumbs_up,total_thumbs):
    con = MySQLdb.connect(host='192.168.1.55', user='root', passwd='password', db='metacritic_data')
    cur = con.cursor()
    cur.execute('INSERT INTO tv_user_reviews (review_id,movie_id,movie_name,date_of_review,review,review_score,reviewed_by,reviewer_link,review_grade,review_grade_type,review_value,thumbs_up,total_thumbs,today_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(review_id,movie_id,movie_name,date_of_review,review,review_score,reviewed_by,reviewer_link,review_grade,review_grade_type,review_value,thumbs_up,total_thumbs,today_date)) 
    mid = cur.lastrowid
    con.commit()
    con.close()
    return mid

def addUserReview(review_id,movie_id,movie_name,date_of_review,review,review_score,reviewed_by,reviewer_link,review_grade,review_grade_type,review_value,thumbs_up,total_thumbs):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='metacritic_data')
    cur = con.cursor()
    cur.execute('INSERT INTO user_reviews_new (review_id,movie_id,movie_name,date_of_review,review,review_score,reviewed_by,reviewer_link,review_grade,review_grade_type,review_value,thumbs_up,total_thumbs) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(review_id,movie_id,movie_name,date_of_review,review,review_score,reviewed_by,reviewer_link,review_grade,review_grade_type,review_value,thumbs_up,total_thumbs)) 
    mid = cur.lastrowid
    con.commit()
    con.close()
    return mid

def addTVCriticReview(movie_id,movie_name,date_of_review,review,metascore,reviewer,reviewer_link,publisher,publisher_link,review_grade_type,review_grade,full_review_link):
    con = MySQLdb.connect(host='192.168.1.55', user='root', passwd='password', db='metacritic_data')
    cur = con.cursor()
    cur.execute('INSERT INTO tv_critic_reviews (movie_id,movie_name,date_of_review,review,metscore,reviewer,reviewer_link,publisher,publisher_link,review_grade_type,review_grade,full_review_link) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(movie_id,movie_name,date_of_review,review,metascore,reviewer,reviewer_link,publisher,publisher_link,review_grade_type,review_grade,full_review_link)) 
    mid = cur.lastrowid
    con.commit()
    con.close()
    return mid

def addCriticReview(movie_id,movie_name,date_of_review,review,metascore,reviewer,reviewer_link,publisher,publisher_link,review_grade_type,review_grade,full_review_link):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='metacritic_data')
    cur = con.cursor()
    cur.execute('INSERT INTO critic_reviews_new (movie_id,movie_name,date_of_review,review,metscore,reviewer,reviewer_link,publisher,publisher_link,review_grade_type,review_grade,full_review_link) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(movie_id,movie_name,date_of_review,review,metascore,reviewer,reviewer_link,publisher,publisher_link,review_grade_type,review_grade,full_review_link)) 
    mid = cur.lastrowid
    con.commit()
    con.close()
    return mid


def addTVCreditDetails(tv_id, tv_name, credit_person, credit_link, credit, credit_details):
    con = MySQLdb.connect(host='192.168.1.55', user='root', passwd='password', db='metacritic_data')
    cur = con.cursor()
    cur.execute('INSERT INTO tv_credits_details (tv_id, tv_name, credit_person, credit_link, credit, credit_details) values (%s,%s,%s,%s,%s,%s)',(tv_id, tv_name, credit_person, credit_link, credit, credit_details)) 
    mid = cur.lastrowid
    con.commit()
    con.close()
    return mid


def addCreditDetails(movie_id,movie_name,credit_person,credit_link,credit,credit_details):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='metacritic_data')
    cur = con.cursor()
    cur.execute('INSERT INTO credits_details_new (movie_id,movie_name,credit_person,credit_link,credit,credit_details) values (%s,%s,%s,%s,%s,%s)',(movie_id,movie_name,credit_person,credit_link,credit,credit_details)) 
    mid = cur.lastrowid
    con.commit()
    con.close()
    return mid
    
    
def addProcessDetails(process_id,process_name,system_ip,system_name,last_action_time):
    con = MySQLdb.connect(host='192.168.1.55', user='root', passwd='password', db='metacritic_data')
    cur = con.cursor()
    cur.execute('INSERT INTO process_details (process_id,process_name,system_ip,system_name,last_action_time) values (%s,%s,%s,%s,%s)',(process_id,process_name,system_ip,system_name,last_action_time)) 
    mid = cur.lastrowid
    con.commit()
    con.close()
    return mid

def addRankDetailsData(app_name,publisher_name,app_link,publisher_link,category,app_store,date,rank):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='app_rank_data')
    cur = con.cursor()
    
    cur.execute('INSERT INTO rank_details(app_name,publisher_name,app_link,publisher_link,category,app_store,date,rank) values (%s,%s,%s,%s,%s,%s,%s,%s)',(app_name,publisher_name,app_link,publisher_link,category,app_store,date,rank)) 
    con.commit()
    con.close()


def addStaticFileDratails(name,url,app_id):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='app_shopper')
    cur = con.cursor()
    
    cur.execute('INSERT INTO static_details(name,url,app_id) values (%s,%s,%s)',(name,url,app_id)) 
    con.commit()
    con.close()


def addAppDetails(name,url,category,size,average_rating,total_votes,last_changed,developer,developer_link,current_version,description,link_to_store,current_price,times,compatibility,app_id):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='app_shopper')
    cur = con.cursor()
    
    cur.execute('INSERT INTO app_details_2(name,url,category,size,average_rating,total_votes,last_changed,developer,developer_link,current_version,description,link_to_store,current_price,times,compatibility,app_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(name,url,category,size,average_rating,total_votes,last_changed,developer,developer_link,current_version,description,link_to_store,current_price,times,compatibility,app_id)) 
    con.commit()
    con.close()
	
def addAppActivity_new(url,date,details,action):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='app_shopper')
    cur = con.cursor()
    
    cur.execute('INSERT INTO app_activity_2(url,date,details,action) VALUES (%s,%s,%s,%s)',(url,date,details,action)) 
    con.commit()
    con.close()
    

def addAppActivity(url,date,details,action):
    con = MySQLdb.connect(host='192.168.1.55', user='root', passwd='password', db='app_shopper')
    cur = con.cursor()
    
    cur.execute('INSERT INTO app_activity(url,date,details,action) VALUES (%s,%s,%s,%s)',(url,date,details,action)) 
    con.commit()
    con.close()
    
def addOtherApps(url,app_name,app_link):
    con = MySQLdb.connect(host='192.168.1.55', user='root', passwd='password', db='app_shopper')
    cur = con.cursor()
    
    cur.execute('INSERT INTO other_apps(url,app_name,app_link) VALUES (%s,%s,%s)',(url,app_name,app_link)) 
    con.commit()
    con.close()

def addcompanyRevenue(name,revenue,address,web,input):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='dbzoom')
    cur = con.cursor()
    
    cur.execute('INSERT INTO company(name,revenue,address,web,input) VALUES (%s,%s,%s,%s,%s)',(name,revenue,address,web,input)) 
    con.commit()
    con.close()
        


def checkExist(app_url):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='paspassword', db='app_zoom')
    cur = con.cursor()
    
    cur.execute('select * from app_master_data where app_url = %s and app_name <> %s',(app_url,'void'))
    c = 0 
    for row in cur.fetchall():
        c += 1
    if c>0:
        return False
    else:
        return True

def addData(query,position,rank,title,domain,line_1,line_2,line_3,followers):
    con = MySQLdb.connect(host='192.168.1.21', user='root', passwd='password', db='google_ads_crawl')
    cur = con.cursor()
    title = title.encode("utf-8")
    line_1 =  line_1.encode("utf-8")
    line_2 =  line_2.encode("utf-8")
    line_3 =  line_3.encode("utf-8")
    
    cur.execute('insert into add_data_2 (query,position,rank,title,domain,line_1,line_2,line_3,followers) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(query,position,rank,title,domain,line_1,line_2,line_3,followers)) 
    con.commit()
    con.close()


def addMasterData(app_url):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='app_zoom')
    cur = con.cursor()
    
    cur.execute('insert into master_data (app_url) values(%s)',(app_url))
    con.commit()
    appid = cur.lastrowid
    con.close()
    return appid
def addErrorLink(app_url):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='app_zoom')
    cur = con.cursor()
    
    cur.execute('insert into master_data (app_url) values(%s)',(app_url))
    con.commit()
    appid = cur.lastrowid
    con.close()
    return appid


def addAppMasterData(app_name,app_url,developer_name,developer_link,qr_link,price):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='app_zoom')
    cur = con.cursor()
    
    cur.execute('insert into app_master_data (app_name,app_url,developer_name,developer_link,qr_link,price) values(%s,%s,%s,%s,%s,%s)',(app_name,app_url,developer_name,developer_link,qr_link,price)) 
    con.commit()
    appid = cur.lastrowid
    con.close()
    return appid

def addAppChangelog(app_name,app_url,log_type,log_message):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='password', db='app_zoom')
    cur = con.cursor()
    
    cur.execute('insert into app_changelog_data (app_name,app_url,log_type,log_message) values(%s,%s,%s,%s)',(app_name,app_url,log_type,log_message)) 
    con.commit()
    appid = cur.lastrowid
    con.close()
    return appid
