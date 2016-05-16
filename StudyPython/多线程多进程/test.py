#!/usr/bin/python
# coding=utf-8

from multiprocessing.dummy import Pool
import requests
import urllib
import time
import os

def get_source(url):
    print "we crawled:%s" % url
    html=urllib.urlopen(url)
    print html.geturl()
    print os.getpid()

urls=[]

for i in range(1,21):
    new_page="http://tieba.baidu.com/p/3522395718?pn="+str(i)
    urls.append(new_page)

time1=time.time()

for url in urls:

    get_source(url)

time2=time.time()
print "it take:",(time2-time1)

pool=Pool(4)
time3=time.time()
res=pool.map(get_source,urls)
pool.close()
pool.join()
time4=time.time()
print "now,it take,",(time4-time3)