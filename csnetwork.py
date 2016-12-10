#!/usr/bin/python

import ipaddress
import err
import csshell

class csnetwork:
	def parse_network(raw_network):
		try:
			return ipaddress.ip_address(raw_network)
		except:
			err.warn('csnetwork_bad_network','{}'.format(raw_network))
			return False

	def ipassign(nic,ip,netmask):
		assign=csshell.sh('ip addr add '+ip+'/'+netmask+' dev '+nic)
		if not assign.err : return True
		else :
			err.warn('csnetwork_assign_ip','{}/{} on {}'.format(ip,netmask,nic))
			return False
