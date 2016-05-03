import json
import requests
import codecs

dicId = {360,361,362,363,476}

logFile = open('voice.log', 'w')
# with open('shipVoiceIdDict.json') as fp:
#     shipVoiceIdDict = json.load(fp)
# with open('wikiFileNameDict.json') as fp:
#     wikiFileNameDict = json.load(fp)
shipVoiceIdDict = {}
wikiFileNameDict = {}

voiceId2Name = {1:'Intro', 2:'Sec1', 3:'Sec2', 4:'Sec3',\
5:'ConstComplete', 6:'DockComplete', 7:'Return', 8:'Achievement', \
9:'Equip1', 10:'Equip2', 11:'DockLightDmg', 12:'DockMedDmg', \
13:'FleetOrg', 14:'Sortie', 15:'Battle', 16:'Atk1', 17:'Atk2', \
18:'NightBattle', 19:'LightDmg1', 20:'LightDmg2', 21:'MedDmg', 22:'Sunk', \
23:'MVP', 24: 'Proposal', 25:'LibIntro', 26:'Equip3', 27:'Resupply', \
28:'SecWed', 29:'Idle', 30:'0000', 31:'0100', 32:'0200', 33:'0300', \
34:'0400', 35:'0500', 36:'0600', 37:'0700', 38:'0800', 39:'0900', \
40:'1000', 41:'1100', 42:'1200', 43:'1300', 44:'1400', 45:'1500', \
46:'1600', 47:'1700', 48:'1800', 49:'1900', 50:'2000', 51:'2100', \
52:'2200', 53:'2300'}

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0',\
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3', \
'Accept-Encoding': 'gzip, deflate', \
'Connection': 'keep-alive'}

# vcKey is extracted from Core.swf/common.util.SoundUtil
vcKey = [604825,607300,613847,615318,624009,631856,635451,637218,640529,643036,\
652687,658008,662481,669598,675545,685034,687703,696444,702593,703894,711191,\
714166,720579,728970,738675,740918,743009,747240,750347,759846,764051,770064,\
773457,779858,786843,790526,799973,803260,808441,816028,825381,827516,832463,\
837868,843091,852548,858315,867580,875771,879698,882759,885564,888837,896168]
# prefix = "http://voice.kcwiki.moe/kcs/sound/"
prefix = "http://125.6.187.229/kcs/sound/"
date = ['2', 'May']

def getAllJson():
    response = requests.get('http://kcwikizh.github.io/kcdata/ship/all.json')
    return response.json()

def getVoiceFileName(shipId, voiceId, fileName):
    id = (shipId + 7) * 17 * (vcKey[voiceId] - vcKey[voiceId - 1]) % 99173 + 100000
    return prefix + 'kc' + fileName + '/' + str(id) + '.mp3', id

def getFileName(j, shipId):
    for ship in j:
        if ship['id'] == shipId:
            return ship['filename']

def isUpdate(modifiedDate):
    if modifiedDate.split()[1] == date[0] \
    and (modifiedDate.split()[2] == "1"
    or modifiedDate.split()[2] == "2"):
        return True
    else:
        return False

# ------------------------------------------------------------------------------

j = getAllJson()
num = 0
for ship in j:
    # if num == 2:
        # break
    shipId = int(ship['id'])
    if shipId not in dicId:
        continue
    fileName = ship['filename']

    print str(num) + '\t' + str(shipId) + ' : ',
    logFile.write(str(shipId) + " : ")
    for voiceId in range(30, 54):
        voiceFileName, shipVoiceId = getVoiceFileName(shipId, voiceId, fileName)
        response = requests.get(voiceFileName, headers)
        # print voiceFileName
        # if response and isUpdate(response.headers['Last-Modified']):
        if response:
            wikiFileName = ship['wiki_id'] + '-' + voiceId2Name[voiceId] +'.mp3'
            data = response.content
            # with open(wikiFileName, 'wb') as f:
            #     f.write(data)

            print voiceId, 'y',
            # update log file
            logFile.write(str(voiceId) + ', ')
            if shipId not in shipVoiceIdDict:
                shipVoiceIdDict[shipId] = [shipVoiceId]
            else:
                shipVoiceIdDict[shipId].append(shipVoiceId)
            wikiFileNameDict[shipVoiceId] = wikiFileName
        else:
            print voiceId, 'x',
        with open('shipVoiceIdDict.json', 'w') as fp:
            json.dump(shipVoiceIdDict, fp)
        with open('wikiFileNameDict.json', 'w') as fp:
            json.dump(wikiFileNameDict, fp)
    print
    logFile.write('\n')
    num = num + 1

# print shipVoiceIdDict
# print wikiFileNameDict
