import MySQLdb
def select_db(cur,con,usr,pss,dbnam,tbl_nm):
    sql_query="select * from "+tbl_nm
    cur.execute(sql_query)
    return cur
con = MySQLdb.connect(host="localhost", user="root", passwd="", db="innovaccer")
cur = con.cursor()
cursor=select_db(cur,con,"root","","innovaccer","linkedin_lawyer_input")
for (innovaccer_id,lawyer_id,name,freq) in cursor:
	print str(innovaccer_id)+"-"+str(lawyer_id)+"-"+name+"-"+str(freq)
	
	# exit()
con.commit()
con.close()
