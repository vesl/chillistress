#!/usr/bin/python
import cstaps
import config
import sys


config=config.get()

cstaps=cstaps.cstaps(config['tap-number'],config['bridge-name'])
#cstaps.clean()
cstaps.create()
cstaps.bind()
cstaps.uptaps()
cstaps.getmac()
cstaps.setip()

#import cshttp
#cshttp=cshttp.cshttp()
#res=cshttp.request('GET','http://www.google.fr','10.1.0.1')
#print(res)
