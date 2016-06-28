import csv
rows = [r[0] for r in csv.reader(open('suggestions.csv','rb'),delimiter=',')]
print rows
rows = [r[1] for r in csv.reader(open('suggestions.csv','rb'),delimiter=',')]
print rows