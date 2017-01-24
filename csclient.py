#!/usr/bin/python
import cshttp
import csshell
import cshtml
import err
import btools

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
		self.csshell.sh('/bin/ping -c 1 {}'.format(self.config['instance']['ip']))
		mac=self.csshell.sh('sh/getMacFromIP.sh {}'.format(self.config['instance']['ip']))
		if mac['err']: err.crit('csclient_mac','IP:{}'.format(self.config['instance']['ip']))
		return mac['out'].replace('\n','')

	def chillipass(self):
		init = "http://gratuit.vipnetwork.fr"
		req=self.cshttp.get(init,self.config['client']['ip'],port=3990)
        if req['status'] == 302 :
            notyet=req['data'].split('/www.coova.html/')[1]
		notyet="http://{}/?res=notyet&uamip={}&uamport={}&challenge={}&called={}&mac={}&ip={}&ssid={}&nasid={}&sessionid=585d4fe600000fb0&ssl=https%3a%2f%2fchilli.vipnetwork.fr%3a4990%2f&userurl=&md={}".format(self.config['instance']['domain'],self.config['instance']['ip'],self.config['instance']['uamport'],self.config['client']['challenge'],self.config['instance']['mac'],self.config['client']['mac'],self.config['client']['ip'],self.config['instance']['ssid'],self.config['instance']['nasid'],self.config['client']['md'])
		err.log('Call url {}'.format(notyet))
		req=self.cshttp.get(notyet,self.config['client']['ip'])
		self.cshtml.check='checkIfChilliPortal'
		self.cshtml.feed(req['data'])
		if self.cshtml.result is False: err.warn('csclient_portal','Status : {}'.format(req['status']))
		else:
			err.log('Catched by portal : {}'.format(self.config['client']['ip']))			
			login="http://{}/?res=login&type={}&uamip={}&uamport={}&challenge={}&nasid={}&mac={}&ip={}&md={}&login={}&password={}&lastname={}&firstname={}&email={}&userurl=''&nolayout=no".format(self.config['instance']['domain'],self.config['portal']['type'],self.config['instance']['ip'],self.config['instance']['uamport'],self.config['client']['challenge'],self.config['instance']['nasid'],self.config['client']['mac'],self.config['client']['ip'],self.config['client']['md'],self.config['portal']['login'],self.config['portal']['password'],self.config['portal']['lastname'],self.config['portal']['firstname'],self.config['portal']['email'])
			err.log('Call url {}'.format(login))
			req=self.cshttp.get(login,self.config['client']['ip'])
			err.log(req['data'])
