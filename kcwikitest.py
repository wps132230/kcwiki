from requests import (post,ConnectionError,HTTPError,
	Timeout,TooManyRedirects)
from functools import wraps
#import logging
#import sys
#import time
import json

rdata = {'action':'login','format':'json'}
rdata['lgname'] = 'wps132230'
rdata['lgpassword'] = '10a260b5'

response = post('http://zh.kcwiki.moe/api.php?action=help&modules=login', rdata)
lgtoken = response.json()['login']['token']
cookies = response.cookies.get_dict()

rdata['lgtoken'] = lgtoken
response = post('http://zh.kcwiki.moe/api.php?action=help&modules=login', rdata, cookies = cookies)

print 'login reponse:\n' + response.text + '\n'

##-------------------------------------------------------------------------------

rdata = {'action':'query', 'meta':'tokens', 'format':'json'}
response = post('http://zh.kcwiki.moe/wiki/module:LUATEST', rdata)

#http://zh.kcwiki.moe/api.php
#http://zh.kcwiki.moe/api.php?action=help&modules=login
