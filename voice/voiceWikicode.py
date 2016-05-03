# -*- coding: utf-8 -*-
import json
import requests
import codecs

chineseName = {}

shipTypeMap = {1:u'海防艦', 2:u'駆逐艦', 3:u'軽巡洋艦', 4:u'重雷装巡洋艦', 5:u'重巡洋艦', \
6:u'航空巡洋艦', 7:u'軽空母', 8:u'巡洋戦艦', 9:u'戦艦', 10:u'航空戦艦', 11:u'正規空母', \
12:u'超弩級戦艦', 13:u'潜水艦', 14:u'潜水空母', 15:u'補給艦(敵のほう)', 16:u'水上機母艦', \
17:u'揚陸艦', 18:u'装甲空母', 19:u'工作艦', 20:u'潜水母艦', 21:u'練習巡洋艦', 22:u'補給艦'}

voiceId2NameZh = {1:u'入手/登入时', 2:u'秘书舰1', 3:u'秘书舰2', 4:u'秘书舰3', 5:u'建造完成', 6:u'修复完成', 7:u'归来', 8:u'战绩', 9:u'装备/改修/改造1', 10:u'装备/改修/改造2', 11:u'小破入渠', 12:u'中破入渠', 13:u'编成', 14:u'出征', 15:u'战斗开始', 16:u'攻击1', 17:u'攻击2', 18:u'夜战', 19:u'小破1', 20:u'小破2', 21:u'中破', 22:u'击沉', 23:u'MVP', 24:u'结婚', 25:u'图鉴介绍', 26:u'装备', 27:u'补给', 28:u'秘书舰（婚后）', 29:u'放置', 30:u'〇〇〇〇时报', 31:u'〇一〇〇时报', 32:u'〇二〇〇时报', 33:u'〇三〇〇时报', 34:u'〇四〇〇时报', 35:u'〇五〇〇时报', 36:u'〇六〇〇时报', 37:u'〇七〇〇时报', 38:u'〇八〇〇时报', 39:u'〇九〇〇时报', 40:u'一〇〇〇时报', 41:u'一一〇〇时报', 42:u'一二〇〇时报', 43:u'一三〇〇时报', 44:u'一四〇〇时报', 45:u'一五〇〇时报', 46:u'一六〇〇时报', 47:u'一七〇〇时报', 48:u'一八〇〇时报', 49:u'一九〇〇时报', 50:u'二〇〇〇时报', 51:u'二一〇〇时报', 52:u'二二〇〇时报', 53:u'二三〇〇时报'}

with open('voiceNeedUpdate.json') as fp:
    voiceNeedUpdate = json.load(fp)
with open('wikiFileNameDict.json') as fp:
    wikiFileNameDict = json.load(fp)

response = requests.get('http://kcwikizh.github.io/kcdata/ship/all.json')
j = response.json()

def codeGen(fileName, occasion):
    rname = ''
    rname = rname + u'{{台词翻译表' + '\n'
    rname = rname + u' | 档名 = ' + fileName[:-4] + '\n'
    rname = rname + u' | 场合 = ' + occasion + '\n'
    rname = rname + u' | 日文台词 = ' + '\n'
    rname = rname + u' | 中文译文 = ' + '\n'
    rname = rname + '}}' + '\n'
    return rname

for ship in j:
    shipId = str(ship['id'])
    if shipId in voiceNeedUpdate:
        if voiceNeedUpdate[shipId][0] == None:
            continue
        chineseName[shipId] = ship['chinese_name']

# print list2ndAnniv, len(list2ndAnniv)
# print list3rdAnniv, len(list3rdAnniv)

for shipId in voiceNeedUpdate:
    wikiCode = '===' + chineseName[shipId] + '===\n'
    wikiCode = wikiCode + u'{{台词翻译表/页头}}\n'
    for i in range(len(voiceNeedUpdate[shipId])):
        if voiceNeedUpdate[shipId][i] != None:
            fileName = wikiFileNameDict[str(voiceNeedUpdate[shipId][i])]
            occasion = voiceId2NameZh[i+30]
            wikiCode = wikiCode + codeGen(fileName, occasion)
    wikiCode = wikiCode + u'{{页尾}}\n'

    wikiCodeFile = codecs.open('wikiCode_alarm_' + shipId, 'w', 'utf-8')
    wikiCodeFile.write(wikiCode)
    wikiCodeFile.close()
