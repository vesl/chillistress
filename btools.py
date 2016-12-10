#!/usr/bin/python
def tryutf8(s):
	try:
		return s.decode('utf-8')		
	except :
		return s
