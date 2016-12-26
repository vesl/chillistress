#!/usr/bin/python
import cshttp
import csshell
import cshtml
import err
import btools
import urllib.parse

class csclient:
	def __init__(self,tap,config):
		self.cshttp=cshttp.cshttp()
		self.csshell=csshell.csshell()
		self.cshtml=cshtml.cshtml()
        	self.config=config
        	self.config.update({'client':{}})
        	self.config['client'].update({'mac':tap['mac']})
        	self.config['client'].update({'ip':tap['ip']})
		self.config['client'].update({'challenge':btools.randmd5()})
		self.config['client'].update({'md':btools.randmd5()})
		self.config['instance'].update({'mac':self.getinstmac()})

	def getinstmac(self):
		self.csshell.sh('/bin/ping -c 1 {}'.format(self.instip))
		mac=self.csshell.sh('sh/getMacFromIP.sh {}'.format(self.instip))
		if mac['err']: err.crit('csclient_mac','IP:{}'.format(self.instip))
		return mac['out'].replace('\n','')

	def chillipass(self):
		notyet="http://{}/?res=notyet&uamip={}&uamport={}&challenge={}&called={}&mac={}&ip={}&ssid={}&nasid={}&sessionid=585d4fe600000fb0&ssl=https%3a%2f%2fchilli.vipnetwork.fr%3a4990%2f&userurl=&md={}".format(self.config['instance']['domain'],self.config['instance']['ip'],self.config['instance']['uamport'],self.config['clien']['challenge'],self.config['instance']['mac'],self.config['client']['mac'],self.config['client']['ip'],self.config['instance']['ssid'],self.config['instance']['nasid'],self.config['client']['md'])
		err.log('Call url {}'.format(notyet))
		req=self.cshttp.get(notyet,self.ip)
		self.cshtml.check='checkIfChilliPortal'
		self.cshtml.feed(req['data'])
		if self.cshtml.result is False: err.warn('csclient_portal','Status : {}'.format(req['status']))
		else:
			err.log('Catched by portal : {}'.format(self.ip))			
			err.log(req['data'])
			params = urllib.parse.urlencode({'@form[type]':self.config['portal']['type'],
							'@form[login]':self.config['portal']['login'],
							'@form[password]':self.config['portal']['password'],
							'@form[uamip]':self.config['instance']['ip'],
							'@form[uamport]':self.config['instance']['uamport'],
							'@form[challenge]':self.config['client']['challenge'],
							'@form[nasid]':self.config['instance']['nasid'],
							'@form[mac]':self.config['client']['mac'],
							'@form[ip]':self.config['client']['ip'],
							'@form[md]':self.config['client']['md'],
							'@form[userurl]':'',
							'@form[termOfUse]':'true',
							'@form[lastname]':self.config['portal']['lastname'],
							'@form[firstname]':self.config['portal']['firstname'],
							'@form[email]':self.config['portal']['email'],
							'@form[submit]':''})
