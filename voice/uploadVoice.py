import json
import copy
from requests import (post,ConnectionError,HTTPError,
	Timeout,TooManyRedirects)
from functools import wraps
#import logging
#import sys
#import time
import json

# logFile = open('2ndAnniv.log', 'w')

# with open('voiceNeedUpdate.json') as fp:
#     voiceNeedUpdate = json.load(fp)
# with open('wikiFileNameDict.json') as fp:
#     wikiFileNameDict = json.load(fp)

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

# num = 0
# for shipId in voiceNeedUpdate:
#     for i in range(len(voiceNeedUpdate[shipId])):
#         if voiceNeedUpdate[shipId][i] == None:
#             continue
#         shipVoiceId = str(voiceNeedUpdate[shipId][i])
#         filename = wikiFileNameDict[shipVoiceId]
#         num = num + 1
#         if num < 144:
#             continue
#         rdata = {'action': 'upload', 'token': token, 'format': 'json', 'filename': filename}
#         files = {'file': open(filename, 'rb')}
#
#         rep = post('http://zh.kcwiki.moe/api.php', \
#         rdata, cookies = cookies, headers = headers, files = files)
#         # print rep.json()
#         result = rep.json()['upload']['result'].encode('utf-8')
#         if result == 'Success':
#             print str(num) + ':' + filename + ':' + 'Success'
#         else:
#             print rep.json()
#             print str(num) + ':' + filename + ':' + 'Failed'
#             logFile.write(str(shipId) + ' ' + filename + '\n')

num = 0
fp = open('shipId269', 'r')
for line in fp:
    filename = line[:-1]
    num = num + 1
    print filename
    rdata = {'action': 'upload', 'token': token, 'format': 'json', 'filename': filename}
    files = {'file': open(filename, 'rb')}

    rep = post('http://zh.kcwiki.moe/api.php', \
    rdata, cookies = cookies, headers = headers, files = files)
    # print rep.json()
    result = rep.json()['upload']['result'].encode('utf-8')
    if result == 'Success':
        print str(num) + ':' + filename + ':' + 'Success'
    else:
        print rep.json()
        print str(num) + ':' + filename + ':' + 'Failed'

#http://zh.kcwiki.moe/api.php
#http://zh.kcwiki.moe/api.php?action=help&modules=login
