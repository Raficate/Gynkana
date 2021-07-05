#!/usr/bin/python3

from socket import *
import sys
import hashlib
import base64
import struct
import array
import _thread
import threading
from typing import Mapping
import urllib.request
from urllib import request

import json
import time


postmsg = ""

## Funciones externas ##
def isPalindrome(word): 
    if word.isdigit():
        return False
    else:
        word = word.lower() 
        return word == word[::-1] 

def searchPalindrome(msg):
    splitMsg = msg.split()        
    for word in splitMsg:
        if len(word)>1:
            if isPalindrome(word):
                return word
    return -1

def reverseWords(myString):
    reverseString = ""
    splitString = myString.split()
    for word in splitString:
        if word.isdigit():
            reverseString = reverseString + " " + word
        else:
            reverseString = reverseString + " " + word[::-1]
    return reverseString

def cksum(pkt): #https://bitbucket.org/DavidVilla/inet-checksum/src/master/inet_checksum.py
    # type: (bytes) -> int
    if len(pkt) % 2 == 1:
        pkt += b'\0'
    s = sum(array.array('H', pkt))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    s = ~s

    if sys.byteorder == 'little':
        s = ((s >> 8) & 0xff) | s << 8

    return s & 0xffff

def handle(sock, client, n): #https://docs.python.org/2/library/urllib.html
    print(f"Client connected: {n} {client}")

    req = sock.recv(65535).decode()
    if(req.find('POST') == -1):
        rfc = req.splitlines()[0].split(' ')[1]

        print(f"Client petition {n} received")
        completeurl = url+rfc

        get = request.Request(completeurl)
        response = request.urlopen(get)
        data = response.read()
        # print(data.decode())
        # sock.sendall('HTTP/1.1 200 OK\n\n'.encode() + data)

        # print(f"Client request {n} downloaded and reedirected")
    
    else:
        data = ""
        print(f"Client {n} contains a POST request")
        global postmsg
        postmsg = req
        # sock.sendall(('HTTP/1.1 200 OK\n\n').encode())

    sock.sendall('HTTP/1.1 200 OK\n\n'.encode() + data)

    # sock.close

    # while 1:
    # data = sock.recv(1024)
    # # if not data:
    # #     break
    # # print("Data: "+data.decode())
    # rfc = data.split()[1].decode()
    # completeurl = url+rfc

    # get = requests.Request()
    # r = requests.get(completeurl)



    # endpoint = endpoint.decode()
    # print("Endpoint: "+rfc)
    # download = urllib.request.urlopen(completeurl)
    # print(r.content)
    # response = completeurl.read().decode()
    # print(r)
    # print(r.headers)
    # requests.post(completeurl, r)
    # print(f"Client disconnected: {n} {client}")

    

def chamber0():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('rick', 2000))
    sock.recv(1024).decode()
    sock.send(username.encode())
    msg = sock.recv(1024).decode()
    msg= msg.split(':')[1]
    idmsg = msg.split('\n')[0]

    sock.close()

    return idmsg

def chamber1(id0):
    port = int(3437)
    udpserver = socket(AF_INET, SOCK_DGRAM)
    udpserver.bind(('', port))

    udpclient = socket(AF_INET, SOCK_DGRAM)
    msg = str(port)+" "+id0
    udpclient.sendto(msg.encode(), ('rick', 4000))

    serverMsg, client = udpserver.recvfrom(1024)
    id0upper = id0.upper()
    msg2 = str(port)+" "+id0upper
    udpclient.sendto(id0upper.encode(), ('rick', client[1]))
    serverMsg2, client2 = udpserver.recvfrom(1024)
    msg = serverMsg2.decode()
    msg= msg.split(':')[1]
    idmsg = msg.split('\n')[0]

    udpclient.close()
    udpserver.close()

    return idmsg

def chamber2(id1):

    tcpSock = socket(AF_INET, SOCK_STREAM)
    tcpSock.connect(('rick', 3002))

    msg = ""
    cont = 0
    while 1:
        data = tcpSock.recv(1024).decode()
        index = data.find("that's it")
        if index == -1:
            msg = msg + data
        else:
            data = data[:index]
            msg = msg + data
            break
    
    cont = 0
    for c in msg:
        if c == ' ' or c == '\n':
            cont = cont + 1

    # print("Total words: "+ str(cont))
    sendMsg = id1+ " " +str(cont)
    tcpSock.sendall(sendMsg.encode())

    check = ""
    while 1:
        data = ""
        data = tcpSock.recv(1024).decode()
        if data == "":
            break
        check = data
        
    check= check.split(':', 1)[1]
    idmsg = check.split('\n')[0]
    tcpSock.close()

    return idmsg

def chamber3(id2):
    tcpsock = socket(AF_INET, SOCK_STREAM)
    tcpsock.connect(('rick', 6500))
    
    myStr = ""

    while 1:

        msg = tcpsock.recv(1024).decode()
        if msg == "":
            break
        
        result = searchPalindrome(msg)
        if result==-1:
            myStr = myStr + msg
        else:
            ulti = msg.split(result)
            myStr = myStr + ulti[0]
            break
    
    reverseStr = reverseWords(myStr)

    enviar = id2 + " " + reverseStr + " " + "--" 
    tcpsock.send(enviar.encode())
    msg = tcpsock.recv(1024).decode()
    msg= msg.split(':', 1)[1]
    idmsg = msg.split('\n')[0]
    tcpsock.close()
    return idmsg  

def chamber4(id3):
    tcpsock = socket(AF_INET, SOCK_STREAM)
    tcpsock.connect(('rick', 9000))
    tcpsock.send(id3.encode())
    
    continues = True
    firstMsg = True
    fullMsg = ""
    while continues:
        data = tcpsock.recv(1024)

        if firstMsg:
            msg = data.split(b':', 1)
            size = int(msg[0].decode())
            fullMsg = msg[1]
            firstMsg = False
        else:
            fullMsg = fullMsg + data
            if int(len(fullMsg)) == size:
                continues = False

    sumMD5 = hashlib.md5(fullMsg).digest()

    tcpsock.send(sumMD5)
    resp = tcpsock.recv(2048).decode()
    idmsg = resp.split(':', 1)[1]
    idmsg = idmsg.split('\n')[0]

    tcpsock.close()
    
    return idmsg

def chamber5(id4):
    
    udpsock = socket(AF_INET, SOCK_DGRAM)

    headerFormat = '!3sBHHH'
    payload = base64.b64encode(id4.encode())
    header = struct.pack(headerFormat, b'WYP', 0, 0, 0, 1)
    packet = header + payload

    checksum = cksum(packet)
    header = struct.pack(headerFormat, b'WYP', 0, 0, checksum, 1)
    packet = header + payload

    udpsock.sendto(packet, ('rick', 6000))
    data, server = udpsock.recvfrom(2048)

    lenData = str(len(data)-8)
    formatResponse = '!3sBHH'+lenData+'s'
    
    msg = struct.unpack(formatResponse, data)

    msg4 = base64.b64decode(msg[4])

    msg4 = msg4.decode()
    idmsg = msg4.split(':', 1)[1]
    idmsg = idmsg.split('\n')[0]

    udpsock.close()

    return idmsg

def chamber6(id5):

    port = 8614

    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(('', port))
    sock.listen()
    
    client = socket(AF_INET, SOCK_STREAM)
    msg = id5+" "+str(port)
    client.connect(('rick', 8002))
    client.send(msg.encode())
    
    errmsg = client.recv(1024) #Recibe el mensaje de error

    n = 0 
    
    while 1:
        (childsocket, address) = sock.accept()
        n += 1
        x = threading.Thread(target=handle, args=(childsocket, address, n))
        # x.daemon = True
        x.start()
        if threading.active_count() > 10:
            x.join()
        # childsocket.close()

    msg = sock.recv(1024).decode()
        #https://realpython.com/intro-to-python-threading/
    print(msg)

    sock.close()


username = "mystifying_bhabha"
url = "http://rick:81/rfc"


id0 = chamber0()
print("Chamber's 0 ID: " +id0)
id1 = chamber1(id0)
print("Chamber's 1 ID: " +id1)
id2 = chamber2(id1)
print("Chamber's 2 ID: " +id2)
id3 = chamber3(id2)
print("Chamber's 3 ID: " +id3)
id4 = chamber4(id3)
print("Chamber's 4 ID: " +id4)
id5 = chamber5(id4)
print("Chamber's 5 ID: " +id5)

chamber6(id5)


