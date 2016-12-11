#!/usr/bin/python
import cstaps
import sys

cstaps=cstaps.cstaps(10000,'br0')
#cstaps.clean()
#cstaps.create()
#cstaps.bind()
#cstaps.uptaps()
cstaps.getmac()
cstaps.setip()

#import cshttp
#cshttp=cshttp.cshttp()
#res=cshttp.request('GET','http://www.google.fr','10.1.0.1')
#print(res)
