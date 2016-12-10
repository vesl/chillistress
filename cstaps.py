#!/usr/bin/python

import csshell
import csip
import err
import time

class cstaps:

	def __init__(self,number,br,ip):
		self.csshell=csshell.csshell()
		self.csip=csip.csip()
		if int(number) > 10000 : err.crit('cstaps_too_much_taps',number)
		self.number = number
		self.br = br
		self.ipstart = ip['start']
		self.network = ip['network']

	def create(self):
		taps = self.csshell.sh('multimac/create.sh {}'.format(int(self.number)-1))
		if taps['err'] and taps['err'][0:7] != "Timeout" : err.crit('cstaps_create',taps['err'])
		tapsready=self.taps()['number']
		while int(tapsready) != int(self.number):
			err.log('Creating taps : {} of {}'.format(tapsready,self.number))
			time.sleep(1)
			tapsready=self.taps()['number']
		return taps

	def bind(self,action):
		if action == 'bind': action = 'addif'
		elif action == 'unbind': action = 'delif'
		else : err.crit('cstaps_bad_bind_action',action)
		tapsup = self.taps()['names']
		for tap in tapsup: 
			bind = self.csshell.sh('/sbin/brctl {} {} {}'.format(action,self.br,tap))
			if bind['err'] : err.warn('cstaps_bind','{} {} {}'.format(action,self.br,tap))
			else : err.log('Added nic {} to br {}'.format(tap,self.br))
		return True

	def uptaps(self):
		taps = self.taps()['names']
		for tap in taps:
			up = self.csshell.sh('/sbin/ifconfig {} up'.format(tap))
			if up['err'] : err.warn('cstaps_up',tap)
		return True

	def setip(self):
		taps = self.taps()['names']
		pool = self.csip.getrange(self.ipstart,self.network,self.number)
		if len(taps) != len(pool) : err.crit('cstaps_number_ip','ip number : {} , taps number : {}'.format(len(pool),len(taps)))
		i = 0
		while i < len(taps):
			add = self.csshell.sh('/sbin/ip addr add {}/32 dev {}'.format(pool[i],taps[i]))
			if add['err'] : err.crit('cstaps_set_ip',add['err'])
			i+=1
		return True

	def clean(self):
		if not self.csshell.kill('./multimac/multimac') : 
			return False
			err.warn('cstaps_kill_multimac','./multimac/multimac')
		if not self.csshell.kill('multimac/create.sh') : 
			return False
			err.warn('cstaps_kill_multimac','multimac/create.sh')
		tapsready=self.taps()['number']
		while int(tapsready) != 0:
			err.log('Removing taps : {} until 0'.format(tapsready))
			time.sleep(1)
			tapsready=self.taps()['number']
		return True

	def taps(self):
		taps = []
		nics = self.csshell.sh('/bin/ls /proc/sys/net/ipv4/conf/')
		if nics['err'] : err.crit('cstaps_list_nics_up',nics['err'])
		for nic in nics['out'].split('\n'):
			if nic[0:3] == 'tap' : taps.append(nic)
		return {'names':taps,'number':len(taps)}
