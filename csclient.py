#!/usr/bin/python
import cshttp
import csshell
import cshtml
import err
import btools
import urllib.parse

class csclient:
	def __init__(self,tap,instdns,instip,instuamport,instssid,instnas):
		self.cshttp=cshttp.cshttp()
		self.csshell=csshell.csshell()
		self.cshtml=cshtml.cshtml()
		self.ip=tap['ip']
		self.mac=tap['mac']
		self.instdns=instdns
		self.instip=instip
		self.instuamport=instuamport
		self.instssid=instssid
		self.instnas=instnas
		self.instmac=self.getinstmac()
		self.challenge=btools.randmd5()
		self.md=btools.randmd5()

	def getinstmac(self):
		self.csshell.sh('/bin/ping -c 1 {}'.format(self.instip))
		mac=self.csshell.sh('sh/getMacFromIP.sh {}'.format(self.instip))
		if mac['err']: err.crit('csclient_mac','IP:{}'.format(self.instip))
		return mac['out'].replace('\n','')

	def chillipass(self):
		notyet="http://{}/?res=notyet&uamip={}&uamport={}&challenge={}&called={}&mac={}&ip={}&ssid={}&nasid={}&sessionid=585d4fe600000fb0&ssl=https%3a%2f%2fchilli.vipnetwork.fr%3a4990%2f&userurl=&md={}".format(self.instdns,self.instip,self.instuamport,self.challenge,self.instmac,self.mac,self.ip,self.instssid,self.instnas,self.md)
		err.log('Call url {}'.format(notyet))
		req=self.cshttp.get(notyet,self.ip)
		self.cshtml.check='checkIfChilliPortal'
		self.cshtml.feed(req['data'])
		if self.cshtml.result is False: err.warn('csclient_portal','Status : {}'.format(req['status']))
		else:
			err.log('Catched by portal : {}'.format(self.ip))			
			err.log(req['data'])
			params = urllib.parse.urlencode({'@form[type]':self.portaltype,
							'@form[login]':self.portallogin,
							'@form[password]':self.portalpassword,
							'@form[uamip]':self.instip,
							'@form[uamport]':self.instuamport,
							'@form[challenge]':self.challenge,
							'@form[nasid]':self.instnas,
							'@form[mac]':self.mac,
							'@form[ip]':self.ip,
							'@form[md]':self.md,
							'@form[userurl]':'',
							'@form[termOfUse]':'true',
							'@form[lastname]':self.portallastname,
							'@form[firstname]':self.portalfirstname,
							'@form[email]':self.portalemail,
							'@form[submit]':''})
