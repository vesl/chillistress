#!/usr/bin/python

import subprocess
import shlex
import err
import btools

class csshell:
	def check_bin(self,bin):
		allowed_bins={
			'/sbin/ip':True,
			'/sbin/ifconfig':True,
			'/sbin/brctl':True,
			'/bin/ps':True,
			'/bin/kill':True,
			'/usr/sbin/tunctl':True,
			'sh/getMac.sh':True,
			'sh/getTaps.sh':True,
			'sh/getMacFromIP.sh':True,
		}
		try:
			return allowed_bins[bin]
		except KeyError:
			err.crit('csshell_bad_bin','{}'.format(bin))
			return False

	def sh(self,raw_cmd):
		self.cmd=shlex.split(raw_cmd)	
		if not self.check_bin(self.cmd[0]) : return False
		err.log('Execution de la commande : {}'.format(self.cmd))
		proc=subprocess.Popen(self.cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		ret=proc.returncode
		try:
			(out,error)=proc.communicate(timeout=20)
		except subprocess.TimeoutExpired:
			error='Timeout: {}'.format(self.cmd)
			out = error
			ret = -1
		return {'out':btools.tryutf8(out),'err':btools.tryutf8(error),'ret':ret}

	def kill(self,process):
		found = False
		ps = self.sh('/bin/ps aux')
		procs = ps['out'].split('\n')[1:-1]
		for proc in procs:
			proc = list(p for p in proc.split(' ') if p is not '')
			search = list(s for s in proc[9:] if s  == process)
			if len(search) > 0 and search[0] == process :
				kill = self.sh('/bin/kill {}'.format(proc[1]))
				if kill['err'] : err.crit('csshell_kill','proc : {} , pid : {}'.format(search[0],proc[1]))
				else : found = True
		if not found : 
			err.warn('csshell_kill_not_found','proc : {}'.format(process))
			return False
		return True
