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


enable_proxy = False
enable_cookie = False
enable_debug = False

my_url = "http://www.baidu.com"

headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Referer':my_url
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
        self.movie = movie()
        self.article_contents = []

        self.re_movie = re.compile(r'\w+\/(\w+\.html)')

        #self.re_cn_name = re.compile(ur'◎译　　名　(.*)')
        #【中文名称】：

        #self.re_cn_name_1 = re.compile(ur'\u25ce\u8bd1\u3000\u3000\u540d\u3000(.*?)\u0020\u25ce')
        self.re_cn_name_1 = re.compile(ur'\u540f')

		#◎中文片名　风雨双流星  (\u25ce\u4e2d\u6587\u7247\u540d\u3000\u98ce\u96e8\u53cc\u6d41\u661f  \u25ce)
        self.re_cn_name_2 = re.compile(ur'\u25ce\u4e2d\u6587\u7247\u540d\u3000+(.+?)\u0020+\u25ce')
        #self.re_cn_name_2 = re.compile(ur'\u302d')

        #self.re_cn_name_3 = re.compile(ur'\u25ce\u4e2d\u6587\u7247\u540d\u3000(.*?)\u0020\u0020\u25ce')
        self.re_cn_name_3 = re.compile(ur'\u5643')



        #self.re_en_name = re.compile(ur'◎片　　名　(.*)')
        self.re_en_name = re.compile(ur'\u25ce\u7247\u3000\u3000\u540d\u3000(.*?)\u0020\u25ce')

        #self.re_year = re.compile(ur'◎年　　代　(\d+)')
        self.re_year = re.compile(ur'\u25ce\u5e74\u3000\u3000\u4ee3\u3000(.*?)\u0020\u25ce')

        #self.re_category = re.compile(ur'◎类　　别　(.*)')
        self.re_category = re.compile(ur'\u25ce\u7c7b\u3000\u3000\u522b\u3000(.*?)\u0020\u25ce')

        #self.re_country = re.compile(ur'◎国　　家　(.*)')
        self.re_country = re.compile(ur'\u25ce\u56fd\u3000\u3000\u5bb6\u3000(.*?)\u0020\u25ce')

    def start_ul(self, attrs):
        for attr in attrs:
            if attr[1] == 'llst06':
                self.is_ul = True

    def start_a(self, attrs):
        if self.is_ul:
    	    href = [v for k, v in attrs if k == 'href']
            search = self.re_movie.search(str(href))
    	    if search:
                self.is_movie = True
                self.id = ''.join(search.groups()) 

    def start_div(self, attrs):
        for attr in attrs:
            if attr[1] == 'articlecontent':
                self.is_article_content = True

    def handle_data(self, text):
        if self.is_ul and self.is_movie:
            self.movie.show_name = text.decode('GBK').encode('UTF-8')

        if self.is_article_content:
            self.article_contents.append(text.decode('GBK'))


    def end_a(self):
        if self.is_movie:
            self.is_movie = False
            self.movies[self.id] = self.movie

    def end_ul(self):
        if self.is_ul:
            self.is_ul = False

	def end_div(self):
		if self.is_article_content:
			self.is_article_content = False
			text = ' '.join(self.article_contents)

			all_found = True;

			search = self.re_cn_name_1.search(text)
			if search:
				self.movie.cn_name = ''.join(search.groups())
				print "cname=", self.movie.cn_name
			else:
				search = self.re_cn_name_2.search(text)
				if search:
					self.movie.cn_name = ''.join(search.groups())
					print "cname=", self.movie.cn_name
				else:
					search = self.re_cn_name_3.search(text)
					if search:
						self.movie.cn_name = ''.join(search.groups())
						print "cname=", self.movie.cn_name
					else:
						print "cname not found"
						all_found = False
			#print repr(self.movie.cn_name)
			time.sleep(10)

            #search = self.re_year.search(text)
    	    #if search:
            #    self.movie.year = int(''.join(search.groups()))
            #    print "year ", self.movie.year
            #else:
            #    print "year not found"
            #    all_found = False

            #search = self.re_en_name.search(text)
    	    #if search:
            #    self.movie.en_name = ''.join(search.groups())
            #    print "ename ", self.movie.en_name
            #else:
            #    print "ename not found"
            #    all_found = False

            #search = self.re_category.search(text)
    	    #if search:
            #    self.movie.category = ''.join(search.groups())
            #    print "category ", self.movie.category
            #else:
            #    print "category not found"
            #    all_found = False

            #search = self.re_country.search(text)
    	    #if search:
            #    self.movie.country = ''.join(search.groups())
            #    print "country ", self.movie.country
            #else:
            #    print "country not found"
            #    all_found = False

			if all_found == False:
				print text
				print repr(text)
			
			self.article_contents = []
			time.sleep(1)



            #if self.movie.en_name == '':
            #    print "en_name not found"
            #    time.sleep(1)

            #if self.movie.cn_name == '':
            #    print "cn_name not found"
            #    time.sleep(1)

            #if self.movie.country == '':
            #    print "country not found"
            #    time.sleep(1)

            #if self.movie.category == '':
            #    print "category not found"
            #    time.sleep(1)

            #if self.movie.year == 0:
            #    print "year not found"
            #    time.sleep(1)

            #self.movie.__init__()

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
    	        #print "R[" + self.url + remote_file_name + "]"
    	        page_content = ''.join(f.readlines())
    	        f.close()
            else:
    	        page_content = urllib2.urlopen(self.url + remote_file_name).read()
    	        f = open(self.dir_name + local_file_name, 'w+')
    	        #print "W[" + self.url + remote_file_name + "]"
    	        f.write(page_content)
    	        f.close()
            self.html_parser.feed(page_content)

    def page_dl_movies(self):
        print "Total:", len(self.html_parser.movies)
        time.sleep(2) 
    	for (k, v) in self.html_parser.movies.items():
    	    remote_file_name = k
            local_file_name = k
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
    #       print 'Name = ' + item.name
    #       print 'Value = ' + item.value
    
    #html = res.read()
    #print html
    
    web_spider = Xun_Lei_Hao_Spider("http://xunleihao.com/jingdiandianying/", "xunleihao/")
    web_spider.page_dl_list(1, 1)
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

