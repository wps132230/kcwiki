# coding = utf8

import json
import requests
import os
from pandas import Series, DataFrame


def getFileName(api_id, start2json):
    for sg in start2json['api_mst_shipgraph']:
        if sg['api_id'] == api_id:
            return sg['api_filename']


def getWikiId(api_id, all):
    for a in all:
        if a['id'] == api_id:
            return a['wiki_id']


def getcnName(api_id, all):
    for a in all:
        if a['id'] == api_id:
            return a['chinese_name']


def rebuildDataJson():
    f = open('friendlyrecords.json', 'rb')
    ship_ids = []
    voice_ids = []
    voice_count = 0
    print("Start rebuilding...")
    #读取friendlyrecords.json中的记录存储到DataFrame中并去重
    for line in f.readlines():
        js = json.loads(line)
        ship_ids += js['api_ship_id']
        voice_ids += js['api_voice_id']
        voice_count += len(js['api_ship_id'])
        print("\rReading record {}...".format(voice_count), end='', flush=True)
    print("\nTotal records {}.".format(voice_count))
    df = DataFrame({'ship_id':Series(ship_ids), 'voice_id':Series(voice_ids)})
    df.drop_duplicates(subset=None, keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)
    print("Voice files {}.".format(len(df)))
    #从start2.json和all.json中获取对应的filename和wiki_id
    f = open('start2.json', 'rb')
    js = json.loads(f.read())
    filenames = []
    for shipid in df.ship_id:
        filenames.append(getFileName(shipid, js))
    df.insert(len(df.columns), 'filename', filenames)
    print("Filename appended to DataFrame.")
    wiki_ids = []
    cn_names = []
    f = open('all.json', 'rb')
    js = json.loads(f.read())
    for shipid in df.ship_id:
        wiki_ids.append(getWikiId(shipid, js))
        cn_names.append(getcnName(shipid, js))
    df.insert(len(df.columns), 'wiki_id', wiki_ids)
    df.insert(len(df.columns), 'cn_name', cn_names)
    print('Wiki_id appended to DataFrame.')
    f = open('friendlyvoicelist.json', 'w')
    f.write(df.to_json(orient ='records'))
    f.close()
    print("Rebulid Complished.")



def genWikiText(filename, path):
    datafile = open('friendlyvoicelist.json', 'r')
    data = json.load(datafile)
    text = '===友军舰队===\n{{台词翻译表/页头}}\n'
    filelist = os.listdir(path)
    for d in data:
        voice_name = '{}-FriendFleet{}'.format(d['wiki_id'], d['voice_id'])
        if voice_name + '.mp3' in filelist:
            text += "{{台词翻译表\n | 档名 =" + voice_name + "\n | 场合 =" + d['cn_name'] \
                    + "\n | 日文台词 =\n | 中文译文 =\n}}\n"
        else:
            text += "{{台词翻译表\n | 档名 =" + voice_name + "\n | 场合 =" + d['cn_name'] + '(文件不存在)' \
                    + "\n | 日文台词 =\n | 中文译文 =\n}}\n"
    text += '{{页尾}}'
    with open(filename, 'w', encoding='utf-8') as text_file:
        text_file.write(text)
        text_file.close()
    print("wikiText generated--" + filename)



def genmp3Urls_filenames(newjson, urls, filenames):
    for nj in newjson:
        urls.append("http://voice.kcwiki.moe/kcs/sound/kc{}/".format(nj['filename']) + "{}.mp3".format(nj['voice_id']))
        filenames.append('{}-FriendFleet{}.mp3'.format(nj['wiki_id'], nj['voice_id']))


def downloadmp3(urls, filenames, path):
    success = 0
    for i in range(len(urls)):
        print("Downloading " + filenames[i])
        r = requests.get(urls[i])
        if r.status_code == 200:
            success += 1
            with open(os.path.join(path, filenames[i]), 'wb') as f:
                f.write(r.content)
                f.close()
        else:
            print(filenames[i] + ' Error ' + str(r.status_code))
    print("Download complete, downloaded {} voices.".format(success))





