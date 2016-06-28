import MySQLdb
import os
import datetime

def addsprofiledata(profile):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='link_final')
    cur = con.cursor()
    #print ('INSERT INTO ucla_student_details_2012_linkedin(CCID,First name,Last name,Location,profil count,positions count,profile links) values ("%s","%s","%s","%s","%s","%s","%s")'%tuple(profile))
    #INSERT INTO ucla_student_details_2012_linkedin(CCID,FirstName,LastName,Location,ProfileCount,positionscount,links) values ("12","ac","cd","12","ac","cd","gdfg")
    cur.execute('INSERT INTO ucla_student_details_2012_linkedin(CCID,FirstName,LastName,Location,ProfileCount,PositionsCount,Links) values (%s,%s,%s,%s,%s,%s,%s)',profile)
    con.commit()
    con.close()

  


def addsposdata(position):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='link_final')
    cur = con.cursor()
    
    cur.execute('INSERT INTO posinfo(CCID,FirstName,LastName,Company,Title,CurrentPosition,ProfileLink) values (%s,%s,%s,%s,%s,%s,%s)',position)
    con.commit()
    con.close()
    
def adderrdata(err):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='link_final')
    cur = con.cursor()
    #print ('INSERT INTO error(CCID,First name,Last name,Profile Count,Profile Status) values (%s,%s,%s,%s,%s)'%tuple(err))
    cur.execute('INSERT INTO error(CCID,FirstName,LastName,ProfileCount,ProfileStatus) values (%s,%s,%s,%s,%s)',err)
    con.commit()
    con.close()


def addsindexdata(ind):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='link_ucla')
    cur = con.cursor()
    #print ('INSERT INTO error(CCID,First name,Last name,Profile Count,Profile Status) values (%s,%s,%s,%s,%s)'%tuple(err))
    cur.execute('INSERT INTO index(start,end,process_number,error) values (%s,%s,%s,%s)',ind)
    con.commit()
    con.close()


