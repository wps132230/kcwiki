import json
import requests
import codecs

ind = 1
formation = [u'单纵', u'复纵', u'轮形', u'梯形', u'单横']

#response = requests.get(

# maplist = ['11', '12', '13', '14', '15', '16',
#            '21', '22', '23', '24', '25',
#            '31', '32', '33', '34', '35',
#            '41', '42', '43', '44', '45',
#            '51', '52', '53', '54', '55',
#            '61', '62', '63']
maplist = ['321','322','323','324','325']
##           '311','312','313','314','315', '316', '317']

# maplist = ['11', '12']
jsonStr = ''

jsonStr += 'local p = {}' + '\n'
jsonStr += 'function p.map(frame)' + '\n'
jsonStr += 'p.enemyDataTb = {' + '\n'

for mapid in maplist:
    response = requests.get('http://db.kcwiki.moe/wiki/enemy/' + mapid + '.json')
    if not response:
        print 'map' + mapid + 'does not exist!'
    else:
        print 'map' + mapid + 'is being generated!'
        #generator json file
        #jsonFile = open('jsonFile/jsonFile_'+mapid, 'w');
        #jsonFile.write(response.text.encode('utf-8'))
        #jsonFile.close()
        
        #generator lua file
        jsonStr += '\t' + '["' + mapid +'"] = {' + '\n'
        
        j = response.json()

        for point in j:
            jsonStr += '\t'*(ind+1) + '["' + point['point'] + '"] = {' + '\n'
            jsonStr += '\t'*(ind+2) + u'["类型"] = "普通战",' + '\n'
            jsonStr += '\t'*(ind+2) + u'["配置日文"] = "' + point['name'] + '",' + '\n'
            jsonStr += '\t'*(ind+2) + u'["配置中文"] = "' + point['name'] + '",' + '\n'
            jsonStr += '\t'*(ind+2) + u'["配置"] = {' + '\n'
            
            for levels in point['levels']:
                jsonStr += '\t'*(ind+3) + '["level' + str(levels['level']) + '"] = {' + '\n'
                fleetNum = 1
                for fleet in levels['fleets']:
                    jsonStr += '\t'*(ind+4) + '["' + str(fleetNum) + '"] = {' + '\n'
                    fleetNum += 1
                    jsonStr += '\t'*(ind+5) + u'["制空"] = ' + '0' + ',' + '\n'
                    jsonStr += '\t'*(ind+5) + u'["阵型"] = "' + formation[fleet['formation']-1] + '",' + '\n'
                    jsonStr += '\t'*(ind+5) + u'["详细"] = ' + str(fleet['ships']).replace('[','{').replace(']','}') + ',' + '\n'
                    jsonStr += '\t'*(ind+5) + u'["hqLvRange"] = ' + '{' + str(fleet['hqLvRange'][0]) + ', '\
                                                                + str(fleet['hqLvRange'][1]) + '},' + '\n'
                    jsonStr += '\t'*(ind+4) + '},' + '\n'
                
                jsonStr += '\t'*(ind+3) + '},' + '\n'
            jsonStr += '\t'*(ind+2) + '},' + '\n'
            jsonStr += '\t'*(ind+1) + '},' + '\n'*2
        jsonStr += '\t' + '},' + '\n'*2

jsonStr += '}' + '\n'
jsonStr += '\t' + 'return p.enemyDataTb[frame.args[1]][frame.args[2]][frame.args[3]]' + '\n'
jsonStr += 'end' + '\n'
jsonStr += 'return p' + '\n'

luaFile = codecs.open('luaFile/luaFile', 'w', 'utf-8')
luaFile.write(jsonStr)
luaFile.close()

##http://zh.kcwiki.moe/wiki/%E6%A8%A1%E5%9D%97:%E6%B5%B7%E5%9B%BE%E9%85%8D%E7%BD%AE%E6%95%B0%E6%8D%AE/2-3
#http://poi.gizeta.me/wiki/enemy/11.json
#http://zh.kcwiki.moe/api.php?action=query&generator=allpages&gapprefix=L
