#!/usr/bin/python
# coding=utf-8

import urllib

url = 'https://www.baidu.com/img/bd_logo1.png'
path = 'baidu.png'

urllib.urlretrieve(url, path)