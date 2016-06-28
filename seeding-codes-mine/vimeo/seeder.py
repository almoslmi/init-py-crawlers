import os
import vimeo
from bs4 import BeautifulSoup
import json
import time

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

				result = []
				for j in fields:
					result.append(s[k])

			g.write(json.dumps(s))

			time.sleep(1)
		except Exception, e:
			print str(e)
			time.sleep(10)
			continue
