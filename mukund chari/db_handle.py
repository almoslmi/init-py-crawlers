import MySQLdb
import os
import datetime
import re
class dbHandler:
	def dbConn(self,hst,usr,pss,dbnm):
		con = MySQLdb.connect(host=hst, user=usr, passwd=pss, db=dbnm)
		cur = con.cursor()
		return [con,cur]

	def select_db(self,cur,tbl_nm,whre):
		sql_query="select * from "+tbl_nm+" where "+whre
		cur.execute(sql_query)
		data=[]
		for row in cur.fetchall():
			data.append(row)
		return data

	def update_db(self,con,cur,tbl_nm,set_update,whre):
		st_up=""
		for k,v in set_update.items():
			# v=v.encode('utf-8')
			# print k
			# print v
			st_up=st_up+""+k+"="+"'"+(re.escape(str(v)))+"'"+" ,"
		sql_query="Update "+tbl_nm+" set "+st_up.strip(',')+"where "+whre
		# sql_query=sql_query.replace('\\','-')
		# print sql_query
		cur.execute(sql_query)
		con.commit()

	def insert_db(self,con,cur,tbl_nm,ins_values):
		col="("
		val=") values ("
		for k,v in ins_values.items():
			col=col+k+","
			val=val+"'"+(re.escape(v)).encode('utf-8')+"',"
		col=col[:(len(col)-1)]
		val=val[:(len(val)-1)]
		val=val+")"
		sql_query="Insert into "+tbl_nm+""+col+""+val+""
		cur.execute(sql_query)
		con.commit()

