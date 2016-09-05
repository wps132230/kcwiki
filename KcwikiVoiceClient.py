# -*- coding: utf-8 -*-
import KcwikiClient as KC
import json
import requests
import codecs
import hashlib
import os
import shutil

class KcwikiVoiceClient(KC.KcwikiClient):
    def __init__(self):
        KC.KcwikiClient.__init__(self)
        self.voiceCacheUrlprefix = "http://125.6.187.229/kcs/sound/"
        self.vcKey = [604825,607300,613847,615318,624009,631856,635451,637218,640529,643036,652687,
                      658008,662481,669598,675545,685034,687703,696444,702593,703894,711191,714166,
                      720579,728970,738675,740918,743009,747240,750347,759846,764051,770064,773457,
                      779858,786843,790526,799973,803260,808441,816028,825381,827516,832463,837868,
                      843091,852548,858315,867580,875771,879698,882759,885564,888837,896168]

        self.voiceId2Name = {1 :'Intro',         2 :'Sec1',          3 :'Sec2',          4 :'Sec3',
                             5 :'ConstComplete', 6 :'DockComplete',  7 :'Return',        8 :'Achievement',
                             9 :'Equip1',        10:'Equip2',        11:'DockLightDmg',  12:'DockMedDmg',
                             13:'FleetOrg',      14:'Sortie',        15:'Battle',        16:'Atk1',
                             17:'Atk2',          18:'NightBattle',   19:'LightDmg1',     20:'LightDmg2',
                             21:'MedDmg',        22:'Sunk',          23:'MVP',           24: 'Proposal',
                             25:'LibIntro',      26:'Equip3',        27:'Resupply',      28:'SecWed',
                             29:'Idle',
                             30:'0000', 31:'0100', 32:'0200', 33:'0300', 34:'0400', 35:'0500',
                             36:'0600', 37:'0700', 38:'0800', 39:'0900', 40:'1000', 41:'1100',
                             42:'1200', 43:'1300', 44:'1400', 45:'1500', 46:'1600', 47:'1700',
                             48:'1800', 49:'1900', 50:'2000', 51:'2100', 52:'2200', 53:'2300'}

        self.voiceId2NameZh = {1:u'入手/登入时', 2:u'秘书舰1', 3:u'秘书舰2', 4:u'秘书舰3', 5:u'建造完成',6:u'修复完成',
                               7:u'归来', 8:u'战绩', 9:u'装备/改修/改造1', 10:u'装备/改修/改造2', 11:u'小破入渠',
                               12:u'中破入渠', 13:u'编成', 14:u'出征', 15:u'战斗开始', 16:u'攻击1', 17:u'攻击2',
                               18:u'夜战', 19:u'小破1', 20:u'小破2', 21:u'中破', 22:u'击沉', 23:u'MVP', 24:u'结婚',
                               25:u'图鉴介绍', 26:u'装备', 27:u'补给', 28:u'秘书舰（婚后）', 29:u'放置',
                               30:u'〇〇〇〇时报', 31:u'〇一〇〇时报', 32:u'〇二〇〇时报', 33:u'〇三〇〇时报',
                               34:u'〇四〇〇时报', 35:u'〇五〇〇时报', 36:u'〇六〇〇时报', 37:u'〇七〇〇时报',
                               38:u'〇八〇〇时报', 39:u'〇九〇〇时报', 40:u'一〇〇〇时报', 41:u'一一〇〇时报',
                               42:u'一二〇〇时报', 43:u'一三〇〇时报', 44:u'一四〇〇时报', 45:u'一五〇〇时报',
                               46:u'一六〇〇时报', 47:u'一七〇〇时报', 48:u'一八〇〇时报', 49:u'一九〇〇时报',
                               50:u'二〇〇〇时报', 51:u'二一〇〇时报', 52:u'二二〇〇时报', 53:u'二三〇〇时报'}
        
        self.stype2Name = {1:u'海防艦', 2:u'駆逐艦', 3:u'軽巡洋艦', 4:u'重雷装巡洋艦', 5:u'重巡洋艦', \
                           6:u'航空巡洋艦', 7:u'軽空母', 8:u'巡洋戦艦', 9:u'戦艦', 10:u'航空戦艦', 11:u'正規空母', \
                           12:u'超弩級戦艦', 13:u'潜水艦', 14:u'潜水空母', 15:u'補給艦(敵のほう)', 16:u'水上機母艦', \
                           17:u'揚陸艦', 18:u'装甲空母', 19:u'工作艦', 20:u'潜水母艦', 21:u'練習巡洋艦', 22:u'補給艦'}

        self.seasonalSuffix = self.config['voice_config']['seasonal_suffix']
        self.newShipId = self.config['voice_config']['new_ship_id']
        self.updateDate = self.config['voice_config']['update_date']
        
        self.downloadIncludeId = self.config['download_config']['include_id']
        self.downloadExcludeId = self.config['download_config']['exclude_id']
        self.shipIdThreshold = 1000 if self.config['download_config']['is_include_enemy'] else 500
        self.thresholdLowForDebug = self.config['download_config']['threshold_low_for_debug']
        self.thresholdUpForDebug = self.config['download_config']['threshold_up_for_debug']
        self.voiceIdRange = self.config['download_config']['voice_id_range']

        self.voiceDataJsonFile = 'voice_data.json'
        if not os.path.exists(self.voiceDataJsonFile):
            with open(self.voiceDataJsonFile, 'w') as fp:
                fp.write('{}')
        with codecs.open(self.voiceDataJsonFile, 'r', 'utf-8') as fp:
            self.voiceDataJson = json.load(fp)
        
        self.downloadVoiceLog = None
        self.uploadVoiceLog = None

        if not os.path.exists('voice_' + self.seasonalSuffix):
            os.mkdir('voice_' + self.seasonalSuffix)
        
        with open('subtitlesZh.json', 'r') as fp:
            self.subtitlesZh = json.load(fp)
        with open('subtitlesJp.json', 'r') as fp:
            self.subtitlesJp = json.load(fp)

#-------------------------------- Download Voice --------------------------------

    def getVoiceCacheUrl(self, shipId, voiceId, filename):
        voiceCacheId = (shipId + 7) * 17 * (self.vcKey[voiceId] - self.vcKey[voiceId - 1]) % 99173 + 100000
        return self.voiceCacheUrlprefix + 'kc' + filename + '/' + str(voiceCacheId) + '.mp3', voiceCacheId
        
    def isUpdate(self, modifiedDate):
        if (modifiedDate.split()[1] in self.updateDate[0]) \
        and (modifiedDate.split()[2] == self.updateDate[1]) \
        and (modifiedDate.split()[3] == self.updateDate[2]):
            return True
        else:
            return False

    def downloadVoice(self):
        self.downloadVoiceLog = codecs.open('log_download_voice_' + self.timestamp + '.log', 'w', 'utf-8')
        num = 1
        for ship in self.kcdataJson:
            shipId = int(ship['id'])
            if num < self.thresholdLowForDebug:
                num += 1
                continue
            if num > self.thresholdUpForDebug:
                break
            if len(self.downloadIncludeId) > 0 and shipId not in self.downloadIncludeId:
                continue
            if len(self.downloadExcludeId) > 0 and shipId in self.downloadExcludeId:
                continue
            if shipId > self.shipIdThreshold:
                continue

            filename = ship['filename']
            chineseName = ship['chinese_name']
            stype = ship['stype']
            wikiId = ship['wiki_id']
            if chineseName == None:
                continue
            
            printResult = str(shipId) + '(' + chineseName + ')' + ' : '
            print str(num) + '\t' + printResult,
            self.downloadVoiceLog.write(printResult)
            for voiceId in self.voiceIdRange:
                voiceCacheUrl, voiceCacheId = self.getVoiceCacheUrl(shipId, voiceId, filename)
                response = requests.get(voiceCacheUrl, self.headers)
                if response and self.isUpdate(response.headers['Last-Modified']):
                    # if response:
                    if (shipId not in self.newShipId) and (self.config['voice_config']['type'] == 'seasonal'):
                        wikiFilename = wikiId + '-' + self.voiceId2Name[voiceId] + self.seasonalSuffix + '.mp3'
                    else:
                        wikiFilename = wikiId + '-' + self.voiceId2Name[voiceId] + '.mp3'
                    data = response.content
                    with open('voice_' + self.seasonalSuffix + '/' + wikiFilename, 'wb') as f:
                        f.write(data)

                    print voiceId, 'y',
                    # update log file
                    self.downloadVoiceLog.write(str(voiceId) + ', ')
                    # update json file
                    if shipId not in self.voiceDataJson:
                        self.voiceDataJson.update({ shipId :
                                                    { 'chinese_name': chineseName,
                                                      'stype': stype,
                                                      'wiki_id': wikiId,
                                                      'voice_status': {voiceId: 'download'},
                                                      'voice_duplicate': {},
                                                      'voice_upload_info': {},
                                                      'voice_cache_url': {voiceId: voiceCacheUrl},
                                                      'voice_wiki_filename': {voiceId: wikiFilename }}})
                    else:
                        self.voiceDataJson[shipId]['voice_status'].update({voiceId: 'download'})
                        self.voiceDataJson[shipId]['voice_cache_url'].update({voiceId: voiceCacheUrl})
                        self.voiceDataJson[shipId]['voice_wiki_filename'].update({voiceId: wikiFilename})
                else:
                    print voiceId, 'x',
                with codecs.open(self.voiceDataJsonFile, 'w', 'utf-8') as fp:
                    json.dump(self.voiceDataJson, fp, ensure_ascii = False, indent = 4)
                    # json.dump(self.voiceDataJson, fp)
            print
            self.downloadVoiceLog.write('\n')
            num = num + 1
        self.downloadVoiceLog.close()
        shutil.copy(self.voiceDataJsonFile, self.voiceDataJsonFile[:-5] + '_backup_download_voice.json')        

#-------------------------------- Remove Duplicated Voice --------------------------------
    def removeDuplicatedVoice(self):
        for ship in self.kcdataJson:
            shipId = str(ship['id'])
            if shipId in self.voiceDataJson:
                for voiceId in self.voiceDataJson[shipId]['voice_status']:
                    if ship['after_ship_id'] != None:
                        nextShipId = str(ship['after_ship_id'])
                        if nextShipId in self.voiceDataJson:
                            nextShipWikiFilename = self.voiceDataJson[nextShipId]['voice_wiki_filename'][voiceId]
                            shipWikiFilename = self.voiceDataJson[shipId]['voice_wiki_filename'][voiceId]
                            # print shipWikiFilename, nextShipWikiFilename
                            if hashlib.md5(open('voice_' + self.seasonalSuffix + '/' + shipWikiFilename, 'rb').read()).hexdigest() \
                            == hashlib.md5(open('voice_' + self.seasonalSuffix + '/' + nextShipWikiFilename, 'rb').read()).hexdigest():
                                self.voiceDataJson[nextShipId]['voice_status'][voiceId] = 'duplicate_1'
                                self.voiceDataJson[nextShipId]['voice_duplicate'].update({voiceId: shipWikiFilename})
        with codecs.open(self.voiceDataJsonFile, 'w', 'utf-8') as fp:
            json.dump(self.voiceDataJson, fp, ensure_ascii = False, indent = 4)
        shutil.copy(self.voiceDataJsonFile, self.voiceDataJsonFile[:-5] + '_backup_remove_duplicated_voice.json') 

#-------------------------------- Upload Voice --------------------------------
    def uploadVoice(self):
        self.uploadVoiceLog = codecs.open('log_upload_voice_' + self.timestamp + '.log', 'w', 'utf-8')
        self.login()
        totalNum = 0
        for shipId in self.voiceDataJson:
            if len(self.downloadIncludeId) > 0 and int(shipId) not in self.downloadIncludeId:
                continue
            if len(self.downloadExcludeId) > 0 and int(shipId) in self.downloadExcludeId:
                continue
            chineseName = self.voiceDataJson[shipId]['chinese_name'] 
            for voiceId in self.voiceDataJson[shipId]['voice_status']:
                if self.voiceDataJson[shipId]['voice_status'][voiceId] != 'download':
                    continue
                wikiFilename = self.voiceDataJson[shipId]['voice_wiki_filename'][voiceId]
                totalNum += 1

                rdata = {'action': 'upload', 'token': self.editToken, 'format': 'json', 'filename': wikiFilename}
                files = {'file': open('voice_' + self.seasonalSuffix + '/' + wikiFilename, 'rb')}

                response = requests.post(self.zhKcWikiUrl, rdata, cookies = self.cookies, headers = self.headers, files = files)
                result = response.json()['upload']['result'].encode('utf-8')
                if result == 'Success':
                    resultPrint = str(shipId) + '(' + chineseName + ')' + ' : ' + wikiFilename + ' : ' + 'Success'
                    print str(totalNum) + '\t' + resultPrint
                    self.uploadVoiceLog.write(str(shipId) + ' : ' + wikiFilename + ' : ' + 'Success' + '\n')
                    self.voiceDataJson[shipId]['voice_status'][voiceId] = 'upload'
                else:
                    resultPrint = str(shipId) + '(' + chineseName + ')' + ' : ' + wikiFilename + ' : ' + 'Failed'
                    print str(totalNum) + '\t' + resultPrint + '\n\t' + response.text
                    self.uploadVoiceLog.write(resultPrint + '\n\t')
                    self.uploadVoiceLog.write(json.dumps(response.json()) + '\n')
                    if 'warnings' in response.json()['upload']:
                        if 'duplicate' in response.json()['upload']['warnings']:
                            duplicatedWikiFilenames = response.json()['upload']['warnings']['duplicate']
                            self.voiceDataJson[shipId]['voice_status'][voiceId] = 'duplicate_2'
                            self.voiceDataJson[shipId]['voice_duplicate'].update({voiceId: duplicatedWikiFilenames})
                        else:
                            self.voiceDataJson[shipId]['voice_status'][voiceId] = 'warnings'
                            self.voiceDataJson[shipId]['voice_upload_info'].update({voiceId: response.json()['upload']})
                    else:
                        self.voiceDataJson[shipId]['voice_status'][voiceId] = 'errors'
                        self.voiceDataJson[shipId]['voice_upload_info'].update({voiceId: response.json()['upload']})
                with codecs.open(self.voiceDataJsonFile, 'w', 'utf-8') as fp:
                    json.dump(self.voiceDataJson, fp, ensure_ascii = False, indent = 4)
        shutil.copy(self.voiceDataJsonFile, self.voiceDataJsonFile[:-5] + '_backup_upload_voice.json')

#-------------------------------- generate wiki code --------------------------------
    def generateUnitWikiCodeSeasonal(self, wikiId, chineseName, wikiFilename, subtitleJp, subtitleZh):
        rname = ''
        rname = rname + u'{{台词翻译表|type=seasonal' + '\n'
        rname = rname + u' | 档名 = ' + wikiFilename + '\n'
        rname = rname + u' | 编号 = ' + wikiId + '\n'
        rname = rname + u' | 舰娘名字 = ' + chineseName + '\n'
        rname = rname + u' | 日文台词 = ' + subtitleJp + '\n'
        rname = rname + u' | 中文译文 = ' + subtitleZh + '\n'
        rname = rname + '}}' + '\n'
        return rname
    
    def generateUnitWikiCodeNewship(self, voiceId, wikiFilename, subtitleJp, subtitleZh):
        rname = ''
        rname = rname + u'{{台词翻译表' + '\n'
        rname = rname + u' | 档名 = ' + wikiFilename[:-4] + '\n'
        rname = rname + u' | 场合 = ' + self.voiceId2NameZh[int(voiceId)] + '\n'
        rname = rname + u' | 日文台词 = ' + subtitleJp + '\n'
        rname = rname + u' | 中文译文 = ' + subtitleZh + '\n'
        rname = rname + '}}' + '\n'
        return rname

    def generateSectionWikiCode(self, unitList, wikiCodeSuffix):
        wikiCodeStr = ''
        for stype in range(len(unitList)):
            shipDict = unitList[stype]
            if not shipDict:
                continue
            wikiCodeStr = wikiCodeStr + '===' + self.stype2Name[stype] + '===' + '\n'
            wikiCodeStr = wikiCodeStr + u'{{台词翻译表/页头|type=seasonal}}' + '\n'
            sortedUnitList = sorted(shipDict.iteritems(), key=lambda d:d[0])
            for ship in sortedUnitList:
                subtitleJp = '' if ship[1]['ship_id'] not in self.subtitlesJp or ship[1]['voice_id'] not in self.subtitlesJp \
                                else self.subtitlesJp[ship[1]['ship_id']][ship[1]['voice_id']]
                subtitleZh = '' if ship[1]['ship_id'] not in self.subtitlesZh or ship[1]['voice_id'] not in self.subtitlesZh \
                                else self.subtitlesZh[ship[1]['ship_id']][ship[1]['voice_id']]
                wikiCodeStr = wikiCodeStr + self.generateUnitWikiCodeSeasonal(ship[1]['wiki_id'], ship[1]['chinese_name'], ship[0], subtitleJp, subtitleZh)
            wikiCodeStr = wikiCodeStr + u'{{页尾}}' + '\n\n'
        wikiCodeFile = codecs.open('wikicode_' + self.seasonalSuffix + wikiCodeSuffix, 'w', 'utf-8')
        wikiCodeFile.write(wikiCodeStr)
        wikiCodeFile.close()

    def generateWikiCodeSeasonal(self):
        oldUnitList = [{} for i in range(23)]
        newUnitList = [{} for i in range(23)]
        for shipId in self.voiceDataJson:
            if len(self.downloadIncludeId) > 0 and int(shipId) not in self.downloadIncludeId:
                continue
            if len(self.downloadExcludeId) > 0 and int(shipId) in self.downloadExcludeId:
                continue
            for voiceId in self.voiceDataJson[shipId]['voice_status']:
                chineseName = self.voiceDataJson[shipId]['chinese_name']
                stype = self.voiceDataJson[shipId]['stype']
                wikiId = self.voiceDataJson[shipId]['wiki_id']
                wikiFilename = self.voiceDataJson[shipId]['voice_wiki_filename'][voiceId]
                voiceStatus = self.voiceDataJson[shipId]['voice_status'][voiceId]
                if voiceStatus == 'warnings' or voiceStatus == 'upload':
                    newUnitList[stype].update({ wikiFilename[:-4]:
                                                { 'ship_id': shipId,
                                                  'voice_id': voiceId,
                                                  'wiki_id': wikiId,
                                                  'chinese_name': chineseName}})
                if voiceStatus == 'duplicate_2':
                    duplicatedWikiFilename = self.voiceDataJson[shipId]['voice_duplicate'][voiceId][0]
                    if duplicatedWikiFilename[-8:-5] != '201':
                        continue
                    oldUnitList[stype].update({ duplicatedWikiFilename[:-4]:
                                                { 'ship_id': shipId,
                                                  'voice_id': voiceId,
                                                  'wiki_id': wikiId,
                                                  'chinese_name': chineseName}})
        self.generateSectionWikiCode(oldUnitList, '_old')
        self.generateSectionWikiCode(newUnitList, '')

    def generateWikiCodeNewship(self):
        for shipId in self.voiceDataJson:
            if len(self.downloadIncludeId) > 0 and int(shipId) not in self.downloadIncludeId:
                continue
            if len(self.downloadExcludeId) > 0 and int(shipId) in self.downloadExcludeId:
                continue
            wikiCodeStr = ''
            chineseName = self.voiceDataJson[shipId]['chinese_name']
            wikiCodeStr += '===' + chineseName + '===' + '\n'
            wikiCodeStr += u'{{台词翻译表/页头}}' + '\n'
            for intVoiceId in range(1, 54):
                voiceId = str(intVoiceId)
                if voiceId not in self.voiceDataJson[shipId]['voice_status']:
                    continue
                wikiId = self.voiceDataJson[shipId]['wiki_id']
                wikiFilename = self.voiceDataJson[shipId]['voice_wiki_filename'][voiceId]
                voiceStatus = self.voiceDataJson[shipId]['voice_status'][voiceId]
                if voiceStatus == 'upload' or voiceStatus == 'warnings':
                    subtitleJp = '' if shipId not in self.subtitlesJp or voiceId not in self.subtitlesJp \
                                    else self.subtitlesJp[shipId][voiceId]
                    subtitleZh = '' if shipId not in self.subtitlesZh or voiceId not in self.subtitlesZh \
                                    else self.subtitlesZh[shipId][voiceId]
                    wikiCodeStr += self.generateUnitWikiCodeNewship(voiceId, wikiFilename, subtitleJp, subtitleZh)
            wikiCodeStr += u'{{页尾}}' + '\n\n'
            wikiCodeFile = codecs.open('wikicode_' + shipId + '_' + chineseName, 'w', 'utf-8')
            wikiCodeFile.write(wikiCodeStr)
            wikiCodeFile.close()

    def generateWikiCode(self):
        if self.config['voice_config']['type'] == 'seasonal':
            self.generateWikiCodeSeasonal()
        if self.config['voice_config']['type'] == 'new_ship':
            self.generateWikiCodeNewship()