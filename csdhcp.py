#!/usr/bin/python

import binascii
import socket
import random
import struct
import err 

class csdhcp:
	def __init__(self,mac):
		self.mac = bytes.fromhex(mac.replace(':',' '))
		self.transaction_id = self.trans_id()

	def trans_id(self):
		transaction_id=b''
		for i in range(4):
			t = random.randint(0, 255)
			transaction_id+= struct.pack('!B', t)
		return transaction_id

	def packet(self):
		boot_req=b'\x01'
		ethernet=b'\x01'
		addr_len=b'\x06'
		hops=b'\x00'
		sec_elapsed=b'\x00\x00'
		broadcast=b'\x80\x00'
		null_ip=b'\x00' * 4
		hw_addr_padd=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		hostname=b'\x00' * 67
		boot_file=b'\x00' * 125
		cookie=b'\x63\x82\x53\x63'
		option_discover=b'\x35\x01\x01'
		option_client_id=b'\x3d\x06'+self.mac
		option_params_limit=b'\x37\x03\x03\x01\x06'
		option_end=b'\xff'
		return boot_req+ethernet+addr_len+hops+self.transaction_id+sec_elapsed+broadcast+null_ip+null_ip+null_ip+null_ip+self.mac+hw_addr_padd+hostname+boot_file+cookie+option_discover+option_client_id+option_params_limit+option_end

	def request(self):
		dhcp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		dhcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
		try : 
			dhcp_sock.bind(('',68))
		except Exception as e:
			err.crit('csdhcp_bind',e)
		dhcp_sock.sendto(self.packet(),('255.255.255.255',67))
		return True
