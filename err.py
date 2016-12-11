#!/usr/bin/python
def warn(code,detail):
	print("WARN -> err: {}. Detail: {} ".format(join(code),detail))

def crit(code,detail):
	print("CRIT -> err: {}. Detail: {} ".format(join(code),detail))
	exit(3)

def log(msg):
	print("LOG -> {}".format(msg))

def join(code):
	err = {
		'cshttp_connect':"Can't connect to host",
		'cshttp_protocol':"Protocol not allowed",
		'cshttp_invalid_url':"Invalid URL",
		'cshttp_method':"Invalid method",
		'cshttp_request':"Can't request",
		'csshell_bad_bin':"That bin is not allowed",
		'csshell_kill_not_found':"Can't find process",
		'cstaps_too_much_taps':"Calm down, there is too much taps",
		'cstaps_create':"Can't create tap",
		'cstaps_clean':"Can't clean tap",
		'cstaps_mac':"Can't get mac of tap",
		'cstaps_bind':"Cant bind tap to br",
		'cstaps_up':"Cant up tap",
	}
	return err[code]
