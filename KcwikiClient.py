import json
import aiohttp
import codecs
import datetime
import async_timeout

from KcwikiClientException import KcwikiClientException


class KcwikiClient:
    kcwikiAPIUrl = 'https://zh.kcwiki.org/api.php'
    kcdataUrl = 'https://kcwikizh.github.io/kcdata/ship/all.json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    }

    def __init__(self):
        self.loginToken = ''
        self.editToken = ''
        self.session = aiohttp.ClientSession()
        self.timestamp = str(
            datetime.datetime.now().strftime(r'%Y_%m_%d')
        )
        self.config = self.loadConfig()
        self.proxy = self.config['proxy'] if 'proxy' in self.config else None

    def loadConfig(self):
        with open('config.json', 'r', encoding='utf-8') as fp:
            return json.load(fp)

    async def request(self, url, method='GET', rdata=None, timeout=10, timeout_message='连接服务器超时'):
        with async_timeout.timeout(timeout):
            try:
                return await self.session.request(
                    method=method,
                    data=rdata, url=url,
                    headers=self.headers,
                    proxy=self.proxy
                )
            except aiohttp.ServerTimeoutError:
                raise KcwikiClientException(timeout_message)

    async def login(self):
        rdata = {
            'action': 'query',
            'meta': 'tokens',
            'type': 'login',
            'format': 'json'
        }
        response = None
        try:
            response = await self.request(self.kcwikiAPIUrl, 'POST', rdata)
            response = await response.json()
        except aiohttp.client_exceptions.ContentTypeError:
            raise KcwikiClientException('Failed to get login token!')
        if not response:
            raise KcwikiClientException('Failed to get login token!')
        self.loginToken = response['query']['tokens']['logintoken']
        rdata = {
            'action': 'login',
            'format': 'json',
            'lgtoken': self.loginToken
        }
        rdata['lgname'] = self.config['login_config']['user_name']
        rdata['lgpassword'] = self.config['login_config']['password']
        try:
            response = await self.request(self.kcwikiAPIUrl, 'POST', rdata)
            response = await response.json()
        except aiohttp.client_exceptions.ContentTypeError:
            raise KcwikiClientException('Failed to log in!')
        if not response:
            raise KcwikiClientException('Failed to log in!')
        if response['login']['result'] == 'Failed':
            raise KcwikiClientException(response['login']['reason'])
        rdata = {
            'action': 'query',
            'meta': 'tokens',
            'format': 'json'
        }
        try:
            response = await self.request(self.kcwikiAPIUrl, 'POST', rdata)
            response = await response.json()
        except aiohttp.client_exceptions.ContentTypeError:
            raise KcwikiClientException('Failed to get edit token!')
        if not response:
            raise KcwikiClientException('Failed to get edit token!')
        self.editToken = response['query']['tokens']['csrftoken']
        if self.editToken == '+\\':
            raise KcwikiClientException('Incorrect edittoken \'+\\\' !')
        print('Login Successfully!')

    def __del__(self):
        self.session.close()
