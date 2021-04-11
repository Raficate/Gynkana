#!/usr/bin/python3

from socket import *

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
        
    comprobacion= comprobacion.split(':')[1]
    idmsg = comprobacion.split('\n')[0]
    tcpSock.close()
    return idmsg

## RETO 3 ##
def reto3(id2):
    # Parte 1, conectar con el servidor tcp rick:6500
    tcpsock = socket(AF_INET, SOCK_STREAM)
    tcpsock.connect(('rick', 6500))
    
    #Parte 2, recorre el mensaje palabra por palabra y comprueba donde está el palindromo
    cadena = ""
    cont = 0

    while 1:

        msg = tcpsock.recv(1024).decode()
        # print("------------")
        # print(msg)
        # cadena = cadena + msg
        if msg == "":
            break
        
        result = buscaPalindromo(msg)
        if result==-1:
            cadena = cadena + msg
        else:
            ulti = msg.split(result)
            cadena = cadena + ulti[0]
            print("---------------"+result+"____________")
            break

    print(cadena)

    return "Hola"          

    

    
    # cadena = ""
    # palabra = ""
    # for each c in msg



## MAIN ##
username = "mystifying_bhabha"
id0 = reto0()
# print("ID Reto 0: "+id0)
id1 = reto1(id0)
# print("ID Reto 1: "+id1)
id2 = reto2(id1)
# print("ID Reto 2: "+id2)
reto3(id2)