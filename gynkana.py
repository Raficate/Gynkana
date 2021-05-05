#!/usr/bin/python3

from socket import *
import sys
import hashlib
import base64
import struct
import array

## Funciones externas ##
def esPalindromo(palabra): #Comprueba si la palabra que se le pasa por parámetro es un palindromo
    if palabra.isdigit():
        return False
    else:
        palabra = palabra.lower() 
        return palabra == palabra[::-1] 

def buscaPalindromo(mensaje):
    msgPartido = mensaje.split()        
    for palabra in msgPartido:
        if len(palabra)>1:
            if esPalindromo(palabra):
                return palabra
    return -1

def inviertePalabras(cadena):
    cadenaInversa = ""
    cadenaPartida = cadena.split()
    for palabra in cadenaPartida:
        if palabra.isdigit():
            cadenaInversa = cadenaInversa + " " + palabra
        else:
            cadenaInversa = cadenaInversa + " " + palabra[::-1]
    return cadenaInversa

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
    # print(serverMsg.decode())
    id0upper = id0.upper()
    # print("id0 to upper: "+id0upper)
    msg2 = str(udpServerPort)+" "+id0upper
    udpClientSock.sendto(id0upper.encode(), ('rick', client[1]))
    serverMsg2, client2 = udpServerSock.recvfrom(1024)
    msg = serverMsg2.decode()
    # print(msg)

    msg= msg.split(':')[1]
    idmsg = msg.split('\n')[0]

    udpClientSock.close()
    udpServerSock.close()

    return idmsg

## RETO 2 ##
def reto2(id1):

    # Parte 1, creación del cliente TCP 
    tcpSock = socket(AF_INET, SOCK_STREAM)
    tcpSock.connect(('rick', 3002))

    # Parte 2, crear una cadena de caracteres con todos los datos recibidos hasta recibir "that's all"
    msg = ""
    cont = 0
    while 1:
        datos = tcpSock.recv(1024).decode()
        # print(datos)
        index = datos.find("that's all")
        if index == -1:
            msg = msg + datos
        else:
            datos = datos[:index]
            msg = msg + datos
            break
    
    # print(msg)
    # Parte 3, contar las palabras que tiene la cadena
    cont = 0
    for c in msg:
        if c == ' ' or c == '\n':
            cont = cont + 1

    # print("Total palabras: "+ str(cont))
    # Parte 4 envio de codigo de Reto 1 más el número de palabras encontrado antes de la Flag
    msgEnvio = id1+ " " +str(cont)
    tcpSock.sendall(msgEnvio.encode())

    # Parte 5, recibir respuesta sobre como comenzar el Reto 3 y coger el identificador
    comprobacion = ""
    while 1:
        datos = ""
        datos = tcpSock.recv(1024).decode()
        if datos == "":
            break
        comprobacion = datos
        
    comprobacion= comprobacion.split(':', 1)[1]
    idmsg = comprobacion.split('\n')[0]
    tcpSock.close()
    return idmsg

## RETO 3 ##
def reto3(id2):
    # Parte 1, conectar con el servidor tcp rick:6500
    tcpsock = socket(AF_INET, SOCK_STREAM)
    tcpsock.connect(('rick', 6500))
    
    # Parte 2, recorre el mensaje palabra por palabra y comprueba donde está el palindromo
    cadena = ""
    cont = 0

    while 1:

        msg = tcpsock.recv(1024).decode()
        if msg == "":
            break
        
        result = buscaPalindromo(msg)
        if result==-1:
            cadena = cadena + msg
        else:
            ulti = msg.split(result)
            cadena = cadena + ulti[0]
            break
    
    # Parte 3, invierte la cadena de caracteres obtenida 
    cadenaInv = inviertePalabras(cadena)

    # Parte 4, crea el formato de cadena que nos pide para enviar, lo envia y reciba info del siguiente reto 
    enviar = id2 + " " + cadenaInv + " " + "--" 
    tcpsock.send(enviar.encode())
    msg = tcpsock.recv(1024).decode()
    # print(msg)
    msg= msg.split(':', 1)[1]
    idmsg = msg.split('\n')[0]
    tcpsock.close()
    return idmsg    

## RETO 4 ##
def reto4(id3):
    tcpsock = socket(AF_INET, SOCK_STREAM)
    tcpsock.connect(('rick', 9000))
    tcpsock.send(id3.encode())
    
    seguir = True
    primerMensaje = True
    msgCompleto = ""
    while seguir:
        data = tcpsock.recv(1024)

        if primerMensaje:
            msg = data.split(b':', 1)
            tamano = int(msg[0].decode())
            # print("Tamaño del archivo: "+str(tamano))
            # print("----------------")
            msgCompleto = msg[1]
            primerMensaje = False
        else:
            msgCompleto = msgCompleto + data
            # print("Tamaño de archivo calculado de momento: "+ str(len(msgCompleto)))
            if int(len(msgCompleto)) == tamano:
                # print("Fin de la cosa ")
                seguir = False
                # break

                
    # print("Tamaño archivo: "+ str(tamano))
    
    # print("Tamaño de archico calculado: "+str(tamMensaje))

    sumaMD5 = hashlib.md5(msgCompleto).digest()
    # print("Suma MD5: "+str(sumaMD5))

    tcpsock.send(sumaMD5)

    resp = tcpsock.recv(2048).decode()
    idmsg = resp.split(':', 1)[1]
    idmsg = idmsg.split('\n')[0]

    tcpsock.close()
    # print(resp)
    return idmsg


## Reto 5 ##
def reto5(id4):
    
    udpsock = socket(AF_INET, SOCK_DGRAM)

    headerFormat = '!3sBHHH'
    payload = base64.b64encode(id4.encode())
    packet = struct.pack(headerFormat, b'WYP', 0, 0, 0, 0) + payload
    # print(packet)
    checksum = cksum(packet)

    # print("Checksum 0: "+ str(checksum))
    header = struct.pack(headerFormat, b'WYP', 0, 0, checksum, 0)
    packet = header + payload
    # print(packet)
    checksum = cksum(packet)
    # print("Checksum 1: "+ str(checksum))
    # print("Cabecera enviada: "+ str(header))

    udpsock.sendto(packet, ('rick', 6000))

    data, server = udpsock.recvfrom(2048)
    # print(data)
    # print(server)


    lenData = str(len(data)-8)
    # print(len(lenData))
    formatResponse = '!3sBHH'+lenData+'s'
    
    msg = struct.unpack(formatResponse, data)
    msg = base64.b64decode(msg[4])
    print(msg)







## MAIN ##
username = "mystifying_bhabha"
id0 = reto0()
print("ID Reto 0: "+id0)
id1 = reto1(id0)
print("ID Reto 1: "+id1)
id2 = reto2(id1)
print("ID Reto 2: "+id2)
id3 = reto3(id2)
print("ID Reto 3: "+id3)
id4 = reto4(id3)
print("ID Reto 4: "+id4)
reto5(id4)
sys.exit("Fin del programa")