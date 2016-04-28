#-*- coding: utf-8 -*-
# ============================================
#  __  __            _           _   
# |  \/  | ___   ___| |__   ___ | |_ 
# | |\/| |/ _ \ / _ \ '_ \ / _ \| __|
# | |  | | (_) |  __/ |_) | (_) | |_ 
# |_|  |_|\___/ \___|_.__/ \___/ \__|
# 
# --------------------------------------------
# @Author: grzhan
# @Date:   2015-06-07
# @Email:  i@grr.moe
# @Description: commons维基的图片清理脚本

from requests import (post,ConnectionError,HTTPError,
	Timeout,TooManyRedirects)
from functools import wraps
import logging
import sys
import time
import json

logging.basicConfig(
	filename = 'moebot.log',
	format = '%(levelname)-10s %(asctime)s %(message)s',
	level = logging.DEBUG
)

logger = logging.getLogger('moebot')
logger.addHandler(logging.StreamHandler(sys.stdout))


class MWAPIException(Exception):
	"""
	MWAPIException MWAPI函数中异常
	"""
	pass


def MWAPIWrapper(func):
	"""
	MWAPIWrapper 控制API请求异常的装饰器
	根据requests库定义的异常来控制请求返回的意外情况
	"""
	@wraps(func)
	def wrapper(*args,**kwargs):
		self = args[0]
		try:
			result = func(*args,**kwargs)
			return result
		except ConnectionError:
			err_title = '连接错误'
			err_message = '[{name}] 连接错误，网络状况异常'.format(name=func.__name__,host=self.host)
		except HTTPError as e:
			err_title = 'HTTP响应错误'
			err_message = '[{name}] 目标服务器"{host}" HTTP响应错误({detail})'.format(name=func.__name__,
				host=self.host,detail=e.message)
		except Timeout:
			err_title = '请求超时'
			err_message = '[{name}] 目标服务器"{host}" 请求超时'.format(name=func.__name__,host=self.host)
		except TooManyRedirects:
			err_title = '过多重定向'
			err_message = '[{name}] 目标服务器"{host}" 过多重定向'.format(name=func.__name__,host=self.host)
		except ValueError as e:
			if e.message.find('JSON') >= 0:
				err_title = 'API JSON返回值异常'
				err_message = '[{name}] 目标服务器"{host}" API JSON返回值异常'.format(name=func.__name__,host=self.host)
			else:
				err_title = '值错误'
				err_message = '[{name}] 存在ValueError：{msg}'.format(name=func.__name__,msg=e.message)
				self.log.error(e,exc_info=True)
		except KeyError as e:
			err_title = '键错误'
			err_message = '[{name}] 存在KeyError，错误键为{key}'.format(name=func.__name__,key=e.message)
			self.log.error(e,exc_info=True)

		except MWAPIException as e:
			err_title = 'Mediawiki API 异常'
			err_message = e.message

		self.log.error('%s:%s',err_title, err_message)
		return {'success': False, 'errtitle': err_title, 'errmsg': err_message}
	return wrapper


class MwApi(object):
	"""Mediawiki API 类"""
	def __init__(self, host, username = '', password = '',limit=5):
		super(MwApi, self).__init__()
		self.host = host
		self.login_exceptions = {
			'WrongPass' : 'Mediawiki登陆密码错误',
			'EmptyPass' : 'Mediawiki密码未填写',
			'NotExists' : 'Mediawiki该用户不存在',
			'NoName'    : 'Mediawiki用户未填写'
		}
		self.signin_cookies = {}
		self.rlimit = limit
		self.log = logging.getLogger('moebot')
		self.ua = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 \
	(KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'}
		self.timestamp = ""


	@MWAPIWrapper
	def post(self, rdata, headers = {}):
		headers.update(self.ua)
		return post(self.host, rdata, 
			cookies=self.signin_cookies, headers=headers)

	
	@MWAPIWrapper
	def login(self,username,password):
		rdata = {'action':'login','format':'json'}
		rdata['lgname'] = username
		rdata['lgpassword'] = password
		# 第一次登陆验证
		rep = self.post(rdata)
		self.signin_cookies = rep.cookies.get_dict()
		result = rep.json()['login']['result'].encode('utf-8')
		if result in self.login_exceptions:
			raise MWAPIException(self.login_exceptions[result])
		if not self.signin_cookies:
			raise MWAPIException('登陆响应Cookie为空，请检查Mediawiki的用户名密码是否正确')
		rdata['lgtoken'] = rep.json()['login']['token']
		
		# 第二次登陆验证
		rep = self.post(rdata)
		result = rep.json()['login']['result'].encode('utf-8')
		if result == 'Success':	
			signin_cookies = rep.cookies.get_dict()
			if signin_cookies == {}:
				raise MWAPIException('二步登陆响应Cookie为空，请联系开发者检查有关程序')
			self.signin_cookies.update(signin_cookies)
			self.log.info('[%s] 登陆成功，用户名：%s',self.host, username)
			return {'success': True, 'json': rep.json() }
		elif result in self.login_exceptions:
			raise MWAPIException(self.login_exceptions[result])
		else:
			raise MWAPIException('登陆异常：' + result)

	@MWAPIWrapper
	def edit_token(self):
		rdata = {'action':'query','meta':'tokens','format':'json'}
		rep = self.post(rdata)
		token = rep.json()['query']['tokens']['csrftoken']
		return {'success': True, 'token': token}


	@MWAPIWrapper
	def delete(self,title=None,pageid=None, reason="Delete by moebot"):
		rdata = {'action':'delete', 'format':'json'}
		rdata['reason'] = reason
		if pageid:
			rdata['pageid'] = pageid
		elif title:
			rdata['title'] = title
		else:
			raise MWAPIException('删除失败，未得到标题或PageID参数')
		token_result = self.edit_token()
		if token_result['success']:
			rdata['token'] = token_result['token']
		else:
			raise MWAPIException('编辑token获取失败')
		headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
		rep = self.post(rdata, headers=headers)
		data = rep.json()
		if not 'delete' in data:
			self.log.error(rep.content)
			raise MWAPIException('删除失败')

	@MWAPIWrapper
	def edit(self,content,reason,pageid=None,title=None):
		rdata = {'action':'edit','format':'json'}
		if pageid:
			rdata['pageid'] = pageid
		elif title:
			rdata['title'] = title
		rdata['text'] = content
		rdata['bot'] = 1
		rdata['summary'] = reason
		token_result = self.edit_token()
		if token_result['success']:
			rdata['token'] = token_result['token']
		else:
			raise MWAPIException('编辑token获取失败')
		headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
		rep = self.post(rdata, headers=headers)
		rep_json = rep.json()
		if 'edit' in rep_json and 'result' in rep_json['edit'] \
		and rep_json['edit']['result'] == 'Success':
			return {'success': True, 'json': rep_json}
		# TODO 对于编辑结果异常的细化处理
		elif 'error' in rep_json:
			raise MWAPIException('编辑失败，出错码【{code}】:{info}'.format(code=rep_json['error']['code'],
				info=rep_json['error']['info']))
		else:
			raise MWAPIException('编辑失败，未知错误：{json}'.format(json=rep_json))

	def files_generator(self):
		rdata = {'action': 'query', 'generator': 'allpages','gapnamespace': '6',
					'gaplimit': self.rlimit,'format':'json','prop':'revisions','rvprop': 'content'}
		while 1:
			data = self.post(rdata).json()
			files = data['query']['pages']
			yield files
			if 'query-continue' in data and 'allpages' in data['query-continue']:
				rdata['gapfrom'] = data['query-continue']['allpages']['gapcontinue']
			else:
				break

	def images_generator(self):
		rdata = {'action' :'query', 'list':'allimages', 'aisort' : 'timestamp',
		'format':'json','aiprop':'timestamp|url|comment','ailimit': self.rlimit}
		if self.timestamp:
			rdata['aistart'] = self.timestamp
		while 1:
			rep = self.post(rdata)
			images = rep.json()['query']['allimages']
			yield images
			if 'query-continue' in rep.json():
				contimestamp = rep.json()['query-continue']['allimages']['aicontinue'].split('|')[0]
				self.timestamp = contimestamp
				rdata['aistart'] = contimestamp
			else:
				break

	@MWAPIWrapper
	def contents(self,titles=[],pids=[]):
		rdata = {'action': 'query', 'format':'json','prop':'revisions','rvprop':'content'}
		self.log.info('Title数量：%d',len(titles))
		if titles:
			rdata['titles'] = '|'.join(titles)
		elif pids:
			rdata['pageids'] = '|'.join(pids)
		else:
			raise MWAPIException
		rep = self.post(rdata).json()
		if rep and 'query' in rep and 'pages' in rep['query']:
			return {'success': True, 'contents': rep['query']['pages']}
		elif 'error' in rep:
			raise MWAPIException('获取内容失败，出错码【{code}】:{info}'.format(code=rep['error']['code'],
				info=rep['error']['info']))
		# print rep.json()

	@MWAPIWrapper
	def update_timestamp(self):
		pass


def execute():
	mwfrom = MwApi('http://zh.kcwiki.moe/api.php',limit=500)
	mwto = MwApi('http://commons.kcwiki.moe/api.php', limit=500)
	mwfrom.login('grzhan','nishixian')
	mwto.login('grzhan','nishixian')

	mwfrom.log.info('正在抓取[%s]的文件信息', mwfrom.host)


	filesfrom = {}
	for files in mwfrom.files_generator():
		for fileinfo in files.itervalues():
			filesfrom[fileinfo['title']] = fileinfo['revisions'][0]['*']
	mwfrom.log.info('抓取完毕，共【%d】条信息', len(filesfrom))


	mwto.log.info('正在抓取[%s]的文件信息', mwto.host)
	filesto = {}
	for files in mwto.files_generator():
		for fileinfo in files.itervalues():
			if 'revisions' in fileinfo:
				filesto[fileinfo['title']] = fileinfo['revisions'][0]['*']
			else:
				filesto[fileinfo['title']] = ''
	mwto.log.info('抓取完毕，共【%d】条信息', len(filesto))

	diff = []
	for title in filesfrom.iterkeys():
		if title not in filesto:
			print title
	toremove = []
	for title in filesto.iterkeys():
		if title not in filesfrom:
			toremove.append(title)
	mwto.log.info('经对照，共【%d】条信息需要清除', len(toremove))

	json.dump(toremove, open('toremove.json','w'))
	for i,title in enumerate(toremove):
		mwto.log.info(u'({num}/{total}) 正在删除【{title}】'.format(num=i,total=len(toremove), title=title))
		mwto.delete(title=title)

def delete_with_cache():
	mwto = MwApi('http://commons.kcwiki.moe/api.php', limit=500)
	mwto.login('grzhan','')
	toremove = json.load(open('toremove.json','r'))
	for title in toremove:
		mwto.delete(title=title)


if __name__ == '__main__':
	execute()



