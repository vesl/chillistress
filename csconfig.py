#!/usr/bin/python
import configparer
import err

def errMissing(param,section):
	err.crit('csconfig_missing','Param : {}, in Section {} :'.format(param,section)

def load():
	config = configparser.ConfigParser()
	try :
		config.read('config.ini')
		sections = { 'system' : ['tap_number','bridge'],
				'instance' : ['ip','uamport','hostname','ssid','nasid'],
				'portal': ['type','login','password','lastname','firstname','email',user_url']
		}
		for section in section:
			if not config[section]: errMissing('all',section)
			else:
				for param in sections[section]:
					if not config[section][param]: errMissing(param,section)
		return config

	except Exception as e: 
		err.crit('csconfig_load','Err :{}'.format(e))
