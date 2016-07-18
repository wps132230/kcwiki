# -*- coding: utf-8 -*-
import json
import requests
import codecs

dict2015 = {}
dict2016 = {}

list2015 = [{} for i in range(23)]
list2016 = [{} for i in range(23)]

shipTypeMap = {1:u'海防艦', 2:u'駆逐艦', 3:u'軽巡洋艦', 4:u'重雷装巡洋艦', 5:u'重巡洋艦', \
6:u'航空巡洋艦', 7:u'軽空母', 8:u'巡洋戦艦', 9:u'戦艦', 10:u'航空戦艦', 11:u'正規空母', \
12:u'超弩級戦艦', 13:u'潜水艦', 14:u'潜水空母', 15:u'補給艦(敵のほう)', 16:u'水上機母艦', \
17:u'揚陸艦', 18:u'装甲空母', 19:u'工作艦', 20:u'潜水母艦', 21:u'練習巡洋艦', 22:u'補給艦'}

with open('voiceNeedUpdate.json') as fp:
    voiceNeedUpdate = json.load(fp)
with open('wikiFileNameDict.json') as fp:
    wikiFileNameDict = json.load(fp)
with open('Shoka2016.log') as fp:
    # with open('Shoka2016.log') as fp:
    line = fp.readline()
    while not(line == ""):
        shipWikiId = line.split()[2].split("-")[0]
        if line.split()[4] == 'Success':
            dict2016[shipWikiId] = None
        if line.split()[4] == 'Failed':
            line = fp.readline()
            if 'Shoka' in line.split()[9]:
                dict2015[shipWikiId] = None
        line = fp.readline()

# print dict2016, len(dict2016)
# print dict2015, len(dict2015)

response = requests.get('http://kcwikizh.github.io/kcdata/ship/all.json')
j = response.json()

def codeGen(wiki_id, name, fileName):
    rname = ''
    rname = rname + u'{{台词翻译表|type=seasonal' + '\n'
    rname = rname + u' | 档名 = ' + fileName + '\n'
    rname = rname + u' | 编号 = ' + wiki_id + '\n'
    rname = rname + u' | 舰娘名字 = ' + name + '\n'
    rname = rname + u' | 日文台词 = ' + '\n'
    rname = rname + u' | 中文译文 = ' + '\n'
    rname = rname + '}}' + '\n'
    return rname

for ship in j:
    shipId = str(ship['id'])
    if shipId in voiceNeedUpdate:
        if voiceNeedUpdate[shipId]['2'] == None:
            continue
        if ship['wiki_id'] in dict2015:
            list2015[ship['stype']][ship['wiki_id']] = \
            [shipId, ship['chinese_name'],wikiFileNameDict[str(voiceNeedUpdate[shipId]['2'])].replace('2016', '')[:-4]]
        if ship['wiki_id'] in dict2016:
            list2016[ship['stype']][ship['wiki_id']] = \
            [shipId, ship['chinese_name'],wikiFileNameDict[str(voiceNeedUpdate[shipId]['2'])][:-4]]

shipId2015Str = ''
for stype in range(len(list2015)):
    shipDict = list2015[stype]
    if not shipDict:
        continue
    shipId2015Str = shipId2015Str + '===' + shipTypeMap[stype] + '===' + '\n'
    shipList = sorted(shipDict.iteritems(), key=lambda d:d[0])
    for ship in shipList:
        shipId2015Str = shipId2015Str + codeGen(ship[0], ship[1][1], ship[1][2])

shipId2016Str = ''
for stype in range(len(list2016)):
    shipDict = list2016[stype]
    if not shipDict:
        continue
    shipId2016Str = shipId2016Str + '===' + shipTypeMap[stype] + '===' + '\n'
    shipList = sorted(shipDict.iteritems(), key=lambda d:d[0])
    for ship in shipList:
        shipId2016Str = shipId2016Str + codeGen(ship[0], ship[1][1], ship[1][2])

shipId2015StrFile = codecs.open('wikicode_Shoka2015', 'w', 'utf-8')
shipId2015StrFile.write(shipId2015Str)
shipId2015StrFile.close()

shipId2016StrFile = codecs.open('wikicode_Shoka2016', 'w', 'utf-8')
shipId2016StrFile.write(shipId2016Str)
shipId2016StrFile.close()
