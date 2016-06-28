import MySQLdb
import os
import datetime

#l=['32','dfsg','fdsga','fas','fas']

def addsgendata(profile):
    
#db.set_character_set('utf8')
#dbc.execute('SET NAMES utf8;') dbc.execute('SET CHARACTER SET utf8;')
#dbc.execute('SET character_set_connection=utf8;')
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='linkedin_final')
    con.set_character_set('utf8')
    cur = con.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    #print ('INSERT INTO ucla_student_details_2012_linkedin(CCID,First name,Last name,Location,profil count,positions count,profile links) values ("%s","%s","%s","%s","%s","%s","%s")'%tuple(profile))
    #INSERT INTO ucla_student_details_2012_linkedin(CCID,FirstName,LastName,Location,ProfileCount,positionscount,links) values ("12","ac","cd","12","ac","cd","gdfg")
    cur.execute('INSERT INTO general_details(ccid,lid,name,title,location,industry,current,previous,education) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',profile)
    
    con.commit()
    con.close()

def addsedudata(profile):

    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='linkedin_final')
    con.set_character_set('utf8')
    cur = con.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    #print ('INSERT INTO ucla_student_details_2012_linkedin(CCID,First name,Last name,Location,profil count,positions count,profile links) values ("%s","%s","%s","%s","%s","%s","%s")'%tuple(profile))
    #INSERT INTO ucla_student_details_2012_linkedin(CCID,FirstName,LastName,Location,ProfileCount,positionscount,links) values ("12","ac","cd","12","ac","cd","gdfg")
    cur.execute('INSERT INTO education_details(ccid,lid,school,degree,major,duration_start,duration_end) values (%s,%s,%s,%s,%s,%s,%s)',profile)
    
    con.commit()
    con.close()

def addsexpdata(exp):

    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='linkedin_final')
    con.set_character_set('utf8')
    cur = con.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    #print ('INSERT INTO ucla_student_details_2012_linkedin(CCID,First name,Last name,Location,profil count,positions count,profile links) values ("%s","%s","%s","%s","%s","%s","%s")'%tuple(profile))
    #INSERT INTO ucla_student_details_2012_linkedin(CCID,FirstName,LastName,Location,ProfileCount,positionscount,links) values ("12","ac","cd","12","ac","cd","gdfg")
    cur.execute('INSERT INTO experience_details(ccid,lid,title,company_name,duration_start,end,loc) values (%s,%s,%s,%s,%s,%s,%s)',exp)
    
    con.commit()
    con.close()

def addsorgdata(org):

    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='linkedin_final')
    con.set_character_set('utf8')
    cur = con.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    #print ('INSERT INTO ucla_student_details_2012_linkedin(CCID,First name,Last name,Location,profil count,positions count,profile links) values ("%s","%s","%s","%s","%s","%s","%s")'%tuple(profile))
    #INSERT INTO ucla_student_details_2012_linkedin(CCID,FirstName,LastName,Location,ProfileCount,positionscount,links) values ("12","ac","cd","12","ac","cd","gdfg")
    cur.execute('INSERT INTO organization_details(ccid,lid,org_name,position,duration_start,end) values (%s,%s,%s,%s,%s,%s)',org)
    
    con.commit()
    con.close()
#addsexpdata(l)

  

'''
def addsposdata(position):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='link_ucla')
    cur = con.cursor()
    
    cur.execute('INSERT INTO posinfo(CCID,FirstName,LastName,Company,Title,CurrentPosition,ProfileLink) values (%s,%s,%s,%s,%s,%s,%s)',position)
    con.commit()
    con.close()
    
def adderrdata(err):
    con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='link_ucla')
    cur = con.cursor()
    #print ('INSERT INTO error(CCID,First name,Last name,Profile Count,Profile Status) values (%s,%s,%s,%s,%s)'%tuple(err))
    cur.execute('INSERT INTO error(CCID,FirstName,LastName,ProfileCount,ProfileStatus) values (%s,%s,%s,%s,%s)',err)
    con.commit()
    con.close()
'''



