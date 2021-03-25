#!/usr/bin/python2

from socket import *

sock=socket(AF_INET, SOCK_DGRAM)
sock.bind(('', 12345))
msg, client = sock.recvfrom(1024)
print(msg.decode(), client)
sock.close()