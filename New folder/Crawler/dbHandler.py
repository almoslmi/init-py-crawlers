import MySQLdb
import os
import datetime
import dbHandler

def fetch_link():
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='link_final')
    cur = con.cursor()
    #print ('INSERT INTO ucla_student_details_2012_linkedin(CCID,First name,Last name,Location,profil count,positions count,profile links) values ("%s","%s","%s","%s","%s","%s","%s")'%tuple(profile))
    #INSERT INTO ucla_student_details_2012_linkedin(CCID,FirstName,LastName,Location,ProfileCount,positionscount,links) values ("12","ac","cd","12","ac","cd","gdfg")
    #cur.execute('select Links from ucla_student_details_2012_linkedin where app_url = %s and app_name <> %s',(app_url,'void'))
    cur.execute('select CCID,Links from private_prof')
    c = [] 
    for row in cur.fetchall():
        c.append(row)
    return c
    con.commit()
    con.close()
