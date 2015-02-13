# -*- coding: utf-8 -*- 
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
import time
import copy

enable_proxy = False
enable_cookie = False
enable_debug = False

my_url = "http://www.baidu.com"

headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Referer':my_url
}

C2D = {
        'JDDY':'xunleihao/JDDY/',
        'OMDY':'xunleihao/OMDY/',
        'RHDY':'xunleihao/RHDY/',
        'GTDY':'xunleihao/GTDY/',
        'DLDY':'xunleihao/DLDY/',
        'OMJ':'xunleihao/OMJ/',
        'RHJ':'xunleihao/RHJ/',
        'GTJ':'xunleihao/GTJ/',
        'DLJ':'xunleihao/DLJ/',
        'ZYP':'xunleihao/ZYP/',
        'DM':'xunleihao/DM/',
}

C2I = {
        'JDDY':5,
        'OMDY':1,
        'RHDY':2,
        'GTDY':3,
        'DLDY':4,
        'OMJ':6,
        'RHJ':7,
        'GTJ':8,
        'DLJ':9,
        'ZYP':10,
        'DM':11,
}

class movie:
    def __init__(self):
        self.imdb_id = ''
        self.cn_name = '' 
        self.en_name = '' 
        self.country = '' 
        self.year = 0 
        self.category = '' 
        self.imdb_score = 0 
        self.imdb_vote = 0 
        self.db_score = 0 
        self.db_vote = 0 
        self.status = 0 
        self.comment = '' 
        ##############
        self.show_name = ''

class Xun_Lei_Hao_Html_Parser(SGMLParser):

    def __init__(self):
        SGMLParser.__init__(self)
        self.is_ul = False
        self.is_movie = False
        self.is_article_content = False

        self.movies = {}
        self.id = ''
        self.category = ''
        self.movie = movie()
        self.article_contents = []

        self.re_movie = re.compile(r'\w+\/(\w+\.html)')


    def start_ul(self, attrs):
        for attr in attrs:
            if attr[1] == 'llst06':
                self.is_ul = True

    def end_ul(self):
        if self.is_ul:
            self.is_ul = False

    # for dl_list
    def start_a(self, attrs):
        if self.is_ul:
    	    href = [v for k, v in attrs if k == 'href']
            search = self.re_movie.search(str(href))
    	    if search:
                self.is_movie = True
                self.id = ''.join(search.groups()) 

    def end_a(self):
        if self.is_movie:
            self.is_movie = False
            self.movie.category = self.category
            self.movies[self.id] = copy.copy(self.movie)


    # for dl_movie
    def start_div(self, attrs):
        for attr in attrs:
            if attr[1] == 'articlecontent':
                self.is_article_content = True

    def end_div(self):
    	if self.is_article_content:
    	    self.is_article_content = False
    	    text = ' '.join(self.article_contents).replace('\r\n', '')

            #self.movie.__init__()

    def handle_data(self, text):
        if self.is_ul and self.is_movie:
            self.movie.show_name = text.decode('GBK', 'ignore')

        if self.is_article_content:
            self.article_contents.append(text.decode('GBK', 'ignore'))



class Xun_Lei_Hao_Spider:

    def __init__(self):
        self.html_parser = Xun_Lei_Hao_Html_Parser()
    
    def page_dl_list(self, url, category):
    	self.url = url
    	self.dir_name = C2D[category]
        self.html_parser.category = category

        i = 1
        while (True):
    	    remote_file_name = "list_5_" + str(i) + ".html"
    	    local_file_name = "list_5_" + string.zfill(i, 3) + ".html"
            if os.path.isfile(self.dir_name + local_file_name):
    	        f = open(self.dir_name + local_file_name, 'r+')
    	        print "R[" + self.url + remote_file_name + "]"
    	        page_content = ''.join(f.readlines())
    	        f.close()
            else:
    	        page_content = urllib2.urlopen(self.url + remote_file_name).read()
                if page_content.decode('GBK', 'ignore').find(ur'\u60a8\u8bbf\u95ee\u7684\u5730\u5740\u4e0d\u5b58\u5728') != -1:
                    print self.url + remote_file_name, "not found 404"
                    break
    	        f = open(self.dir_name + local_file_name, 'w+')
    	        print "W[" + self.url + remote_file_name + "]"
    	        f.write(page_content)
    	        f.close()
            self.html_parser.feed(page_content)
            i = i + 1

    def page_dl_movies(self):
        print "Total:", len(self.html_parser.movies)
        time.sleep(2) 
    	for (k, v) in self.html_parser.movies.items():
    	    remote_file_name = k
            local_file_name = k
            if os.path.isfile("xunleihao/movies/" + local_file_name):
    	        f = open("xunleihao/movies/" + local_file_name, 'r+')
    	        print "R>>>>" + self.url + remote_file_name
    	        page_content = ''.join(f.readlines())
    	        f.close()
            else:
    	        page_content = urllib2.urlopen(self.url + remote_file_name).read()
    	        f = open("xunleihao/movies/" + local_file_name, 'w+')
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
    #       print 'Name = ' + item.name
    #       print 'Value = ' + item.value
    
    #html = res.read()
    #print html
    
    web_spider = Xun_Lei_Hao_Spider()
    web_spider.page_dl_list('http://xunleihao.com/jingdiandianying/', 'JDDY')
    web_spider.page_dl_list('http://xunleihao.com/oumeidianying/', 'OMDY')
    web_spider.page_dl_list('http://xunleihao.com/rihandianying/', 'RHDY')
    web_spider.page_dl_list('http://xunleihao.com/gangtaidianying/', 'GTDY')
    web_spider.page_dl_list('http://xunleihao.com/daludianying/', 'DLDY')
    web_spider.page_dl_list('http://xunleihao.com/oumeiju/', 'OMJ')
    web_spider.page_dl_list('http://xunleihao.com/rihanju/', 'RHJ')
    web_spider.page_dl_list('http://xunleihao.com/gangtaiju/', 'GTJ')
    web_spider.page_dl_list('http://xunleihao.com/daluju/', 'DLJ')
    web_spider.page_dl_list('http://xunleihao.com/zongyipian/', 'ZYP')
    web_spider.page_dl_list('http://xunleihao.com/dongman/', 'DM')
    web_spider.page_dl_movies()


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
#ia = imdb.IMDb('http')
#movie = 'sex' 
#results = ia.search_movie(movie)
#print results

##############writing to DB
conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '')
cursor = conn.cursor()
cursor.execute("set names utf8")
cursor.execute("set autocommit=1")

try:
    cursor.execute("use movies")
    cursor.execute("truncate table xunleihao")
    for (k, v) in web_spider.html_parser.movies.items():
        cursor.execute("insert into xunleihao values('%s','%s','%s')"  % (k, v.show_name.encode('UTF-8'), v.category));
        conn.commit()

except MySQLdb.Error, e:
    print 'MySQL Error: %d %s' % (e.args[0], e.args[1])
    conn.rollback()
    sys.exit()
else:
    cursor.close()
    conn.close()

