import ipaddress
import err

class csip:
	def getrange(self,ipstart,network,number):
		try:self.iprange=list(ipaddress.ip_network(network).hosts())
		except:err.crit('csip_bad_network',network)
		while str(self.iprange[0]) != str(ipstart):
			del self.iprange[0]
			if len(self.iprange) == 1 : 
				err.crit('csip_ipstart_not_found',ipstart)
		del self.iprange[int(number):]
		return self.iprange
