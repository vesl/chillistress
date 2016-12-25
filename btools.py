#!/usr/bin/python

import hashlib
import random

def tryutf8(s):
	try:
		return s.decode('utf-8')		
	except :
		return s
def md5(s):
	m = hashlib.md5(s)
	return m.hexdigest()

def rand(s,e):
	random.seed()
	return random.randint(s,e)

def randmd5():
	i = rand(0,1000000000000)
	s = str(i).encode('utf-8')
	return md5(s)
