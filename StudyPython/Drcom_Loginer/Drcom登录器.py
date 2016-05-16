#!/usr/bin/env python
#encoding:utf-8
import urllib
import urllib2

def post(url, data):
    data = urllib.urlencode(data)
    response = urllib2.urlopen(url, data)
    return response.read()

def main():
	Login_url = 'http://172.16.192.111'
	Post_data = {
		'DDDDD' : '2014131126',
	    'upass' : 'e6614f95a05e43d4a2b086060d8227ed123456781',
	    'R1' : '0',
	    'R2' : '1',
	    'para' : '00',
	    '0MKKey' : '123456',
	}
	print post(Login_url, Post_data)

if __name__ == '__main__':
	main()
