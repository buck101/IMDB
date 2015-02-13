
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
