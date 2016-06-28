import traceback
import csv
import glob
import MySQLdb

def addTweetDataMany(tweetList):
    try:
        con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='ab_twitter')
        cur = con.cursor()
       
        cur.executemany('INSERT INTO adobe(date,tweet,user) values (%s,%s,%s)',[sub for sub in tweetList])
        con.commit()
        con.close()
    except Exception, e:
        print traceback.format_exc()

source = raw_input("Enter the source:")
filename = 'D:/Innovaccer/Projects/Abhishek borah - twitter data/Input-Files/distinct csv/' + source + '.csv'
with open(filename, 'rb') as f:
    try:
        reader = csv.reader(f)
        count = 0
        tweetList = []

        for row in reader:
            # print row
            tweetTuple = tuple(row)
            # print tweetTuple
            tweetList.append(tweetTuple)
            count += 1
            if count >= 10000:
                print count
                addTweetDataMany(tweetList)
                count = 0
                tweetList = []
                print count,tweetList
                # break
        print count
        addTweetDataMany(tweetList)
        count = 0
        tweetList = []
        print count,tweetList
        # if 'RT ' in row[1]:
        #   print row
        # break
    except Exception, e:
        print traceback.format_exc()