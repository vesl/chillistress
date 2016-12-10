#!/usr/bin/python
import cstaps
import sys
#cstaps=cstaps.cstaps('50','br0',{'start':'10.1.0.100','network':'10.1.0.0/16'})
#cstaps.bind('unbind')
#cstaps.clean()
#cstaps.create()
#cstaps.bind('bind')
#cstaps.setip()
#cstaps.uptaps()
import cshttp
cshttp=cshttp.cshttp()
res=cshttp.request('GET','http://www.google.fr','10.1.0.1')
print(res)
