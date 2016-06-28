import os
import vimeo
from bs4 import BeautifulSoup
import json
import time
import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="seeds")
c = conn.cursor()

try:
	c.execute('''CREATE TABLE seeds 
		(`id` int AUTO_INCREMENT PRIMARY KEY, 
			`source` varchar(100), 
			`url` varchar(255) UNIQUE, 
			`priority` int,
			`is_active` BOOLEAN,
			`timestamp` TIMESTAMP);
	''')
	conn.commit()
except Exception,e:
	print str(e)
	pass

f = open('colors.txt', 'r')
h = open('errors.txt', 'w')

fields = [
	'link'
]

primary_colors = []

v = vimeo.VimeoClient('3943ea0c766357085254467fd1336cdb')

for i in f:
	primary_colors.append(i.strip())

for i in primary_colors:
	if i not in os.listdir('seeds'):
		os.mkdir('seeds/' + i)

for i in primary_colors:
	print i

	count = 0

	while True:
		try:
			count = count + 1
			print i, count
			file_location = 'seeds/' + i + '/' + i + str(count) + '.txt'
			print file_location
			g = open(file_location, 'w')

			t = v.videos(query=i, page=count, sort='date')
			print type(t)
			s = json.dumps(t)
			s = json.loads(s)
			print type(s)
			
			posts = s['body']['data']

			for j in posts:
				s = {}

				for k in fields:
					if k in j.keys() and k not in s.keys():
						if j[k] != None:
							t = j[k].encode('utf-8')
						s[k] = t
						print k, s[k]

				results = []
				for j in fields:
					results.append(s[k])
				
				source = 'vimeo'
				url = results[0]
				priority = 0
				is_active = 1

				try:
					command = 'INSERT INTO seeds (source, url, priority, is_active) VALUES ("%s", "%s", "%s", "%s")'%(source, url, priority, is_active)
					c.execute(command)
					conn.commit()
				except Exception, e:
					print str(e)
					continue

			g.write(json.dumps(s))

			time.sleep(1)
		except Exception, e:
			print str(e)
			time.sleep(10)
			continue
