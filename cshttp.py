#!/usr/bin/python
import http.client
import err
import random
import btools

class cshttp:

	def connect(self,s_addr,prot):
		port = random.randrange(10000,60000)
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
			'https':443
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

	def request(self,method,url,s_addr):
		self.raw_url=url
		self.params=self.parse_url()
		if not self.params: return False
		self.params['method']=self.check_method(method)
		if not self.params['method']: return False
		self.params['s_addr']=s_addr
		self.connect(self.params['s_addr'],self.params['prot'])
		try:
			self.sock.request(self.params['method'],self.params['url'])
		except:
			err.warn('cshttp_request','{}'.format(self.params))
		res = self.sock.getresponse()
		err.log("Status: {} Reason: {}".format(res.status,res.reason))
		if res.status == 302 : 
			self.sock.close()
			self.request(method,res.getheader('Location'),s_addr)
		return btools.tryutf8(res.read())

	def get(self,url,s_addr):
		return self.request('GET',url,s_addr)

	def post(self,url,s_addr):
		return self.request('POST',url,s_addr)
