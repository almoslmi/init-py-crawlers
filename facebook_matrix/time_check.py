from time import gmtime, strftime
print "start-time: "+strftime("%Y-%m-%d %H:%M:%S", gmtime())
i=1
while i<=(971*971):
	print i
	i=i+1
print "end-time: "+strftime("%Y-%m-%d %H:%M:%S", gmtime())
