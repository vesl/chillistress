#!/usr/bin/python
import http.client
import err
import random
import btools
import urllib.parse

class cshttp:

	def __init__(self):
		self.headers={'User-Agent':'Mozilla/5.0 (Linux; U; Android 2.2.2; tr-tr; GM FOX Build/HuaweiU8350) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1','Accept-Language':'en-gb;q=0.8, en;q=0.7'}

	def connect(self,s_addr,prot,customPort=False):
		port = random.randrange(10000,60000)
		if customPort : self.params['port'] = customPort['port']['port']
		if prot == 'http' : self.sock=http.client.HTTPConnection(self.params['host'],self.params['port'],source_address=(self.params['s_addr'],port))
		elif prot == 'https' : self.sock=http.client.HTTPSConnection(self.params['host'],self.params['port'],source_address=(self.params['s_addr'],port))

	def parse_url(self):
		host = self.raw_url.split('/')[2]
		if not host : 
			err.warn('cshttp_invalid_url','{}'.format(self.raw_url))
			return False
		url = '/' if not  "".join(self.raw_url.split('/')[3:]) else "/"+"".join(self.raw_url.split('/')[3:])
		prot = self.raw_url.split('://')[0]
		port = {
                        'http':80,
			'https':443,
		}
		try:
			return {
				'prot':prot,
				'host':host,
				'url':url,
				'port':port[prot]
			}
		except KeyError:
			err.warn('cshttp_protocol','{}'.format(prot))
			return False

	def check_method(self,method):
		methods={
			'GET':'GET',
			'POST':'POST',
		}
		try:
			return methods[method]
		except KeyError:
			err.warn('cshttp_method','{}'.format(method))
			return False

	def request(self,method,url,s_addr,data=False,**port):
		self.raw_url=url
		self.params=self.parse_url()
		if not self.params: return False
		self.params['method']=self.check_method(method)
		if not self.params['method']: return False
		self.params['s_addr']=s_addr
		if not port : port = False
		self.connect(self.params['s_addr'],self.params['prot'],port)
		try:
			if not data : self.sock.request(self.params['method'],self.params['url'],headers=self.headers)
			else : 
				headers=btools.mergedicts(self.headers,{"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"})
				print(headers)
				self.sock.request(self.params['method'],self.params['url'],urllib.parse.urlencode(data),headers)
		except Exception as e:
			err.warn('cshttp_request','Params : {} Err : {}'.format(self.params,e))
		res = self.sock.getresponse()
		err.log("Status: {} Reason: {}".format(res.status,res.reason))
		if res.status == 302 : data = res.getheader('Location')
		else : data = btools.tryutf8(res.read())
		self.sock.close()
		return {'status':res.status,'data':data}

	def get(self,url,s_addr,**port):
		return self.request('GET',url,s_addr,port=port)

	def post(self,url,s_addr,data):
		return self.request('POST',url,s_addr,data)
