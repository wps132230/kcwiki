import json
import requests
import codecs
import hashlib
import copy

directory = 'voice_Tsuyu2016/'

with open('shipVoiceIdDict.json') as fp:
    shipVoiceIdDict = json.load(fp)
with open('wikiFileNameDict.json') as fp:
    wikiFileNameDict = json.load(fp)

voiceNeedUpdate = copy.deepcopy(shipVoiceIdDict)
response = requests.get('http://kcwikizh.github.io/kcdata/ship/all.json')
j = response.json()

for ship in j:
    shipId = str(ship['id'])
    if shipId in shipVoiceIdDict:
        for voiceId in shipVoiceIdDict[shipId]:
            # print shipId, ship['after_ship_id']
            if ship['after_ship_id'] != None:
                nextShipId = str(ship['after_ship_id'])
                if nextShipId in shipVoiceIdDict:
                    nextShipFileName = wikiFileNameDict[str(shipVoiceIdDict[nextShipId][voiceId])]
                    shipFileName = wikiFileNameDict[str(shipVoiceIdDict[shipId][voiceId])]
                    # print shipFileName, nextShipFileName
                    if hashlib.md5(open(directory + shipFileName, 'rb').read()).hexdigest() \
                    == hashlib.md5(open(directory + nextShipFileName, 'rb').read()).hexdigest():
                        voiceNeedUpdate[nextShipId][voiceId] = None
# print voiceNeedUpdate
with open('voiceNeedUpdate.json', 'w') as fp:
    json.dump(voiceNeedUpdate, fp)
