import json
#
# dic = {}
# f = open('miao', 'w')
# f2 = open('shiptype', 'r')
# for line in f2:
#     first = line.split()[0]
#     second = first.split('=')
#     dic[int(second[0])] = second[1].encode('utf-8')
#
# # with open('shipTypeMap.json', 'w') as fp:
# #     json.dump(dic, fp)
# print dic

with open('wikiFileNameDict.json', 'r') as fp:
    wikiFileNameDict = json.load(fp)
#
# with open('wikiFileName.json', 'w') as fp:
#     for shipVoiceId in wikiFileNameDict:
#         wikiFileNameDict[shipVoiceId] = wikiFileNameDict[shipVoiceId][16:]
#     json.dump(wikiFileNameDict, fp)

num = 0
with open('voiceNeedUpdate.json', 'r') as fp:
    voiceNeedUpdate = json.load(fp)
    for key in voiceNeedUpdate:
        if voiceNeedUpdate[key]['2'] != None:
            print wikiFileNameDict[str(voiceNeedUpdate[key]['2'])]
            num = num + 1
print num