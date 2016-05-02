import urllib2, re, mechanize, cookielib, time
from bs4 import BeautifulSoup

#AUTHOR: JORGE WEBSEC
#TWITTER: @JORGEWEBSEC
#EMAIL: JORGE@QUANTIKA14.COM
#LICENSE: GNU V.3
#****VIVA TRIANA****

br = mechanize.Browser()
cj = cookielib.LWPCookieJar() 
br.set_cookiejar(cj) 
br.set_handle_equiv( True ) 
br.set_handle_gzip( True ) 
br.set_handle_redirect( True ) 
br.set_handle_referer( True ) 
br.set_handle_robots( False ) 

br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 ) 

br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ] 

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
	return TAG_RE.sub('', text)

def sqlite_insert(table, row):
	connection = sqlite3.connect('meetupUserDB',  timeout=10)
	cols = ', '.join('"{}"'.format(col) for col in row.keys())
	vals = ', '.join(':{}'.format(col) for col in row.keys())
	sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
	connection.cursor().execute(sql, row)
	connection.commit()

for i in range(1, 9999999):
	try:
		url = "http://www.meetup.com/es-ES/members/" + str(i) + "/?op=&memberId=" + str(i)
		print url
		html = br.open(url).read()
		soup = BeautifulSoup(html)
		name = soup.find("span", {"class": "memName fn"})
		locality = soup.find("span", {"class": "locality"})
		bio = soup.find("div", {"class": "D_memberProfileContentItem"})
		meetups = soup.findAll("a", {"class": "omnCamp omngj_pswg4"})
		print remove_tags(str(name)), remove_tags(str(locality)), remove_tags(str(bio)), remove_tags(str(meetups))
		try:
			sqlite_insert('users', {'username': name, 'locality': locality, 'bio': bio, 'meetups': meetups})
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]
	except urllib2.HTTPError, e:
		print e
		time.sleep(10)

	

