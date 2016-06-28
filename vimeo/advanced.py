from vimeo import VimeoClient

vimeo = VimeoClient("fd43cedfe52f09848142cbd3501ea0a5")

a = vimeo.channels()
b = vimeo.videos(query="battle")
c = vimeo.videos.get("87374427")

for i in a.items():
	print i
	print

print
print
print
print
print

for i in b.items():
	print i
	print

print
print
print

print "Comments"
print c.comments()
print
print "Credits"
print c.credits()
print
print "Likes"
print c.likes()
print
print "Stats"
print c.stats()
print
print "Tags"
print c.tags()
