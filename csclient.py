#!/usr/bin/python
import cshttp
import csshell

class csclient:
	def __init__(self,tap,instdns,instip,instuamport,instssid,instnas):
		self.cshttp=cshttp.cshttp()
		self.csshell=csshell.csshell()
		self.ip=tap['ip']
		self.mac=tap['mac']
		self.instdns=instdns
		self.instip=instip
		self.instuamport=instuamport
		self.instssid=instssid
		self.instnas=instnas
		self.instmac=self.csshell.sh('sh/getMacFromIP.sh {}'.format(self.instip))['out'].replace('\n','')

	def pass(self):
		notyet="http://{}/?res=notyet&uamip={}&uamport={}&challenge=2652d8fdbf78c5b0344cb697681b9fe2&called={}&mac={}&ip={}&ssid={}&nasid={}&sessionid=585d4fe600000fb0&ssl=https%3a%2f%2fchilli.vipnetwork.fr%3a4990%2f&userurl=&md=B92FE22AFFB23EF2C135E93AC665B4E8".format(self.instdns,self.instip,self.instuamport,self.instmac,self.mac,self.ip,self.instssid,self.instnas)
		req=cshttp.get(notyet,self.ip)
		return req