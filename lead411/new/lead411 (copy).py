import requests
import ast

# Getting Query
print "Enter Your Query"
query = raw_input()

# Parameters
ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
ACCEPT_ENCODING = 'gzip,deflate,sdch'
ACCEPT_LANGUAGE = 'en-US,en;q=0.8'
CACHE_CONTROL = 'max-age=0'
CONNECTION = 'keep-alive'
CONTENT_LENGTH = 24
CONTENT_TYPE = 'application/x-www-form-urlencoded'
COOKIE = 'PHPSESSID=6g9r6rqiasahbmnrrucmt9jab1; km_ai=25YBKTiJMbTlCT7VDuM7YKcL9Lw%3D; __cfduid=d2da7fc2751f60db2b7be54832c7a36601408716896629; _dc=1; km_uq=; __distillery=9336EBBCA205774D54E1DF7A2221062138814F43; lead411_login_user=m.kumar%40innovaccer.com; lead411_login_pass=innovation123; CISESSION=JmiYSq8QDtwhRDdXK4ungdUw1R2W0StKeLYhwGtq8xO%2BVon1o9Ri%2BFNAgAyUDZT%2BxksLNAFoL9GcXnV27v8vfWwhTrJzDqHHmRYkQuMLZvaTkY2ur2%2BSGAuC0R%2FZVAcjkTvC1rWHazopniIDiD8UgFPjmHRvURsQ8Ly49%2F4VGnmZtdd%2BLTZPa85bjTsgV42zIkEK2ybW2qdDHJ7ntyn5Ly3nytzi3Mzks8xN4rV4FyRFDX8Tx5VF246DwoT%2F4rluovxYqIDSfD5by6XM7s8Ktvf%2BMnRcPqrBix89MTevwfZpxGuvs%2FAQEOlMV7LKo9EjizD%2FxEABO%2BjGdnKsQXj5Yj38tYfE6ChAJXxSayKFj9pwnxgqgOV5sbdjnWAFTKvEvXF5nboBK0gtRHrMMEJDAy0pTPBNyMcDCN7VM9gVmzrkgJKs0em5vE1rxdTXlGZDYAfziceZlZHmPS2UA8QuZbBY40FFmq4MBdeCLwJS5VloLt4yzSDSpucwI9qGOFt1sI8XExOXMEHk4tQuYiQVndlPjV9pCH0ZE6hDnWf%2F6TvuzrfqVJgcg%2BgmISQDSa%2FzTsMMky1eH5%2F8QLT0PTQMcuH8SM5KgkNy1fA8V1XxgjpX4EwUhBVngTAysuUiyAvJslg4rJBJWcg9a%2BfaBJGUGYyCM5rUcBEmDuj5TtFkyFVB%2FLuMr1C9q93n0pNovCO%2B8NwlsjVGwgxc0uQYEXxVzYkJOvrph%2FlTvTH7NwJ6sNkx3ifCidDyAzItlDC7944pNeyelwNeXnGxprmhoiElbWM4YShmDt3Knq6KlfvEufKDWK77QF2CusDAdRl7VLcK1RZGFjbEgFpI%2BmFcb2OX%2BC%2BNGOasEvv3JDIS%2BT8zQKImBMbLMhIy0aCnAM4PwWjAAtTBvpVl3BdfqRJYUHHwFIo0ObqVSCAj4JUC9pDxSZ1jxBKyh8mW3uHRjXWI%2B%2FO9cHminlj3P6uxYIJ8DuSCzw9xZS0q3SsELd7obxgATLwAAIXZz5iIR1yesHdNzjDUsmBMDEuICXgUBphb1ReLW3OjuZL7UTZN1L4R%2BUvbov1c%2B%2F5W54o%2Bk%2FWpWIZBVb1oH5pKCTjC2Su5CYQMu4JId6uAF8N7yAXL2AtM7GklZMSKFNVtmJszC1pe9Q3iRY9Muxsfi5oEpJ6cAPAiHTlkd5PE%2BfRamx2jsAPv7H6d2C%2FmuFGA%2BJGG7bsvuDWrBWPfYGUeRKeJWhVIIc5jng%2BYG0A5z2EA2p0zl5T6g83pRx3vBs0u5BE9SVFwD6CDjAFHBkFnG0iiT26JfaA4gQnR0V5lEVOcApuRwZSCfRTgAkNMj3cd1qsRjfBiPgrlYDvjGApbWrA6VKwq660whVjEmqNUcrQnrMVmXxLgMpcp5B%2FR%2Fm%2BfAFku9MsGa1bhcxAE; _ga=GA1.2.1044926857.1408716899; kvcd=1408717386341; km_vs=1; km_lv=1408717386'
HOST = 'www.lead411.com'
ORIGIN = 'http://www.lead411.com'
REFERER = 'http://www.lead411.com/search/freehand_search'
USER_AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'

req_params = {'Accept':ACCEPT,
	'Accept-Encoding':ACCEPT_ENCODING,
	'Accept-Language':ACCEPT_LANGUAGE,
	'Cache-Control':CACHE_CONTROL,
	'Connection':CONNECTION,
	'Content-Length':CONTENT_LENGTH,
	'Content-Type':CONTENT_TYPE,
	'Cookie':COOKIE,
	'Host':HOST,
	'Origin':ORIGIN,
	'Referer':REFERER,
	'User-Agent':USER_AGENT
}

form_data = {'query':'washington',
	'submit':''
}

# Logging in
f = open('login.html', 'w')
login = requests.get('http://www.lead411.com//autologin.php?email=m.kumar@innovaccer.com&password=innovation123&redirect=http://www.lead411.com/')
login_cookie = login.cookies
f.write(login.text.encode('utf-8'))

# freehand_search
f = open('free_hand.html', 'w')
params = {"query":"washington", "submit":""}
freehand_search = requests.post('http://www.lead411.com/search/freehand_search', data=params)
f.write(freehand_search.text.encode('utf-8'))

# freehand_search
f = open('free_hand_login.html', 'w')
freehand_search_login = requests.post('http://www.lead411.com/search/freehand_search', 
		data=form_data, 
		headers=req_params,
		cookies=login_cookie,
		auth=('m.kumar@innovaccer.com', 'innovation123')
	)
f.write(freehand_search_login.text.encode('utf-8'))

# freehand_search
f = open('free_hand_login2.html', 'w')
freehand_search_login_2 = requests.post('http://www.lead411.com/search/freehand_search', 
		data=form_data, 
		headers=req_params,
		cookies={'Cookie':COOKIE},
		auth=('m.kumar@innovaccer.com', 'innovation123')
	)
f.write(freehand_search_login_2.text.encode('utf-8'))

# Total JSON Data
form_data_total_json = {
	'US_zipcodes':'',
	'range':'5',
	'State_array':'',
	'Title_array':'',
	'user_search_string':'chicago',
	'SIC_codes':'',
	'US_areacodes':'',
	'Technology_array':'',
	'Industry_Codes':'',
	'Press_event_data':'null#2014-08-23#2014-08-23',
	'FilterRevenue':'all,1,2,3,4,5,6,7,8,9,10,11',
	'FilterEmployees':'all,1,2,3,4,5,6,7,8,9,10,11',
	'FilterLevel':'all,c_level,vp_level,director_level,manager_level',
	'FilterType':'resultTypeAll,companyResultsAll,peopleResultsAny,resultNormal,,yearlyRevDesc',
	'description':'description',
	'teamShare':'',
	'user_id':'73728',
	'company_description_string':'',
	'title_keyword':'',
	'currently_hiring_title':'',
	'keyword_match_text':'anyMatch'
}

form_data_total_json['user_search_string'] = query

f = open('json_total_login.json', 'w')

json_total_login = requests.post('http://www.lead411.com/search/getTotalDataJSON', 
	data=form_data_total_json, 
	headers=req_params,
	cookies={'Cookie':COOKIE},
	auth=('m.kumar@innovaccer.com', 'innovation123')
)

json_total = ast.literal_eval(json_total_login.text.strip())
print type(json_total)
print json_total
f.write(json_total_login.text.encode('utf-8'))

num_records = int(json_total['iTotalDisplayRecords'])

# JSON data

form_data_json = {
	'sEcho':1,
	'iColumns':36,
	'sColumns': '',
	'iDisplayStart':0,
	'iDisplayLength':125,
	'mDataProp_0':'checkbox',
	'mDataProp_1':'result_type',
	'mDataProp_2':'img_open_c',
	'mDataProp_3':'clink_phone',
	'mDataProp_4':'location',
	'mDataProp_5':'state',
	'mDataProp_6':'contacts',
	'mDataProp_7':'img_open_p',
	'mDataProp_8':'title',
	'mDataProp_9':'DCL',
	'mDataProp_10':'city',
	'mDataProp_11':'get_data',
	'mDataProp_12':'hlink',
	'mDataProp_13':'address',
	'mDataProp_14':'phone',
	'mDataProp_15':'plink',
	'mDataProp_16':'zip',
	'mDataProp_17':'ticker',
	'mDataProp_18':'flink',
	'mDataProp_19':'revenue',
	'mDataProp_20':'revenueFilter',
	'mDataProp_21':'employees',
	'mDataProp_22':'stock_price_html',
	'mDataProp_23':'employee_level_filter',
	'mDataProp_24':'total_contacts',
	'mDataProp_25':'executive_level',
	'mDataProp_26':'vp_level',
	'mDataProp_27':'director_level',
	'mDataProp_28':'manager_level',
	'mDataProp_29':'staff',
	'mDataProp_30':'other',
	'mDataProp_31':'type',
	'mDataProp_32':'address2',
	'mDataProp_33':'fax',
	'mDataProp_34':'clink',
	'mDataProp_35':'description',
	'sSearch':'',
	'bRegex':'false',
	'sSearch_0':'',
	'bRegex_0':'false',
	'bSearchable_0':'true',
	'sSearch_1':'',
	'bRegex_1':'false',
	'bSearchable_1':'true',
	'sSearch_2':'',
	'bRegex_2':'false',
	'bSearchable_2':'true',
	'sSearch_3':'',
	'bRegex_3':'false',
	'bSearchable_3':'true',
	'sSearch_4':'',
	'bRegex_4':'false',
	'bSearchable_4':'true',
	'sSearch_5':'',
	'bRegex_5':'false',
	'bSearchable_5':'true',
	'sSearch_6':'',
	'bRegex_6':'false',
	'bSearchable_6':'true',
	'sSearch_7':'',
	'bRegex_7':'false',
	'bSearchable_7':'true',
	'sSearch_8':'',
	'bRegex_8':'false',
	'bSearchable_8':'true',
	'sSearch_9':'',
	'bRegex_9':'false',
	'bSearchable_9':'true',
	'sSearch_10':'',
	'bRegex_10':'false',
	'bSearchable_10':'true',
	'sSearch_11':'',
	'bRegex_11':'false',
	'bSearchable_11':'true',
	'sSearch_12':'',
	'bRegex_12':'false',
	'bSearchable_12':'true',
	'sSearch_13':'',
	'bRegex_13':'false',
	'bSearchable_13':'true',
	'sSearch_14':'',
	'bRegex_14':'false',
	'bSearchable_14':'true',
	'sSearch_15':'',
	'bRegex_15':'false',
	'bSearchable_15':'true',
	'sSearch_16':'',
	'bRegex_16':'false',
	'bSearchable_16':'true',
	'sSearch_17':'',
	'bRegex_17':'false',
	'bSearchable_17':'true',
	'sSearch_18':'',
	'bRegex_18':'false',
	'bSearchable_18':'true',
	'sSearch_19':'',
	'bRegex_19':'false',
	'bSearchable_19':'true',
	'sSearch_20':'',
	'bRegex_20':'false',
	'bSearchable_20':'true',
	'sSearch_21':'',
	'bRegex_21':'false',
	'bSearchable_21':'true',
	'sSearch_22':'',
	'bRegex_22':'false',
	'bSearchable_22':'true',
	'sSearch_23':'',
	'bRegex_23':'false',
	'bSearchable_23':'true',
	'sSearch_24':'',
	'bRegex_24':'false',
	'bSearchable_24':'true',
	'sSearch_25':'',
	'bRegex_25':'false',
	'bSearchable_25':'true',
	'sSearch_26':'',
	'bRegex_26':'false',
	'bSearchable_26':'true',
	'sSearch_27':'',
	'bRegex_27':'false',
	'bSearchable_27':'true',
	'sSearch_28':'',
	'bRegex_28':'false',
	'bSearchable_28':'true',
	'sSearch_29':'',
	'bRegex_29':'false',
	'bSearchable_29':'true',
	'sSearch_30':'',
	'bRegex_30':'false',
	'bSearchable_30':'true',
	'sSearch_31':'',
	'bRegex_31':'false',
	'bSearchable_31':'true',
	'sSearch_32':'',
	'bRegex_32':'false',
	'bSearchable_32':'true',
	'sSearch_33':'',
	'bRegex_33':'false',
	'bSearchable_33':'true',
	'sSearch_34':'',
	'bRegex_34':'false',
	'bSearchable_34':'true',
	'sSearch_35':'',
	'bRegex_35':'false',
	'bSearchable_35':'true',
	'iSortingCols':'0',
	'bSortable_0':'false',
	'bSortable_1':'false',
	'bSortable_2':'false',
	'bSortable_3':'false',
	'bSortable_4':'false',
	'bSortable_5':'false',
	'bSortable_6':'false',
	'bSortable_7':'false',
	'bSortable_8':'false',
	'bSortable_9':'false',
	'bSortable_10':'true',
	'bSortable_11':'true',
	'bSortable_12':'true',
	'bSortable_13':'true',
	'bSortable_14':'true',
	'bSortable_15':'true',
	'bSortable_16':'true',
	'bSortable_17':'true',
	'bSortable_18':'true',
	'bSortable_19':'true',
	'bSortable_20':'true',
	'bSortable_21':'true',
	'bSortable_22':'true',
	'bSortable_23':'true',
	'bSortable_24':'true',
	'bSortable_25':'true',
	'bSortable_26':'true',
	'bSortable_27':'true',
	'bSortable_28':'true',
	'bSortable_29':'true',
	'bSortable_30':'true',
	'bSortable_31':'true',
	'bSortable_32':'true',
	'bSortable_33':'true',
	'bSortable_34':'true',
	'bSortable_35':'true',
	'user_search_string':'chicago',
	'keyword_match_text':'anyMatch',
	'company_description_string':'',
	'range':'5',
	'currently_hiring_title':'',
	'FilterType':'resultTypeAll,companyResultsAll,peopleResultsAny,resultNormal,,yearlyRevDesc',
	'title_keyword':'',
	'Tracker_Search':'',
	'Press_event_data':'',
	'iTotalRecordsFound':'',
	'FilterEmployees':'all,1,2,3,4,5,6,7,8,9,10,11',
	'FilterRevenue':'all,1,2,3,4,5,6,7,8,9,10,11',
	'FilterLevel':'all,c_level,vp_level,director_level,manager_level'
}

count = 0
form_data_json['user_search_string'] = query
print num_records
while count < num_records:
	print count
	f = open('json_' + query + str(count/125) + '.json', 'w')
	form_data_json['iDisplayStart'] = count

	json_login = requests.post('http://www.lead411.com/search/getDataJSON', 
		data=form_data_json, 
		headers=req_params,
		cookies={'Cookie':COOKIE},
		auth=('m.kumar@innovaccer.com', 'innovation123')
	)

	f.write(json_login.text.encode('utf-8'))

	count = count + 125