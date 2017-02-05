#!/usr/bin/python
import cshttp
import csshell
import cshtml
import urllib
import err
import btools

class csclient:
	def __init__(self,tap,config):
		self.cshttp=cshttp.cshttp()
		self.csshell=csshell.csshell()
		self.cshtml=cshtml.cshtml()
		self.config=config
		self.config.update({'client':{}})
		self.config['client'].update({'mac':tap['mac'].upper().replace(':','-')})
		self.config['client'].update({'ip':tap['ip']})
		self.config['client'].update({'challenge':btools.randmd5()})
		self.config['client'].update({'md':btools.randmd5()})
		self.config['instance'].update({'mac':self.getinstmac()})

	def getinstmac(self):
		#self.csshell.sh('/bin/ping -c 1 {}'.format(self.config['instance']['ip']))
		mac=self.csshell.sh('sh/getMacFromIP.sh {}'.format(self.config['instance']['ip']))
		if mac['err']: err.crit('csclient_mac','IP:{}'.format(self.config['instance']['ip']))
		return mac['out'].replace('\n','')

	def chillipass(self):
		init = "http://gratuit.vipnetwork.fr"
		req=self.cshttp.get(init,self.config['client']['ip'],port=3990)
		if req['status'] == 302 :
			err.log('Client {} Catched by portal')
			err.log(req['data'])
			try :
				notyet=urllib.parse.unquote(req['data'].split('?loginurl=')[1])
			except Exception as e:
				err.crit('csclient_notyet','Url : {} Detail : {}'.format(req['data'],e))

			params=notyet.split('&')
			self.domain=params[0].split('=')[0]
			self.uamip=params[1].split('=')[1]
			self.uamport=params[2].split('=')[1]
			self.challenge=params[3].split('=')[1]
			self.called=params[4].split('=')[1]
			self.mac=self.config['client']['mac']
			self.ip=params[6].split('=')[1]
			self.ssid=params[7].split('=')[1]
			self.nasid=params[8].split('=')[1]
			self.sessionid=params[9].split('=')[1]
			self.ssl=params[10].split('=')[1]
			self.userurl=params[11].split('=')[1]
			self.md=params[12].split('=')[1]

			notyet=notyet.replace('10.1.0.254',self.config['client']['ip']).replace('52-54-00-32-06-D3',self.config['client']['mac'])
			req=self.cshttp.get(notyet,self.config['client']['ip'])
			err.log('Call notyet {}'.format(notyet))
			
			login="{}=login&type={}&uamip={}&uamport={}&challenge={}&nasid={}&mac={}&ip={}&md={}&login={}&password={}&lastname={}&firstname={}&email={}&userurl={}&nolayout=no".format(self.domain,self.config['portal']['type'],self.uamip,self.uamport,self.challenge,self.nasid,self.config['client']['mac'],self.config['client']['ip'],self.md,self.config['portal']['login'],self.config['portal']['password'],self.config['portal']['lastname'],self.config['portal']['firstname'],self.config['portal']['email'],self.userurl)
			req=self.cshttp.get(login,self.config['client']['ip'])
			err.log('Call login {}'.format(login))

			logon=req['data'].replace(':3990','')
			req=self.cshttp.get(logon,self.config['client']['ip'],port=3990)
			err.log('Call logon {}'.format(logon))
			err.log(req['data'])
