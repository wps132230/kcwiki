import json
import requests
import codecs
import datetime

class KcwikiClient:
    def __init__(self):
        self.zhKcWikiUrl = 'http://zh.kcwiki.moe/api.php'
        self.loginToken = ""
        self.editToken = ""
        self.cookies = ""
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0',\
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
                       'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3', \
                       'Accept-Encoding': 'gzip, deflate', \
                       'Connection': 'keep-alive'}

        self.kcdataJsonUrl = 'http://kcwikizh.github.io/kcdata/ship/all.json'
        self.kcdataJson = self.getKcdataJson(self.kcdataJsonUrl)
        self.timestamp = str(datetime.datetime.now())
        with open('config.json', 'r') as fp:
            self.config = json.load(fp)

    def getKcdataJson(self, url):
        response = requests.get(url)
        return response.json()

    def login(self):
        # login token
        rdata = {'action': 'query', 'meta': 'tokens', 'type': 'login', 'format': 'json'}
        response = requests.post(self.zhKcWikiUrl, rdata, headers = self.headers)
        if not response:
            print "failed to get login token!"
        self.loginToken = response.json()['query']['tokens']['logintoken']
        self.cookies = response.cookies.get_dict()

        rdata = {'action': 'login', 'format': 'json', 'lgtoken': self.loginToken}
        rdata['lgname'] = self.config['login_config']['user_name']
        rdata['lgpassword'] = self.config['login_config']['password']
        response = requests.post(self.zhKcWikiUrl, rdata, cookies = self.cookies, headers = self.headers)
        if not response:
            print "failed to log in!"
        self.cookies = response.cookies.get_dict()

        rdata = {'action': 'query', 'meta': 'tokens', 'format': 'json'}
        response = requests.post(self.zhKcWikiUrl, rdata, cookies = self.cookies, headers = self.headers)
        if not response:
            print "failed to get edit token!"
        self.editToken = response.json()['query']['tokens']['csrftoken']
