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
		'csnetwork_bad_network':"This is not a valid network. Should be xxx.xxx.xxx.xxx/xx",
		'csnetwork_assign_ip':"Can't assign ip on nic",
		'cstaps_too_much_taps':"Calm down, there is too much taps",
		'cstaps_create':"Can't create taps",
		'cstaps_create_br':"Can't create bridge",
		'cstaps_kill_multimac':"Can't kill process multimac",
		'cstaps_list_nics_up':"Can't list nics in",
		'cstaps_bad_bind_action':"Bad action in bind arg should be bind or unbind",
		'cstaps_bind':"Cant bind tap to br",
		'cstaps_up':"Cant up tap",
		'cstaps_number_ip':"Not same lenght ip and taps",
		'cstaps_set_ip':"Can't set ip on tap",
		'csip_bad_network':"Can't deal with this network",
		'csip_ipstart_not_found':"Can't found ipstart",
	}
	return err[code]
