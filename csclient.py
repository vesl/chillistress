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
		self.urllist=['http://heeeeeeeey.com/','http://thatsthefinger.com/','http://cant-not-tweet-this.com/','http://weirdorconfusing.com/','http://eelslap.com/','http://www.staggeringbeauty.com/','http://burymewithmymoney.com/','http://endless.horse/','http://www.fallingfalling.com/','http://just-shower-thoughts.tumblr.com/','http://ducksarethebest.com/','http://www.trypap.com/','http://www.republiquedesmangues.fr/','http://www.movenowthinklater.com/','http://www.partridgegetslucky.com/','http://www.rrrgggbbb.com/','http://beesbeesbees.com/','http://www.sanger.dk/','http://www.koalastothemax.com/','http://www.everydayim.com/','http://www.leduchamp.com/','http://www.haneke.net/','http://r33b.net/','http://randomcolour.com/','http://cat-bounce.com/','http://www.sadforjapan.com/','http://www.taghua.com/','http://chrismckenzie.com/','http://hasthelargehadroncolliderdestroyedtheworldyet.com/','http://ninjaflex.com/','http://iloveyoulikeafatladylovesapples.com/','http://ihasabucket.com/','http://corndogoncorndog.com/','http://www.ringingtelephone.com/','http://www.pointerpointer.com/','http://imaninja.com/','http://willthefuturebeaweso.me/','http://www.ismycomputeron.com/','http://www.nullingthevoid.com/','http://www.muchbetterthanthis.com/','http://www.ouaismaisbon.ch/','http://www.yesnoif.com/','http://iamawesome.com/','http://www.pleaselike.com/','http://crouton.net/','http://corgiorgy.com/','http://www.electricboogiewoogie.com/','http://www.wutdafuk.com/','http://unicodesnowmanforyou.com/','http://www.crossdivisions.com/','http://tencents.info/','http://intotime.com/','http://leekspin.com/','http://minecraftstal.com/','http://www.patience-is-a-virtue.org/','http://whitetrash.nl/','http://www.theendofreason.com/','http://zombo.com','http://pixelsfighting.com/','http://baconsizzling.com/','http://isitwhite.com/','http://onemillionlols.com/','http://www.omfgdogs.com/','http://oct82.com/','http://semanticresponsiveillustration.com/','http://chihuahuaspin.com/','http://potato.io/','http://www.blankwindows.com/','http://www.biglongnow.com/','http://dogs.are.the.most.moe/','http://tunnelsnakes.com/','http://www.infinitething.com/','http://www.trashloop.com/','http://www.ascii-middle-finger.com/','http://www.coloursquares.com/','https://annoying.dog/','http://spaceis.cool/','https://thebigdog.club/']

	def getinstmac(self):
		#self.csshell.sh('/bin/ping -c 1 {}'.format(self.config['instance']['ip']))
		mac=self.csshell.sh('sh/getMacFromIP.sh {}'.format(self.config['instance']['ip']))
		if mac['err']: err.crit('csclient_mac','IP:{}'.format(self.config['instance']['ip']))
		return mac['out'].replace('\n','')

	def chillipass(self):
		init = "http://gratuit.vipnetwork.fr"
		req=self.cshttp.get(init,self.config['client']['ip'],port=3990)
		if req['status'] == 302 :
			err.log('Client {} Catched by portal'.format(self.config['client']['ip']))
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

			req=self.cshttp.get(notyet,self.config['client']['ip'])
			err.log('Call notyet {}'.format(notyet))
			
			login="{}=login&type={}&uamip={}&uamport={}&challenge={}&nasid={}&mac={}&ip={}&md={}&login={}&password={}&lastname={}&firstname={}&email={}&userurl={}&nolayout=no".format(self.domain,self.config['portal']['type'],self.uamip,self.uamport,self.challenge,self.nasid,self.config['client']['mac'],self.config['client']['ip'],self.md,self.config['portal']['login'],self.config['portal']['password'],self.config['portal']['lastname'],self.config['portal']['firstname'],self.config['portal']['email'],self.userurl)
			req=self.cshttp.get(login,self.config['client']['ip'])
			err.log('Call login {}'.format(login))

			logon=req['data'].replace(':3990','')
			req=self.cshttp.get(logon,self.config['client']['ip'],port=3990)
			err.log('Call logon {}'.format(logon))
			if req['data'].split('?res=')[1][0:7] == "success" : 
				err.log('Client {} connected'.format(self.config['client']['ip']))
				return True
			else : 
				err.log('Client {} failed to connect'.format(self.config['client']['ip']))
				err.crit('csclient_logon','IP:{} Result logon:{}'.format(self.config['instance']['ip'],req['data']))

	def getrandomurl(self):
		i = btools.rand(0,len(self.urllist)-1)
		req=self.cshttp.get(self.urllist[i],self.config['client']['ip'])
		if req['status'] != 200 : err.warn('csclient_urllist_bad',self.urllist[i])
		else : err.log('Client {} checked url {}'.format(self.config['client']['ip'],self.urllist[i]))		
