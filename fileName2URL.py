import json
import requests
import md5

fileName = 'Bglm2.png'
##response = requests.get('http://zh.kcwiki.moe/wiki/File:' + fileName)
####j = response.json()
##string = response.text
##ind = string.find('/'+fileName+'"')
##subString = string[ind-50 : ind+len(fileName)+1]
##ind = subString.find('http')
##url = subString[ind : ]
##print url

m1 = md5.new()
m1.update(fileName)
char = m1.hexdigest()
url = 'http://kcwiki.ikk.me/commons/' + char[0] + '/' + \
      char[0:2] + '/' + fileName
print url
