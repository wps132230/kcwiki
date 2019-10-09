import os
import requests
import json
from FriendlyRecords import *
from KcwikiClient import KcwikiClient


def downVoiceFromFriendlyRecords(path):
    rebuildDataJson()
    f = open('friendlyvoicelist.json', 'r')
    js = json.load(f)
    urls = []
    fns = []
    genmp3Urls_filenames(js, urls, fns)
    downloadmp3(urls, fns, path)


def loginWiki(mysession):
    print("Login start, getting login token...")
    kcwikiAPIUrl = 'https://zh.kcwiki.org/api.php'
    with open('config.json', 'r') as f:
        cfg = json.loads(f.read())
        user_name = cfg['login_config']['user_name']
        user_pswd = cfg['login_config']['password']
        f.close()
    print("Login token get, ready to login...")
    rdata = {
            'action': 'query',
            'meta': 'tokens',
            'type': 'login',
            'format': 'json'
        }
    resp = mysession.post(kcwikiAPIUrl, data=rdata)
    resp_json = resp.json()

    rdata = {
        'action': 'login',
        'format': 'json',
        'lgtoken': resp_json['query']['tokens']['logintoken'],
        'lgname': user_name,
        'lgpassword': user_pswd
    }
    resp = mysession.post(kcwikiAPIUrl, data=rdata)
    #resp_json = resp.json()
    rdata = {
        'action': 'query',
        'meta': 'tokens',
        'format': 'json'
    }
    print("Getting edit token...")
    resp = mysession.post(kcwikiAPIUrl, data=rdata)
    resp_json = resp.json()
    print("login successfully!")
    print("Edit token is " + resp_json['query']['tokens']['csrftoken'])
    return resp_json['query']['tokens']['csrftoken']


def uploadVoice(path, mysession, editToken):
    kcwikiAPIUrl = 'https://zh.kcwiki.org/api.php'
    filelist = os.listdir(path)
    i = 0
    for fff in filelist:
        rdata = {
            'action': 'upload',
            'token': editToken,
            'format': 'json',
            'filename': fff,
        }
        resp = mysession.post(kcwikiAPIUrl, data=rdata, files=[('file', open(os.path.join(path, fff), 'rb'))])
        #print(resp.content)
        print('Uploading ' + fff)
        i += 1
    print("Upload Finished!")
    print("Uploaded {} files.".format(i))


if __name__ == "__main__":
    path = ''#path为存放语音文件的目录
    rebuildDataJson()
    downVoiceFromFriendlyRecords(path)
    genWikiText('2019SummerFriendFleet.txt', path)

    mySess = requests.session()
    editToken = loginWiki(mySess)
    uploadVoice(path, mySess, editToken)

