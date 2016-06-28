import MySQLdb
import os
import datetime

#hostname = "173.194.108.59"
hostname = "127.0.0.1"
dbname = "conferance_calls"
passwrd = "password"




def enterMasterDetails(ticker_symbol,company_name,quarter,datetime_of_call,timezone,presentation_changeover,qna_changeover):
	con = MySQLdb.connect(host=hostname, user='root', passwd=passwrd, db=dbname) 
    	cur = con.cursor() 
    	res =cur.execute("INSERT  ignore INTO call_master_details(ticker_symbol,company_name,quarter,datetime_of_call,timezone,presentation_changeover,qna_changeover) values(%s,%s,%s,%s,%s,%s,%s)",(ticker_symbol,company_name,quarter,datetime_of_call,timezone,presentation_changeover,qna_changeover))
    	call_id = cur.lastrowid
    	con.commit()
    	con.close()
    	return call_id


def enterParticipantsDetails(call_id,participant_name,participant_org,participant_designation,participant_type):
	con = MySQLdb.connect(host=hostname, user='root', passwd=passwrd, db=dbname) 
    	cur = con.cursor() 
    	res =cur.execute("INSERT  ignore INTO call_participants_details(call_id,participant_name,participant_org,participant_designation,participant_type) values(%s,%s,%s,%s,%s)",(call_id,participant_name,participant_org,participant_designation,participant_type))
    	#print res
    	con.commit()
    	con.close()

def enterChangeoverDetails(call_id,name_of_speaker,speaker_text):
	con = MySQLdb.connect(host=hostname, user='root', passwd=passwrd, db=dbname) 
    	cur = con.cursor() 
    	res =cur.execute("INSERT  ignore INTO call_changeover_details(call_id,speaker_name,speaker_text) values(%s,%s,%s)",(call_id,name_of_speaker.strip(),speaker_text))
    	con.commit()
    	con.close()

