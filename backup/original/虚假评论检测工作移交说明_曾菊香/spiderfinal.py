# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import json
import re
import urllib2 
from bs4 import BeautifulSoup
import cookielib
import MySQLdb
import time
import codecs

def getresultstr(result,number):#convert list to unicode string 
    resultstr=u""
    for i in range(number,len(result)-number):
        resultstr+=result[i]
    return resultstr

def getnameid(html):
    getnameid=re.compile(r'(?<=user-id\=\")\d+')
    result=getnameid.findall(html)
    resultstr=getresultstr(str(result),1)
    return resultstr

def getname(html):
    getname=re.compile(r'<p class="name"><a target="_blank" title="" href="/member/\d+">[\s\S]*?</a></p>')
    resultware=getname.findall(html)
    result=re.sub(r'<p class="name"><a target="_blank" title="" href="/member/\d+">|</a></p>',"",str(resultware))
    resultstr=getresultstr(result,1)
    return resultstr

def getcontribution(html):
    soup = BeautifulSoup(html)
    resultware=soup.find_all('span',class_="user-rank-rst")
    getnumber=re.compile(r'\d+\-\d+')
    result=getnumber.findall(str(resultware))
    resultstr=getresultstr(str(result),2)
    return resultstr


def getreview(html):
    getreviewcontent=re.compile(r'<div class="J_brief-cont">[\s\S]*?</div>')
    middleware=getreviewcontent.findall(html)
    resultware=re.sub(r'<div class="J_brief-cont">|</div>',"",str(middleware))
    result=re.sub(r'\s+|\\n',"",str(resultware))
    resultstr=getresultstr(result,1)
    return resultstr

def getuserinforank(html):
    getuserinforanknumber=re.compile(r'(?<=class="item-rank-rst irr-star)\d+')
    result=getuserinforanknumber.findall(html)
    resultstr=getresultstr(str(result),1)
    return resultstr

def gettime(html):
    gettime=re.compile(r'(?<=<span class="time">)\d{2}\-\d{2}')
    result=gettime.findall(html)
    result=str(result)
    resultstr=getresultstr(result,2)
    return resultstr

def getcost(html):
    getcost=re.compile(r'(?<=<span class="comm-per">)[\s\S]*?(?=</span>)')
    result=getcost.findall(html)
    resultstr=getresultstr(result,1)
    return resultstr


def getshop(html):
    getshop=re.compile(r'(?<=<h2 class="misc-name">)[\s\S]*?(?=</h2>)')
    result=getshop.findall(html)
    resultstr=getresultstr(str(result),1)
    return resultstr


def getrst1(html):#the first classic review
    try:
        getshop=re.compile(r'(?<=<span class="rst">)[\s\S]*?(?=<em class="col-exp">)')
        middleware=getshop.findall(html)
    #middleware=soup.find_all('span',class_="rst")
        result=middleware[0]
        return result
    except Exception,e:
        print Exception,":",e
        return "None"


def getrst2(html):#the second classic review
    try:
        getshop=re.compile(r'(?<=<span class="rst">)[\s\S]*?(?=<em class="col-exp">)')
        middleware=getshop.findall(html)
        #middleware=soup.find_all('span',class_="rst")
        result=middleware[1]
        return result
    except Exception,e:
        print Exception,":",e
        return "None"

def getrst3(html):#the third classic review
    try:
        getshop=re.compile(r'(?<=<span class="rst">)[\s\S]*?(?=<em class="col-exp">)')
        middleware=getshop.findall(html)
        #middleware=soup.find_all('span',class_="rst")
        result=middleware[2]
        return result
    except Exception,e:
        print Exception,":",e
        return "None"

def gethtml(url):
    cookieJar = cookielib.MozillaCookieJar()#setcookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    headers={#set headers
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.87 Safari/537.36 QQBrowser/9.2.5584.400',
        'Accept'    :'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control':'max-age=0',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'www.dianping.com',
        'Upgrade-Insecure-Requests':'1',
        'Cookie':'showNav=javascript:; navCtgScroll=0; _hc.v=69ec1d48-6214-a4a6-3e4f-8d3eb5c8f2cb.1467510663; __utma=1.1749497646.1467510663.1467510663.1467510663.1; __utmz=1.1467510663.1.1.utmcsr=sogou|utmccn=(organic)|utmcmd=organic|utmctr=%E5%A4%A7%E4%BC%97%E7%82%B9%E8%AF%84%E7%BD%91; PHOENIX_ID=0a0302bc-155d90b6be9-c8936; s_ViewType=10; JSESSIONID=7299F758AA33C769D888B5CF53E1A88C; aburl=1; cy=17; cye=xian'
    }
    data=None
    request=urllib2.Request(url,data,headers)#setrequest
    result = opener.open(request)
    html = result.read().decode('utf-8')
    return html

def getcitylist(html):
    time.sleep(1)
    getcitywareurl=re.compile(r'<a href="/[\s\S]*?</a>')
    cityurlware=getcitywareurl.findall(html)
    getcityurl=re.compile(r'href="/[\s\S]*?"')
    cityurl=getcityurl.findall(str(cityurlware))
    result=re.sub(r'href=|"|\s|\'',"",str(cityurl))
    result=result.split(',')
    number=len(result)
    cityurllist=[]
    for i in range(3,number-1):
        urlcity="https://www.dianping.com"+str(result[i])
        cityurllist.append(urlcity)
    return cityurllist

def getcategoryurllist(cityurl):
    time.sleep(0.5)
    cityhtml=gethtml(cityurl)
    getcategorylist=re.compile(r'<a data-key="\d+" href="[\s\S]*?">[\s\S]*?</a>')
    middleware=getcategorylist.findall(cityhtml)
    getcategoryhref=re.compile(r'href="[\s\S]*?"')
    resultware=getcategoryhref.findall(str(middleware))
    result=re.sub(r'href=|"|\'|\s|\[|\]',"",str(resultware))
    result=result.split(",")
    number=len(result)
    categoryurllist=[]
    for i in range(0,number):
        categoryurl="https://www.dianping.com"+str(result[i])
        categoryurllist.append(categoryurl)
    return categoryurllist

def getareaurllist(categoryurl):
    time.sleep(0.5)
    categoryhtml=gethtml(categoryurl)
    getareaurlware=re.compile(r'href="/search/category/\d+/\d+/g\d+r\d+')
    resultware=getareaurlware.findall(categoryhtml)

    result=re.sub(r'href=|\"|\'|\[|\]|\s|u|#nav-tab\|0\|1',"",str(resultware))
    result=result.split(",")
    number=len(result)
    areaurllist=[]
    for i in range(0,number):
        areaurl="https://www.dianping.com"+str(result[i])
        areaurllist.append(areaurl)
    return areaurllist

def getshopurllist(shopeachlisturl):
    shopurlhtml=gethtml(shopeachlisturl)
    getshopurl=re.compile(r'<a target="_blank" href="/shop/\d+"')
    resultware=getshopurl.findall(shopurlhtml)
    result=re.sub(r'<a target="_blank" href=|\"|\'|\[|\]|\s|u',"",str(resultware))
    result=result.split(",")
    number=len(result)
    shopurllist=[]
    for i in range(0,number):
        shopurl="https://www.dianping.com"+str(result[i])
        shopurllist.append(shopurl)
    return shopurllist

def getpagenumber(url):
     html=gethtml(url)
     getpagenumber=re.compile(r'title\="\d+">\d+</a>')
     pagenumberware=getpagenumber.findall(html)
     if pagenumberware==[]:
          return 1
     getpageinnernumber=re.compile(r'\d+')
     pagenumber=getpageinnernumber.findall(str(pagenumberware[-1]))
     pagenumber=int(pagenumber[1])
     return pagenumber


'''
rooturl="https://www.dianping.com/citylist/citylist?citypage=1"
roothtml=gethtml(rooturl)
cityurllist=getcitylist(roothtml)
for cityurl in cityurllist:
'''
cityurl = "https://www.dianping.com/xian"
categoryurllist=getcategoryurllist(cityurl)
outputFp = codecs.open("review_data_dianping719_0.txt", 'w', 'utf-8')
for categoryurl in categoryurllist:
    areaurllist=getareaurllist(categoryurl)
    for areaurl in areaurllist:
        shoplistpagenumber=getpagenumber(areaurl)#togetpagenumber
        for y in range(1,shoplistpagenumber+1):
            shopeachlisturl=areaurl+"p"+str(y)
            shopurllist=getshopurllist(shopeachlisturl)
            for shopurl in shopurllist:
                url=shopurl+"/review_all?pageno=1"#togetpagenumber
                print url
                pagenumber=getpagenumber(url)
                print url
                for x in range(1,pagenumber+1):
                    url=shopurl+"/review_all?pageno="+str(x)
                    try:
                        html=gethtml(url)
                    except Exception,e:
                        print Exception,":",e
                    getcontent=re.compile(r'<li id="rev_\d+" data-id="\d+">[\s\S]*?<div class="mode-tc respond Hide">')
                    result=getcontent.findall(html)
                    contentnumber=len(result)
                    for i in  range(0,contentnumber):
                        nameid=getnameid(result[i])
                        name=getname(result[i])
                        contribution=getcontribution(result[i])
                        userinforank=getuserinforank(result[i])
                        review=getreview(result[i])
                        timet=gettime(result[i])
                        shop=getshop(result[i])
                        cost=getcost(result[i])
                        rst1=getrst1(result[i])
                        rst2=getrst2(result[i])
                        rst3=getrst3(result[i])
                        print nameid
                        print name.decode('unicode_escape')
                        print contribution
                        print userinforank.decode('unicode_escape')
                        print review.decode('unicode_escape')
                        print timet
                        print shop.decode('unicode_escape')
                        print cost.decode('unicode_escape')
                        print rst1
                        print rst2
                        print rst3
                        outputFp.write("nameid: " + nameid + '\r\n' + "name: " + name.decode('unicode_escape') + '\r\n' + "contribution: " + contribution + '\r\n' + "userinforank: " + userinforank.decode('unicode_escape') + '\r\n' + "review: " + review.decode('unicode_escape') + '\r\n' + "time: " + timet +'\r\n' + "shop: " + shop.decode('unicode_escape') + '\r\n' + "cost: " + cost.decode('unicode_escape') + '\r\n' + "rst1: " + rst1 + '\r\n' +"rst2: " + rst2 + '\r\n' +"rst3: " + rst3 + '\r\n')
                        time.sleep(0.5)

                        '''
                        db=MySQLdb.connect(user='root',db='dianping',host='localhost' ,charset = 'utf8')
                        cursor=db.cursor()
                        sql = 'INSERT INTO `dianpingcontent`(`nameid`,`name`,`contribution`,`userinforank`,`review`,`time`,`shop`,`cost`,`rst1`,`rst2`,`rst3`)VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
                        val = (nameid,name,contribution,userinforank,review,time,shop,cost,rst1,rst2,rst3)
                        try:
                            cursor.execute(sql%val)
                            db.commit()
                        except:
                            db.rollback()
                        db.close()
                        '''

                    time.sleep(0.5)
                time.sleep(3)
            time.sleep(2)
        time.sleep(3)
    time.sleep(5)
time.sleep(10)
outputFp.flush()
outputFp.close()