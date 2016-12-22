#!/usr/bin/python

import csshell
import csdhcp
import err
import time

class cstaps:

	def __init__(self,number,br):
		if int(number) > 10000 : err.crit('cstaps_too_much_taps',number)
		self.csshell=csshell.csshell()
		self.br = br
		self.taps = []
		while number > 0:
			self.taps.append({'name':'tap{}'.format(number)})
			number-=1
	def gettaps(self):
		return self.taps

	def getactivetaps(self):
		taps = self.csshell.sh('sh/getActiveTaps.sh')['out'].split('\n')
		return taps

	def create(self):
		for tap in self.taps:
			create=self.csshell.sh('/usr/sbin/tunctl -u root -t {}'.format(tap['name']))
			if create['err'] : err.crit('cstaps_create','Tap : {} Err: {}'.format(tap['name'],create['err']))
			else : err.log('Created tap {}'.format(tap['name']))
		return True

	def bind(self):
		for t in self.taps: 
			tap = {}
			tap.update(t)
			bind = self.csshell.sh('/sbin/brctl addif {} {}'.format(self.br,tap['name']))
			if bind['err'] : err.warn('cstaps_bind','Br : {} Tap : {} Err : {}'.format(self.br,tap['name'],bind['err']))
			else : err.log('Added nic {} to br {}'.format(tap,self.br))
		return True

	def uptaps(self):
		for tap in self.taps:
			up = self.csshell.sh('/sbin/ifconfig {} up'.format(tap['name']))
			if up['err'] : err.warn('cstaps_up','Tap : {} Err : {}'.format(tap['name'],up['err']))
		return True

	def getmac(self):
		self.taps=[]
		macs = self.csshell.sh('sh/getMac.sh')
		if macs['err'] : err.crit('cstaps_mac',macs['err'])
		macs = macs['out'].split(' ')
		for i in range(len(macs)):
			if macs[i][0:3] == 'tap': self.taps.append({'name':macs[i],'mac':macs[i+4]})
		return True

	def setip(self):
		for tap in self.taps:
			dhcp=csdhcp.csdhcp(tap['mac'])
			ip=dhcp.request()
			tap.update({'ip':ip})
			assign = self.csshell.sh('/sbin/ip addr add {}/32 dev {}'.format(tap['ip'],tap['name']))
			err.log('Set ip {} to dev {}'.format(tap['ip'],tap['name']))
			if assign['err'] : err.crit('cstaps_ip_assign','Tap : {} IP : {}'.format(tap['name'],tap['ip']))
		return True

	def clean(self):
		for tap in self.getactivetaps():
			clean = self.csshell.sh('/usr/sbin/tunctl -u root -d {}'.format(tap))
			if clean['err'] : err.warn('cstaps_clean','Taps : {} Err : {}'.format(tap,clean['err']))
		return True
