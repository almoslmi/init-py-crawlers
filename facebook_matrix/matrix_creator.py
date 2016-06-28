import json
import excelHelper
import csv
from time import gmtime, strftime
print "start-time: "+strftime("%Y-%m-%d %H:%M:%S", gmtime())

def array_creator(input_string):
	if "}{" in input_string:
		input_string=input_string[1:len(input_string)-1]
		string_arr=input_string.split("}{")
	elif "," in input_string or "and" in input_string:
		input_string=input_string.replace(" and",",")
		string_arr=input_string.split(", ")
	else:
		string_arr=[input_string]
	return string_arr

def array_comparator(arr1,arr2):
	sc=0
	for a1 in arr1:
		for a2 in arr2:
			if a1==a2:
				sc=sc+1
	return sc

def csv_writer(filename,info):
    write_item = csv.writer(open(filename,"ab+"))
    write_item.writerow(info)
    # write_item.close`

workbook_access ='test.xlsx'

csv_writer("comparative_matrix.csv",["innovaccer_id1","link1","innovaccer_id2","link2","interested in","language","gender","religion","politics","education","current_city","places_lived","work","music","movie","tv shows","books","Total Score"])
csv_writer("fullerton_matrix.csv",["innovacer_id","fb url","fullerton score"])

col=[""]
query1 =  excelHelper.excelHelper().readExcel(workbook_access,0,971,0)
for (inno_id1,fbid1,fb_url1,gender1,interest1,relation1,languages1,bday1,anniv1,rel_view1,po_view1,email1,education1,current_city1,places_lived1,work1,music1,movie1,tv1,book1) in query1:
	# print fb_url1
	col.insert(len(col),str(inno_id1))
	
# print col
# exit()
csv_writer("adjacency_matrix.csv",col)

i=1

# while i<3:
query1 =  excelHelper.excelHelper().readExcel(workbook_access,0,971,0)
for (inno_id1,fbid1,fb_url1,gender1,interest1,relation1,languages1,bday1,anniv1,rel_view1,po_view1,email1,education1,current_city1,places_lived1,work1,music1,movie1,tv1,book1) in query1:

	lang_arr1=array_creator(languages1)
	edu_arr1=array_creator(education1)
	place_arr1=array_creator(places_lived1)
	work_arr1=array_creator(work1)
	music_arr1=array_creator(music1)
	movie_arr1=array_creator(movie1)
	tv_arr1=array_creator(tv1)
	book_arr1=array_creator(book1)
	score_arr=[str(inno_id1)]
	# j=0
	# while j<i:
	# 	score_arr.insert(len(score_arr),"0")
	# 	j=j+1
	query2 =  excelHelper.excelHelper().readExcel(workbook_access,0,971,0)
	this_score=0
	for (inno_id2,fbid2,fb_url2,gender2,interest2,relation2,languages2,bday2,anniv2,rel_view2,po_view2,email2,education2,current_city2,places_lived2,work2,music2,movie2,tv2,book2) in query2:
		interest_score=0
		lang_score=0
		gender_score=0
		rel_score=0
		pol_score=0
		edu_score=0
		city_score=0
		places_score=0
		work_score=0
		music_score=0
		movie_score=0
		tv_score=0
		book_score=0
		# total_Score=0
		if fb_url1!=fb_url2:
			lang_arr2=array_creator(languages2)
			edu_arr2=array_creator(education2)
			place_arr2=array_creator(places_lived2)
			work_arr2=array_creator(work2)
			music_arr2=array_creator(music2)
			movie_arr2=array_creator(movie2)
			tv_arr2=array_creator(tv2)
			book_arr2=array_creator(book2)

			
			lang_score=array_comparator(lang_arr1,lang_arr2)
			edu_score=array_comparator(edu_arr1,edu_arr2)
			places_score=array_comparator(place_arr1,place_arr2)
			work_score=array_comparator(work_arr1,work_arr2)
			music_score=array_comparator(music_arr1,music_arr2)
			movie_score=array_comparator(movie_arr1,movie_arr2)
			tv_score=array_comparator(tv_arr1,tv_arr2)
			book_score=array_comparator(book_arr1,book_arr2)
		
			if interest1==interest2:
				interest_score=1
			if gender1==gender2:
				gender_score=1
			if rel_view1==rel_view2:
				rel_score=1
			if po_view1==po_view2:
				pol_score=1
			if current_city1==current_city2:
				city_score=1

			if languages1=='NULL' or languages2=='NULL':
				lang_score=0
			if education1=='NULL' or education2=='NULL':
				edu_score=0
			if places_lived1=='NULL' or places_lived2=='NULL':
				places_score=0
			if work1=='NULL' or work2=='NULL':
				work_score=0
			if music1=='NULL' or music2=='NULL':
				music_score=0
			if movie1=='NULL' or movie2=='NULL':
				movie_score=0
			if tv1=='NULL' or tv2=='NULL':
				tv_score=0
			if book1=='NULL' or book2=='NULL':
				book_score=0

			if interest1=='NULL' or interest2=='NULL':
				interest_score=0
			if gender1=='NULL' or gender2=='NULL':
				gender_score=0
			if rel_view1=='NULL' or rel_view2=='NULL':
				rel_score=0
			if po_view1=='NULL' or po_view2=='NULL':
				pol_score=0
			if current_city1=='NULL' or current_city2=='NULL':
				city_score=0

			

		total_Score=interest_score+lang_score+gender_score+rel_score+pol_score+edu_score+city_score+places_score+work_score+music_score+movie_score+tv_score+book_score
		
		csv_writer("comparative_matrix.csv",[inno_id1,fb_url1,inno_id2,fb_url2,interest_score,lang_score,gender_score,rel_score,pol_score,edu_score,city_score,places_score,work_score,music_score,movie_score,tv_score,book_score,total_Score])
		
		this_score=this_score+total_Score

		score_arr.insert(len(score_arr),total_Score)

	csv_writer("fullerton_matrix.csv",[inno_id1,fb_url1,this_score])

	csv_writer("adjacency_matrix.csv",score_arr)

	i=i+1
print "end-time: "+strftime("%Y-%m-%d %H:%M:%S", gmtime())
