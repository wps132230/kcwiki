from requests import post
from functools import wraps
#import logging
#import sys
#import time
import json
host = 'http://zh.kcwiki.moe/api.php'
ua = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36(KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'}
rdata = {'action':'login','format':'json'}
rdata['lgname'] = 'grzhan'
rdata['lgpassword'] = 'shenyanghua'

##response = post('http://zh.kcwiki.moe/api.php?action=help&modules=login', rdata)
print host
print rdata
print ua
print
print '-----------------------------------------------'
print
response = post(host, rdata, headers = ua)
print 'login token response' + response.text + '\n'
lgtoken = response.json()['login']['token']
cookies = response.cookies.get_dict()

rdata['lgtoken'] = lgtoken
##response = post('http://zh.kcwiki.moe/api.php?action=help&modules=login', rdata, cookies = cookies)
print host
print rdata
print cookies
print ua
print
print '-----------------------------------------------'
print
response = post(host, rdata, cookies = cookies, headers = ua)

print 'login reponse:\n' + response.text + '\n'
cookies.update(response.cookies.get_dict())

##-------------------------------------------------------------------------------

rdata = {'action':'query', 'meta':'tokens', 'format':'json'}
print host
print rdata
print cookies
print ua
print
print '-----------------------------------------------'
print
response = post(host, rdata, cookies = cookies, headers = ua)

print 'edit_token response:\n' + response.text + '\n'
token = response.json()['query']['tokens']['csrftoken']

text = 'lua test'
rdata = {'title':'Module:Sandbox', 'action':'edit', 'token':token, 'bot':1,\
         'text':text, 'format':'json', 'summary': 'test'}
headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}

headers.update(ua)
print host
print rdata
print cookies
print headers
print
print '-----------------------------------------------'
print
response = post(host, rdata, cookies = cookies, headers = headers)
print 'edit response:\n' + response.text + '\n'

#http://zh.kcwiki.moe/api.php
#http://zh.kcwiki.moe/api.php?action=help&modules=login
