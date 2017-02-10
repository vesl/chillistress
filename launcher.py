#!/usr/bin/python
import csconfig
import cstaps
import cshttp
import csclient
import sys


config=csconfig.load()
cstaps=cstaps.cstaps(int(config['system']['tap_number']),config['system']['bridge'])

cstaps.clean()
cstaps.create()
cstaps.bind()
cstaps.uptaps()
cstaps.getmac()
cstaps.setip()
taps = cstaps.gettaps()

for tap in taps:
	client=csclient.csclient(tap,config)
	portal = client.chillipass()
	client.getrandomurl()
