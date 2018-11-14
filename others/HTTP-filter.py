#!/usr/bin/env python
import os
from scapy.all import *
from scapy.layers import http
from netfilterqueue import NetfilterQueue

def packetCheck(packet):
    payload = packet.get_payload()
    pkt = IP(payload)
    if pkt[TCP].flags == 'PA':
        http_layer = pkt.getlayer(http.HTTPRequest)
        http_layer = http_layer.Path
        ip_layer = pkt.getlayer(IP)
        ip_layer =  ip_layer.src
        print "{} has requested {}".format(ip_layer, http_layer)
        # login page
        if str(http_layer) == '/':
            print "[!] BAD REQUEST"
            packet.drop()
        # camera center
        elif str(http_layer) == '/decoder_control.cgi?command=25&user=TurnCamera&pwd=JMfe894':
            print "[!] BAD REQUEST"
            packet.drop()
        # IR on
        elif str(http_layer) == '/decoder_control.cgi?command=95&user=TurnCamera&pwd=JMfe894':
            print "[!] BAD REQUEST"
            packet.drop()
        # IR off
        elif str(http_layer) == '/decoder_control.cgi?command=94&user=TurnCamera&pwd=JMfe894':
            print "[!] BAD REQUEST"
            packet.drop()
        # preset go
        elif str(http_layer) == '/decoder_control.cgi?command=31&user=TurnCamera&pwd=JMfe894':
            print "[!] BAD REQUEST"
            packet.drop()
        # video refresh
        elif str(http_layer) == '/decoder_control.cgi?command=30&user=TurnCamera&pwd=JMfe894':
            print "[!] BAD REQUEST"
            packet.drop()
        else:
            packet.accept()
    else:
        packet.accept()

def main():
    os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
    os.system('iptables -A FORWARD -p tcp --destination-port 80 -j NFQUEUE --queue-num 1')
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, packetCheck)

    try:
        print "[+] Filter started"
        nfqueue.run()

    except KeyboardInterrupt:
        os.system('echo 0 > /proc/sys/net/ipv4/ip_forward')
        os.system('iptables -F')
        os.system('iptables -Z')
        nfqueue.unbind()
        


if __name__ == '__main__':
    main()

