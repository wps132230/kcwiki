import json
import copy
from requests import (post,get,ConnectionError,HTTPError,Timeout,TooManyRedirects)
from functools import wraps
#import logging
#import sys
#import time
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0',\
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3', \
'Accept-Encoding': 'gzip, deflate', \
'Connection': 'keep-alive'}

rdata = {'action':'login','format':'json'}
rdata['lgname'] = 'wps132230'
rdata['lgpassword'] = '10a260b5'

response = post('http://zh.kcwiki.moe/api.php?action=help&modules=login', \
rdata, headers = headers)
lgtoken = response.json()['login']['token']
cookies = response.cookies.get_dict()

rdata['lgtoken'] = lgtoken
response = post('http://zh.kcwiki.moe/api.php?action=help&modules=login', \
rdata, cookies = cookies, headers = headers)
# print 'login reponse:\n' + response.text + '\n'

# edit token
rdata = {'action': 'query', 'meta': 'tokens', 'format': 'json'}
rep = post('http://zh.kcwiki.moe/api.php?action=help&modules=login', \
rdata, cookies = cookies, headers = headers)
token = rep.json()['query']['tokens']['csrftoken']

##-------------------------------------------------------------------------------

response = get('http://kcwikizh.github.io/kcdata/ship/all.json')
j = response.json()

start = False
for ship in j:
    if not start:
        if ship['id'] == 2:
            start = True
        continue
    if ship['id'] > 500:
        continue
    wiki_id = ship['wiki_id']
    if wiki_id == None:
        continue
    rdata = {'action': 'move', 'token': token, 'format': 'json', 'from':'File:'+wiki_id+'-Tsuyu2015.mp3', 'to':'File:'+wiki_id+'-Sec1Tsuyu2015.mp3'}

    rep = post('http://zh.kcwiki.moe/api.php', rdata, cookies = cookies, headers = headers)
    print rep.json()

for ship in j:
    if ship['id'] > 500:
        continue
    wiki_id = ship['wiki_id']
    if wiki_id == None:
        continue
    rdata = {'action': 'move', 'token': token, 'format': 'json', 'from':'File:'+wiki_id+'-Tsuyu2016.mp3', 'to':'File:'+wiki_id+'-Sec1Tsuyu2016.mp3'}

    rep = post('http://zh.kcwiki.moe/api.php', rdata, cookies = cookies, headers = headers)
    print rep.json()

#http://zh.kcwiki.moe/api.php
#http://zh.kcwiki.moe/api.php?action=help&modules=login
