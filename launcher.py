#!/usr/bin/python
import csconfig
import cstaps
import cshttp
import csclient
import sys


config=csconfig.get()
cstaps=cstaps.cstaps(config['tap-number'],config['bridge'])

cstaps.clean()
cstaps.create()
cstaps.bind()
cstaps.uptaps()
cstaps.getmac()
cstaps.setip()
taps = cstaps.gettaps()


for tap in taps:
	csclient=csclient.csclient(tap,config['instance-dns'],config['instance-ip'],config['instance-uamport'],config['instance-ssid'],config['instance-nasid'])
	portal = csclient.chillipass()
