import MySQLdb
import os
import datetime	

hostLocal = '127.0.0.1'
hostCloud = '173.194.251.56'

	
def bid_history_fetch(item_id,automatic_bid,bid_history_found):
	con = MySQLdb.connect(host=hostCloud, user='root', passwd='root', db='ebay_api')
	cur = con.cursor()
	try:
		s = "select count(*) FROM ebay_api.bid_history2 where item_id = '%s' and automatic_bid = '%s' and bid_history_found = '%s'"%(item_id,automatic_bid,bid_history_found)
		cur.execute(s)
		con.commit()
		result = cur.fetchall()
		for row in result:
			count = row[0]
		con.close()
		return count
	except Exception,e:
		print str(e)
		print "problem in sql bid fetch"

def item_specifics_insert(title, item_id, category_name,seller_username,item_url,payment,location,ship_locations,shipping_type,shipping_cost,currency,handling_time,bid_count, current_price,buyItNowAvailable,time_left,merchant, value, type, valid_location, item_cond,description1,description2,start_price,bid_url,category_id,start_time,end_time,feedback_score,positive_feedback_percent,city,state,country):
	con = MySQLdb.connect(host=hostCloud, user='root', passwd='root', db='ebay_api')
	cur = con.cursor()
	try:
		cur.execute("INSERT INTO item_specifics2(item_id, title, category_name,seller_username,item_url,payment,location,ship_locations,shipping_type,shipping_cost,currency,handling_time,bid_count, current_price,buyItNowAvailable,time_left,merchant, value, type, valid_locations, item_cond,starting_price,bid_url,description1,description2,category_id,start_time,end_time,feedback_score,positive_feedback_percent,city,state,country) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(item_id, title, category_name,seller_username,item_url,payment,location,ship_locations,shipping_type,shipping_cost,currency,handling_time,bid_count, current_price,buyItNowAvailable,time_left,merchant, value, type, valid_location, item_cond,start_price,bid_url,description1,description2,category_id,start_time,end_time,feedback_score,positive_feedback_percent,city,state,country))
		con.commit()
		con.close()
	except Exception,e:
		print str(e)
		print "problem in sql insert item"

def bid_history_insert(item_id,bid_url,bidder_name,amount,time,automatic_bid,bid_history_found):
	con = MySQLdb.connect(host=hostCloud, user='root', passwd='root', db='ebay_api')
	cur = con.cursor()
	try:
		cur.execute("INSERT INTO bid_history2(item_id,bid_url,bidder_name,amount,time,automatic_bid,bid_history_found) values (%s,%s,%s,%s,%s,%s,%s)",(item_id,bid_url,bidder_name,amount,time,automatic_bid,bid_history_found))
		con.commit()
		con.close()
	except Exception,e:
		print str(e)
		print "problem in sql insert bid"
