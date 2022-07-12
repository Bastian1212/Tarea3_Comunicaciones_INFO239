from base64 import decode
import socket
import time
import random
import os
import json

def envioMsg(msj, direccion):
    bytesToSend = str.encode(msj)
    UDPServerSocket.sendto(bytesToSend, direccion)

def reciboMsj(buff):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    return bytesAddressPair[0].decode(), bytesAddressPair[1]

def generadorDePerdida():
    perdida =random.randint(1,11)
    time = 0
    if perdida <= 3:
        time = random.randint(2001,3000)/1000
    else: 
        time = random.randint(500,2000)/1000
    return time


# Variables globales para controlar los id de los clientes y los mensajes que se recibirán, 
idClient = 0 
nombres = []



localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
msgFromServer       = "ACK"
bytesToSend         = str.encode(msgFromServer)


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip, conexion (host, puerto)
UDPServerSocket.bind((localIP, localPort))
print("Server ok ")
# peticiones que puede manejar en cola
time.sleep(1)

# Listen for incoming datagrams
while(True):
    
    message,address = reciboMsj(bufferSize)
    mensaje_decode = str(message)
    print("mensaje recibido")

    ## si se  conecta un cliente 
    if(mensaje_decode == 'connect' ):
        os.system("clear")
        print("conectando ")
        idClient+=1
        print("Id Client :",idClient)
        envioMsg(str(idClient),address)
        ## agrega una lista a nuestra lista nombres donde se almacenaran los caracteres 
        nombres.append([])
        
    else : 
        tiempo = generadorDePerdida()
        print("tiempo perdida",tiempo)
        while(tiempo>=2):
            tiempo = generadorDePerdida()
            time.sleep(tiempo)
            print("se realizo perdida \n")

            print("enviando aviso al  cliente \n")
            msgFromServer ="NAK"
            envioMsg(msgFromServer,address)
            print("esperando data del cliente \n")

            message,address = reciboMsj(bufferSize)
            mensaje_decode = str(message)
        
        obj = json.loads(mensaje_decode) # {'idClient': '1', 'mensaje': 'd', 'palabra': '1'}

        if (len(obj) == 3):
            obj_idClient = int(obj["idClient"])
            obj_mensaje = obj["mensaje"]
            obj_palabra = int(obj["palabra"])

        else:
            obj_idClient = int(obj["idClient"])
            obj_mensaje = obj["mensaje"] 
 
            
        ## id del cliente con la cual estamos conversando
        if(obj_mensaje != "terminar"):
            if(not(bool(nombres[obj_idClient-1]))):
                print("Vacio: ")
                nombres[obj_idClient-1].insert(0, obj_mensaje)
                
            else:

                if(obj_palabra > len(nombres[obj_idClient-1])):
                    print("Cae en esto")
                    nombres[obj_idClient-1].insert(obj_palabra-1, obj_mensaje)
                    
                else: 
                    nombres[obj_idClient-1][obj_palabra-1] += obj_mensaje

            print("nombres insertado :", nombres)

            ## envia un mensaje de confirmacion al cliente
            msgFromServer ="ACK"
            print("enviando respuesta al cliente ")
            envioMsg(msgFromServer,address)
        
        else:
            msgFromServer ="ACK"
            envioMsg(msgFromServer,address)
        
            print("---------------------------------------")
            print("se enviara el mensaje recibido al cliente con ID = ", obj_idClient)
            dirUserMessages = len(nombres[obj_idClient-1])
            texto = ""
            if (dirUserMessages != 0):
                for i in range(dirUserMessages):
                    texto += "Mensaje nº " + str(i) + " es: " + str(nombres[obj_idClient-1][i]) + "\n"
                    print(f"Mensaje nº {i} es: {nombres[obj_idClient-1][i]}")
            else:
                texto = "El usuario no envió mensajes"

            envioMsg(texto, address)
            

