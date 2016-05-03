# -*- coding: utf-8 -*-
import json
import requests
import codecs

ignore_shipId = {127:None}

dict2ndAnniv = {}

list2ndAnniv = [{} for i in range(23)]
list3rdAnniv = [{} for i in range(23)]

shipTypeMap = {1:u'海防艦', 2:u'駆逐艦', 3:u'軽巡洋艦', 4:u'重雷装巡洋艦', 5:u'重巡洋艦', \
6:u'航空巡洋艦', 7:u'軽空母', 8:u'巡洋戦艦', 9:u'戦艦', 10:u'航空戦艦', 11:u'正規空母', \
12:u'超弩級戦艦', 13:u'潜水艦', 14:u'潜水空母', 15:u'補給艦(敵のほう)', 16:u'水上機母艦', \
17:u'揚陸艦', 18:u'装甲空母', 19:u'工作艦', 20:u'潜水母艦', 21:u'練習巡洋艦', 22:u'補給艦'}

with open('voiceNeedUpdate.json') as fp:
    voiceNeedUpdate = json.load(fp)
with open('wikiFileNameDict.json') as fp:
    wikiFileNameDict = json.load(fp)
with open('2ndAnniv.log') as fp:
    for line in fp:
        shipId2ndAnniv = line.split()[0]
        dict2ndAnniv[shipId2ndAnniv] = None

response = requests.get('http://kcwikizh.github.io/kcdata/ship/all.json')
j = response.json()

def codeGen(wiki_id, name, fileName):
    rname = ''
    rname = rname + u'{{台词翻译表|type=seasonal' + '\n'
    rname = rname + u' | 档名 ＝ ' + fileName + '\n'
    rname = rname + u' | 编号 ＝ ' + wiki_id + '\n'
    rname = rname + u' | 舰娘名字 ＝ ' + name + '\n'
    rname = rname + u' | 日文台词 ＝ ' + '\n'
    rname = rname + u' | 中文台词 ＝ ' + '\n'
    rname = rname + '}}' + '\n'
    return rname

for ship in j:
    shipId = str(ship['id'])
    if shipId in voiceNeedUpdate:
        if voiceNeedUpdate[shipId][0] == None:
            continue
        if shipId in dict2ndAnniv:
            list2ndAnniv[ship['stype']][ship['wiki_id']] = \
            [shipId, ship['chinese_name'],wikiFileNameDict[str(voiceNeedUpdate[shipId][0])].replace('Sec13nd', '2nd')[:-4]]
        else:
            list3rdAnniv[ship['stype']][ship['wiki_id']] = \
            [shipId, ship['chinese_name'],wikiFileNameDict[str(voiceNeedUpdate[shipId][0])][:-4]]

# print list2ndAnniv, len(list2ndAnniv)
# print list3rdAnniv, len(list3rdAnniv)

shipId2ndAnnivStr = ''
for stype in range(len(list2ndAnniv)):
    shipDict = list2ndAnniv[stype]
    if not shipDict:
        continue
    shipId2ndAnnivStr = shipId2ndAnnivStr + '==' + shipTypeMap[stype] + '==' + '\n'
    shipList = sorted(shipDict.iteritems(), key=lambda d:d[0])
    for ship in shipList:
        shipId2ndAnnivStr = shipId2ndAnnivStr + codeGen(ship[0], ship[1][1], ship[1][2])

shipId3rdAnnivStr = ''
for stype in range(len(list3rdAnniv)):
    shipDict = list3rdAnniv[stype]
    if not shipDict:
        continue
    shipId3rdAnnivStr = shipId3rdAnnivStr + '==' + shipTypeMap[stype] + '==' + '\n'
    shipList = sorted(shipDict.iteritems(), key=lambda d:d[0])
    for ship in shipList:
        shipId3rdAnnivStr = shipId3rdAnnivStr + codeGen(ship[0], ship[1][1], ship[1][2])

shipId2ndAnnivStrFile = codecs.open('wikicode_2nd', 'w', 'utf-8')
shipId2ndAnnivStrFile.write(shipId2ndAnnivStr)
shipId2ndAnnivStrFile.close()

shipId3rdAnnivStrFile = codecs.open('wikicode_3rd', 'w', 'utf-8')
shipId3rdAnnivStrFile.write(shipId3rdAnnivStr)
shipId3rdAnnivStrFile.close()
