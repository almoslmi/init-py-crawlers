import pytumblr
import sys

tumblr_object = pytumblr.TumblrRestClient(
  'OV6J27Ac4slojHHpj9aqpCT3EwN2g3h9zcuYaCND9yiFtmm3oW',
  'j2mtwSBEjwXyIiZzctonwlqmAht57BfOz7GLaYX3f9kNmFebH5',
  'aXhmvDsYsc9vnMQO8sgXsuXfikQlWbvMuvG5VqKtaKM8MbAf9R',
  'r55YfAPa7TGU5FHAt0jskjIeZoWQ1niWxcvtD5Nf4qM5QUnEt7'
)

tag = raw_input("Enter tag: ")

posts = tumblr_object.tagged(tag)
count = 0

while posts:
	for post in posts:
		count = count + 1
		print count
		# print post
		# print post['type']
		# if post['type'] == 'chat':
		print post
		print post['post_url']
		print post['short_url']
		print
		
	ts = posts[0]['timestamp'] - 1
	
	posts = tumblr_object.tagged(tag, before=ts)
