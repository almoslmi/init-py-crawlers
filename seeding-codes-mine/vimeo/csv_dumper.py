import json
import os
import csv


filenames = os.listdir('json_dumps')

fields = [
	'link'
]

for filename in filenames:
	print filename
	f = open("json_dumps/" + filename, 'r')
	content = f.read()
	json_dict = json.loads(content)

	posts = json_dict['body']['data']

	for i in posts:
		s = {}

		for j in fields:
			if j in i.keys() and j not in s.keys():
				print j
				if i[j] != None:
					t = i[j].encode('utf-8')
				s[j] = t

		result = []
		for j in fields:
			result.append(s[j])