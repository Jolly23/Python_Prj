#!/usr/bin/env python
# coding: utf-8
#copyRight by Jolly

import urllib
import os
import re

def downloadURL(url):
    if len(url)>0:
        print "current process id is ",os.getpid()
        content1 = urllib.urlopen(url)
        content = content1.read()
        open(r'yst/'+url[-26:],'a+').write(content)
        print 'downloaded',url

def parseTarget(url):
    urls=[]
    con=urllib.urlopen(url).read()
    pattern = r'<a title=(.*?) href="(.*?)">'
    hrefs = re.findall(pattern,con)

    for href in hrefs:
        urls.append(href[1])

    return urls

if __name__=="__main__":
    import multiprocessing as multi

    urls=[]
    i = 0
    while i < 5:
        #原生态的博客
        #http_url='http://blog.sina.com.cn/s/articlelist_1368179347_0_'+str(i+1)+'.html'
        #韩寒的博客
        http_url='http://blog.sina.com.cn/s/articlelist_1191258123_0_'+str(i+1)+'.html'
        try:
            urls.extend(parseTarget(http_url))
            print "have parse "+str(i)+" pages"
            i += 1
        except:
            print "error, have parse "+str(i)+" pages"
            break

    #创建进程池
    pool_num = 8
    pool = multi.Pool(pool_num)
    pool.map(downloadURL, urls)