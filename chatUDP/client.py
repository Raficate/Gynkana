#!/usr/bin/python3

from socket import *

sock = socket(AF_INET, SOCK_DGRAM)
sock.sendto("hello".encode()), ('localhost', 12345))
sock.close()
