import requests

# Parameters
ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
ACCEPT_ENCODING = 'gzip,deflate,sdch'
ACCEPT_LANGUAGE = 'en-US,en;q=0.8'
CACHE_CONTROL = 'max-age=0'
CONNECTION = 'keep-alive'
CONTENT_LENGTH = 24
CONTENT_TYPE = 'application/x-www-form-urlencoded'
COOKIE = 'PHPSESSID=6g9r6rqiasahbmnrrucmt9jab1; km_ai=25YBKTiJMbTlCT7VDuM7YKcL9Lw%3D; __cfduid=d2da7fc2751f60db2b7be54832c7a36601408716896629; _dc=1; km_uq=; __distillery=9336EBBCA205774D54E1DF7A2221062138814F43; lead411_login_user=m.kumar%40innovaccer.com; lead411_login_pass=innovation123; CISESSION=JmiYSq8QDtwhRDdXK4ungdUw1R2W0StKeLYhwGtq8xO%2BVon1o9Ri%2BFNAgAyUDZT%2BxksLNAFoL9GcXnV27v8vfWwhTrJzDqHHmRYkQuMLZvaTkY2ur2%2BSGAuC0R%2FZVAcjkTvC1rWHazopniIDiD8UgFPjmHRvURsQ8Ly49%2F4VGnmZtdd%2BLTZPa85bjTsgV42zIkEK2ybW2qdDHJ7ntyn5Ly3nytzi3Mzks8xN4rV4FyRFDX8Tx5VF246DwoT%2F4rluovxYqIDSfD5by6XM7s8Ktvf%2BMnRcPqrBix89MTevwfZpxGuvs%2FAQEOlMV7LKo9EjizD%2FxEABO%2BjGdnKsQXj5Yj38tYfE6ChAJXxSayKFj9pwnxgqgOV5sbdjnWAFTKvEvXF5nboBK0gtRHrMMEJDAy0pTPBNyMcDCN7VM9gVmzrkgJKs0em5vE1rxdTXlGZDYAfziceZlZHmPS2UA8QuZbBY40FFmq4MBdeCLwJS5VloLt4yzSDSpucwI9qGOFt1sI8XExOXMEHk4tQuYiQVndlPjV9pCH0ZE6hDnWf%2F6TvuzrfqVJgcg%2BgmISQDSa%2FzTsMMky1eH5%2F8QLT0PTQMcuH8SM5KgkNy1fA8V1XxgjpX4EwUhBVngTAysuUiyAvJslg4rJBJWcg9a%2BfaBJGUGYyCM5rUcBEmDuj5TtFkyFVB%2FLuMr1C9q93n0pNovCO%2B8NwlsjVGwgxc0uQYEXxVzYkJOvrph%2FlTvTH7NwJ6sNkx3ifCidDyAzItlDC7944pNeyelwNeXnGxprmhoiElbWM4YShmDt3Knq6KlfvEufKDWK77QF2CusDAdRl7VLcK1RZGFjbEgFpI%2BmFcb2OX%2BC%2BNGOasEvv3JDIS%2BT8zQKImBMbLMhIy0aCnAM4PwWjAAtTBvpVl3BdfqRJYUHHwFIo0ObqVSCAj4JUC9pDxSZ1jxBKyh8mW3uHRjXWI%2B%2FO9cHminlj3P6uxYIJ8DuSCzw9xZS0q3SsELd7obxgATLwAAIXZz5iIR1yesHdNzjDUsmBMDEuICXgUBphb1ReLW3OjuZL7UTZN1L4R%2BUvbov1c%2B%2F5W54o%2Bk%2FWpWIZBVb1oH5pKCTjC2Su5CYQMu4JId6uAF8N7yAXL2AtM7GklZMSKFNVtmJszC1pe9Q3iRY9Muxsfi5oEpJ6cAPAiHTlkd5PE%2BfRamx2jsAPv7H6d2C%2FmuFGA%2BJGG7bsvuDWrBWPfYGUeRKeJWhVIIc5jng%2BYG0A5z2EA2p0zl5T6g83pRx3vBs0u5BE9SVFwD6CDjAFHBkFnG0iiT26JfaA4gQnR0V5lEVOcApuRwZSCfRTgAkNMj3cd1qsRjfBiPgrlYDvjGApbWrA6VKwq660whVjEmqNUcrQnrMVmXxLgMpcp5B%2FR%2Fm%2BfAFku9MsGa1bhcxAE; _ga=GA1.2.1044926857.1408716899; kvcd=1408717386341; km_vs=1; km_lv=1408717386'
HOST = 'www.lead411.com'
ORIGIN = 'http://www.lead411.com'
REFERER = 'http://www.lead411.com/search/freehand_search'
USER_AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'

req_params = {'Accept':ACCEPT,
	'Accept-Encoding':ACCEPT_ENCODING,
	'Accept-Language':ACCEPT_LANGUAGE,
	'Cache-Control':CACHE_CONTROL,
	'Connection':CONNECTION,
	'Content-Length':CONTENT_LENGTH,
	'Content-Type':CONTENT_TYPE,
	'Cookie':COOKIE,
	'Host':HOST,
	'Origin':ORIGIN,
	'Referer':REFERER,
	'User-Agent':USER_AGENT
}

form_data = {'query':'washington',
	'submit':''
}

r = requests.post('http://www.lead411.com/search/freehand_search', 
	data=form_data,
	headers=req_params,
	cookies={'Cookie':COOKIE},
	auth=('m.kumar@innovaccer.com', 'innovation123')
)


print r.text

