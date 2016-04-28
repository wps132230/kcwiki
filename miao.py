import json
import requests

ind = 0

#response = requests.get(

#maplist = ['11', '12', '13', '14', '15', '16',
#           '21', '22', '23', '24', '25',
#           '31', '32', '33', '34', '35',
#           '41', '42', '43', '44', '45',
#           '51', '52', '53', '54', '55',
#           '61', '62', '63',
#           '311','312','313','314','315', '316', '317']

maplist = ['11','12']

for mapid in maplist:
    response = requests.get('http://db.kcwiki.moe/wiki/enemy/' + mapid + '.json')
    if not response:
        print 'map' + mapid + 'does not exist!'
    else:
        #generator json file
        #jsonFile = open('jsonFile/jsonFile_'+mapid, 'w');
        #jsonFile.write(response.text.encode('utf-8'))
        #jsonFile.close()
        
        #generator lua file
        #luaFile = open('luaFile/luaFile_'+mapid, 'w')
        j = response.json()
        jsonStr = ''
        for point in j:
            jsonStr += '\t'*(ind+1) + '["' + point['point'] + '"] = {' + '\n'
            jsonStr += '\t'*(ind+2) + u'["类型"] = "普通战",' + '\n'
            jsonStr += '\t'*(ind+2) + u'["配置日文"] = "' + point['name'] + '"' + '\n'
            print jsonStr
        #luaFile = open('luaFile/luaFile_'+mapid, 'w')
        #luaFile.write(jsonStr)
        #luaFile.close()

#http://poi.gizeta.me/wiki/enemy/11.json
#http://zh.kcwiki.moe/api.php?action=query&generator=allpages&gapprefix=L
