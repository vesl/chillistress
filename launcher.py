#!/usr/bin/python
import csconfig
import cstaps
import cshttp
import sys


config=csconfig.get()
cstaps=cstaps.cstaps(config['tap-number'],config['bridge'])
cshttp=cshttp.cshttp()

cstaps.clean()
cstaps.create()
cstaps.bind()
cstaps.uptaps()
cstaps.getmac()
cstaps.setip()
taps = cstaps.gettaps()

res=cshttp.request('GET','http://www.google.fr','10.1.0.1')
print(res)
