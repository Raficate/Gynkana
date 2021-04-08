#!/usr/bin/python3

from socket import *

## RETO 0 ##

def reto0():
    # Parte 1, conexión con el server rick:2000
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('rick', 2000))
    sock.recv(1024).decode()
    
    # Parte 2, enviamos al server el nombre de usuario de thehub
    sock.send(username.encode())
    
    msg = sock.recv(1024).decode()
    # print(msg)
    msg= msg.split(':')[1]
    idmsg = msg.split('\n')[0]

    sock.close()

    return idmsg

## RETO 1 ##

def reto1(id0):
    # Paso por parámetros el id obtenido en el reto 0
    # Parte 1, creamos un server UDP local que escuche desde el puerto 3437
    udpServerPort = int(3437)
    udpServerSock = socket(AF_INET, SOCK_DGRAM)
    udpServerSock.bind(('', udpServerPort))

    # Parte 2, creamos un cliente UDP y enviamos a rick:4000 el puerto en el que tenemos el server UDP y el id0 
    udpClientSock = socket(AF_INET, SOCK_DGRAM)
    msg = str(udpServerPort)+" "+id0
    udpClientSock.sendto(msg.encode(), ('rick', 4000))
    

    # Parte 3, nuestro server recibe msg de vuelta y envía respuesta al servidor que la ha mandado 
    serverMsg, client = udpServerSock.recvfrom(1024)
    print(serverMsg.decode())
    id0upper = id0.upper()
    print("id0 to upper: "+id0upper)
    msg2 = str(udpServerPort)+" "+id0upper
    udpClientSock.sendto(id0upper.encode(), ('rick', client[1]))
    serverMsg2 = udpServerSock.recvfrom(1024)
    msg = serverMsg2[0].decode()
    # print(msg)
    
    msg= msg.split(':')[1]
    idmsg = msg.split('\n')[0]

    udpClientSock.close()
    udpServerSock.close()

    return idmsg

## RETO 2 ##

def reto2(id1):

    tcpSock = socket(AF_INET, SOCK_STREAM)
    tcpSock.connect(('rick', 3002))



## MAIN ##
username = "mystifying_bhabha"
id0 = reto0()
print("ID Reto 0: "+id0)
id1 = reto1(id0)
print("ID Reto 1: "+id1)
