import requests

# Logging in
f = open('login.html', 'w')
login = requests.get('http://www.lead411.com//autologin.php?email=m.kumar@innovaccer.com&password=innovation123&redirect=http://www.lead411.com/')
login_cookie = login.cookies
f.write(login.text.encode('utf-8'))

# freehand_search
f = open('free_hand.html', 'w')
params = {"query":"washington", "submit":""}
freehand_search = requests.post('http://www.lead411.com/search/freehand_search', data=params)
f.write(freehand_search.text.encode('utf-8'))

# freehand_search
f = open('free_hand_login.html', 'w')
params = {"query":"washington", "submit":""}
freehand_search_login = requests.post('http://www.lead411.com/search/freehand_search', data=params, cookies=login_cookie)
f.write(freehand_search_login.text.encode('utf-8'))

# JSON data