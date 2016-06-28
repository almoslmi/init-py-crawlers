import traceback
import requests

url1 = 'http://www.businesswire.com/portal/site/home/template.BINARYPORTLET/search/resource.process/'
# ?javax.portlet.tpst=92055fbcbec7e639f1f554100d908a0c&javax.portlet.rst_92055fbcbec7e639f1f554100d908a0c_searchTerm=apple&javax.portlet.rst_92055fbcbec7e639f1f554100d908a0c_resultsPage='
# url2 = '&javax.portlet.rst_92055fbcbec7e639f1f554100d908a0c_searchType=news'
proxyDict = {"http"  : "http://67.43.42.193:8080"}
try:
	for i in range(20,3044):
		print i
		# nurl = url1 + str(i) + url2
		nurl = url1
		print nurl
		#payload = 'javax.portlet.tpst=92055fbcbec7e639f1f554100d908a0c&javax.portlet.rst_92055fbcbec7e639f1f554100d908a0c_searchTerm=apple&javax.portlet.rst_92055fbcbec7e639f1f554100d908a0c_resultsPage=3&javax.portlet.rst_92055fbcbec7e639f1f554100d908a0c_searchType=news&javax.portlet.rid_92055fbcbec7e639f1f554100d908a0c=searchBox&javax.portlet.rcl_92055fbcbec7e639f1f554100d908a0c=cacheLevelPage&javax.portlet.begCacheTok=com.vignette.cachetoken&javax.portlet.endCacheTok=com.vignette.cachetoken'
		params = {'javax.portlet.tpst':'92055fbcbec7e639f1f554100d908a0c',
				'javax.portlet.rst_92055fbcbec7e639f1f554100d908a0c_searchTerm':'apple',
				'javax.portlet.rst_92055fbcbec7e639f1f554100d908a0c_resultsPage':1,
				'javax.portlet.rst_92055fbcbec7e639f1f554100d908a0c_searchType':'news',
				'javax.portlet.rid_92055fbcbec7e639f1f554100d908a0c':'searchBox',
				'javax.portlet.rcl_92055fbcbec7e639f1f554100d908a0c':'cacheLevelPage',
				'javax.portlet.begCacheTok':'com.vignette.cachetoken',
				'javax.portlet.endCacheTok':'com.vignette.cachetoken'}
		params['javax.portlet.rst_92055fbcbec7e639f1f554100d908a0c_resultsPage'] = i
		cook = dict(cookies_are='portal.JSESSIONID=6qh8T44BFrgPQ5nXqXZL8slnkhJpC2zhl7KyxhbCyh5XQhJ11Nn9!301063728!1767710261; visitor_id19392=129152324; __utma=217664773.602187055.1408792706.1408792706.1408792706.1; __utmb=217664773.5.10.1408792706; __utmc=217664773; __utmz=217664773.1408792706.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)')
		r = requests.get(nurl, proxies=proxyDict, params = params, headers  ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/28.0','X-Requested-With':'XMLHttpRequest'})
		print r.status_code

		htmlText = r.text.encode('utf8')
		# print htmlText
		filename = './Dump/dump-page' + str(i) + '.html'
		with open(filename, 'wb') as outf:
			outf.write(htmlText)
		# break
except Exception,e:
	print traceback.format_exc()
	
