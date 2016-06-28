import requests
import json
import csv

obj = raw_input("Enter the object:").lower()
act = raw_input("Enter the association:").lower()

act = '_'.join(act.split())

print obj
print act


r = requests.get('http://vimeo.com/api/v2/brad/appears_in.json')



# print r.text
j = json.loads(r.text)
with open('json.csv', 'wb') as csvfile:
	w = csv.writer(csvfile)
	for key in j:
		if type(key) == type([]):
			for i in key:
				w.writerow([].append(i))
		else:
			for i, j in key.items():
				l = []
				l.append(i)
				l.append(j)
				w.writerow(l)
