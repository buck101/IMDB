
import urllib2
import cookielib
import string
import re
#from HTMLParser import HTMLParser
from sgmllib import SGMLParser
import os
import MySQLdb
import imdb
import sys


enable_proxy = False
enable_cookie = False
enable_debug = False

my_url = "http://www.baidu.com"

headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Referer':my_url
}

class Xun_Lei_Hao_Html_Parser(SGMLParser):

    def __init__(self):
        SGMLParser.__init__(self)
        self.is_ul = False
        self.is_movie = False
        self.movies = {} 
        self.id = ''
        self.name = ''
        self.re_movie = re.compile(r'\w+\/(\w+\.html)')

    def start_ul(self, attrs):
        for attr in attrs:
            if attr[1] == 'llst06':
                self.is_ul = True

    def start_a(self, attrs):
        if self.is_ul:
    	    href = [v for k, v in attrs if k == 'href']
            match = self.re_movie.search(str(href))
    	    if match:
                self.is_movie = True
                print ''.join(match.groups())
                self.id = ''.join(match.groups()) 
                #self.movies.extend(match.groups())

    def handle_data(self, text):
        if self.is_ul and self.is_movie:
            print unicode(text,'GBK').encode('UTF-8')
            self.name = unicode(text,'GBK').encode('UTF-8')
            #self.movies_name.extend(unicode(text,'GBK').encode('UTF-8'))

    def end_a(self):
        if self.is_movie:
            self.is_movie = False
            self.movies[self.id] = self.name

    def end_ul(self):
        if self.is_ul:
            self.is_ul = False

class Xun_Lei_Hao_Spider:

    def __init__(self, url, dir_name):
    	self.url = url
    	self.dir_name = dir_name
        self.html_parser = Xun_Lei_Hao_Html_Parser()
    
    def page_dl_list(self, begin_page, end_page):
    	for i in range(begin_page, end_page + 1):
    	    remote_file_name = "list_5_" + str(i) + ".html"
    	    local_file_name = "list_5_" + string.zfill(i, 3) + ".html"
            if os.path.isfile(self.dir_name + local_file_name):
    	        f = open(self.dir_name + local_file_name, 'r+')
    	        print "R[" + self.url + remote_file_name + "]"
    	        page_content = ''.join(f.readlines())
    	        f.close()
            else:
    	        page_content = urllib2.urlopen(self.url + remote_file_name).read()
    	        f = open(self.dir_name + local_file_name, 'w+')
    	        print "W[" + self.url + remote_file_name + "]"
    	        f.write(page_content)
    	        f.close()
            self.html_parser.feed(page_content)

    def page_dl_movies(self):
        print "Total:", len(self.html_parser.movies)
    	for (k, v) in self.html_parser.movies.items():
    	    remote_file_name = k
            local_file_name = k
            #local_file_name = v + ".html"
            if os.path.isfile(self.dir_name + "/movies/" + local_file_name):
    	        f = open(self.dir_name + "/movies/" + local_file_name, 'r+')
    	        print "R>>>>" + self.url + remote_file_name
    	        page_content = ''.join(f.readlines())
    	        f.close()
            else:
    	        page_content = urllib2.urlopen(self.url + remote_file_name).read()
    	        f = open(self.dir_name + "/movies/" + local_file_name, 'w+')
    	        print "D>>>>" + self.url + remote_file_name
    	        f.write(page_content)
    	        f.close()
            self.html_parser.feed(page_content)







if enable_debug:
    httpHandler = urllib2.HTTPHandler(debuglevel = 1)
    httpsHandler = urllib2.HTTPSHandler(debuglevel = 1)
    opener = urllib2.build_opener(httpHandler, httpsHandler)
else:
    opener = urllib2.build_opener()

if enable_proxy:
    proxy_handler = urllib2.ProxyHandler({"http" : 'http://some-proxy.com:8080'})
    opener.add_handler(proxy_handler)

if enable_cookie:
    cookie = cookielib.CookieJar()
    opener.add_handler(urllib2.HTTPCookieProcessor(cookie))

urllib2.install_opener(opener)

#req.add_header('User-Agent', 'fake-client')
#req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')

#postdata = ''
#req = urllib2.Request(my_url, data = postdata, headers = headers)
#req = urllib2.Request(my_url)

try:
    #res = urllib2.urlopen(req, timeout = 10)
    #print res.geturl()
    #print res.info()
    #if res.geturl() != my_url:
    #	print "#############redirect ", res.geturl()
    
    #if enable_cookie:
    #   for item in cookie:
    #   	print 'Name = ' + item.name
    #   	print 'Value = ' + item.value
    
    #html = res.read()
    #print html
    
    web_spider = Xun_Lei_Hao_Spider("http://xunleihao.com/jingdiandianying/", "xunleihao/")
    #web_spider.page_dl_list(1, 163)
    #web_spider.page_dl_movies()



except urllib2.URLError, e:
    if hasattr(e, 'reason'):
    	print e.reason
    elif hasattr(e, 'code'):
    	print e.code

except urllib2.HTTPError, e:
    if hasattr(e, 'reason'):
    	print e.reason
    elif hasattr(e, 'code'):
    	print e.code


#ia = imdb.IMDb('sql', 'mysql://root:@localhost/imdb')
ia = imdb.IMDb('http')
movie = 'The Founding of a Republic' 
results = ia.search_movie(movie)
print results

##############writing to DB
#conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '')
#cursor = conn.cursor()
#cursor.execute("set names utf8")
#
#try:
#    cursor.execute("create database movies")
#
#except MySQLdb.Error, e:
#    print 'MySQL Error: %d %s' % (e.args[0], e.args[1])
#    conn.rollback()
#    sys.exit()
#else:
#    cursor.close()
#    conn.close()

