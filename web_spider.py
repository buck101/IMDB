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

        #self.found_count = 0
        #self.not_found_count = 0


        #self.re_cn_name = []
        ##【中文片名】父辈的旗帜/硫磺岛浴血战/硫磺岛的英雄们/战火旗迹  
        #self.re_cn_name.append(re.compile(ur'\u3010\u4e2d\u6587\u7247\u540d\u3011.(.+?)\u3010'))

        ##◎中文译名 彗星美人  
        #self.re_cn_name.append(re.compile(ur'\u25ce\u4e2d\u6587\u8bd1\u540d.(.+?)\u25ce'))
	##◎中文片名　风雨双流星  (\u25ce\u4e2d\u6587\u7247\u540d\u3000\u98ce\u96e8\u53cc\u6d41\u661f  )
        #self.re_cn_name.append(re.compile(ur'\u25ce\u4e2d\u6587\u7247\u540d.(.+?)\u25ce'))
        ##中文名称：光荣岁月 
        #self.re_cn_name.append(re.compile(ur'\u4e2d\u6587\u540d\u79f0.(.+?)\u0020+'))

        ##◎中 文 名: 
        #self.re_cn_name.append(re.compile(ur'\u25ce\u4e2d.*?\u6587.*?\u540d.(.+?)\u25ce'))
        ##中 文 名: 败家仔  
        #self.re_cn_name.append(re.compile(ur'\u4e2d.*\u6587.*\u540d.(.+?)\u0020+'))

        ##【译　　名】　小鬼大间谍/非常小特务/神童特工/特工神童  【 ()
        #self.re_cn_name.append(re.compile(ur'\u3010\u8bd1.*?\u540d\u3011(.+?)\u3010'))
        ##◎译　　名  拨云见日 ◎ (\u25ce\u8bd1\u3000\u3000\u540d  \u62e8\u4e91\u89c1\u65e5 )
        #self.re_cn_name.append(re.compile(ur'\u25ce\u8bd1.*?\u540d.(.+?)\u25ce'))
        ##译　　名：爱再来一次  
        #self.re_cn_name.append(re.compile(ur'\u8bd1.*?\u540d.(.+?)\u0020+'))


        ##片名：爱的逃兵  　
        #self.re_cn_name.append(re.compile(ur'\u7247\u540d.(.+?)\u0020+'))
        ##别名：挥洒烈爱/笔姬别恋   
        #self.re_cn_name.append(re.compile(ur'\u522b\u540d.(.+?)\u0020+'))
        ##◎片　　名 迷途英雄  
        #self.re_cn_name.append(re.compile(ur'\u25ce\u7247\u3000*\u540d(.+?)\u0020+'))
        ##【别　　名】蝙蝠侠：开战时刻/蝙蝠侠前传/蝙蝠侠5：侠影之谜
        #self.re_cn_name.append(re.compile(ur'\u3010\u522b.*\u540d\u3011(.+?)\u0020+'))
        ##【片 　　名】冒险王  
        #self.re_cn_name.append(re.compile(ur'\u3010\u7247.*\u540d\u3011(.+?)\u0020+'))

        ##【外文译名】铁道员/鉄道員  
        #self.re_cn_name.append(re.compile(ur'\u3010\u5916\u6587\u8bd1\u540d\u3011(.+?)\u0020+'))


        ##self.re_en_name = re.compile(ur'◎片　　名　(.*)')
        #self.re_en_name = re.compile(ur'\u25ce\u7247\u3000\u3000\u540d\u3000(.*?)\u0020\u25ce')

        ##self.re_year = re.compile(ur'◎年　　代　(\d+)')
        #self.re_year = re.compile(ur'\u25ce\u5e74\u3000\u3000\u4ee3\u3000(.*?)\u0020\u25ce')

        ##self.re_category = re.compile(ur'◎类　　别　(.*)')
        #self.re_category = re.compile(ur'\u25ce\u7c7b\u3000\u3000\u522b\u3000(.*?)\u0020\u25ce')

        ##self.re_country = re.compile(ur'◎国　　家　(.*)')
        #self.re_country = re.compile(ur'\u25ce\u56fd\u3000\u3000\u5bb6\u3000(.*?)\u0020\u25ce')

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
            self.movie.show_name = text.decode('GBK', 'ignore')

        if self.is_article_content:
            self.article_contents.append(text.decode('GBK', 'ignore'))


    def end_a(self):
        if self.is_movie:
            self.is_movie = False
            self.movies[self.id] = copy.copy(self.movie)

    def end_ul(self):
        if self.is_ul:
            self.is_ul = False

    def end_div(self):
    	if self.is_article_content:
    	    self.is_article_content = False
    	    text = ' '.join(self.article_contents).replace('\r\n', '')

    	    #found = False;

            #for p in self.re_cn_name:
            #    search = p.search(text)
    	    #    if search:
    	    #        self.movie.cn_name = ''.join(search.groups())
            #        found = True
            #        break
    	    #if found:
    	    #	print "cname=", self.movie.cn_name.encode('UTF-8')
            #    self.found_count = self.found_count + 1 
    	    #else:
            #    self.not_found_count = self.not_found_count + 1
    	    #	print "cname not found"
            #    print text.encode('UTF-8')
            #    print repr(text)


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

	    #self.article_contents = []
	    #time.sleep(1)



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
    web_spider.page_dl_list(1, 163)
    web_spider.page_dl_movies()

    #print web_spider.html_parser.found_count
    #print web_spider.html_parser.not_found_count



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
    cursor.execute("truncate table xlh_fileid2show_name")
    for (k, v) in web_spider.html_parser.movies.items():
        #print "insert into xlh_fileid2show_name values('%s','%s')"  % (k, v.show_name.encode('UTF-8'));
        cursor.execute("insert into xlh_fileid2show_name values('%s','%s')"  % (k, v.show_name.encode('UTF-8')));
        conn.commit()

except MySQLdb.Error, e:
    print 'MySQL Error: %d %s' % (e.args[0], e.args[1])
    conn.rollback()
    sys.exit()
else:
    cursor.close()
    conn.close()

