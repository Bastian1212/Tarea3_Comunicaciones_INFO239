from base64 import decode
import socket
import time
import random
import os
import json

'''
    Integrantes: Diego Troncoso Jara y Bastián Villanueva
    Curso: Comunicaciones
    Profesor: Cristian Lazo

'''


# Se envia el mensaje al cliente
def envioMsg(msj, direccion):
    bytesToSend = str.encode(msj)
    UDPServerSocket.sendto(bytesToSend, direccion)

# Recibe el mensaje del cliente
def reciboMsj(buff):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    return bytesAddressPair[0].decode(), bytesAddressPair[1]

# Genera la pérdida de los mensajes
def generadorDePerdida():
    perdida =random.randint(1,11)
    time = 0
    if perdida <= 3:
        time = random.randint(2001,3000)/1000
    else: 
        time = random.randint(500,2000)/1000
    return time


# Variables globales para controlar los id de los clientes y los mensajes que se recibirán, 
idClient    = 0 
nombres     = []

localIP             = "127.0.0.1"
localPort           = 20001
bufferSize          = 1024
msgFromServer       = "ACK"
bytesToSend         = str.encode(msgFromServer)


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip, conexion (host, puerto)
UDPServerSocket.bind((localIP, localPort))
print("Server ok ")
# peticiones que puede manejar en cola
time.sleep(1)

# El server está listo para recibir conexiones de los clientes.
while(True):
    # Se recibe el mensaje y la dirección ip del cliente.
    message,address = reciboMsj(bufferSize)
    mensaje_decode = str(message)
    print("mensaje recibido")

    # Si se  conecta un nuevo cliente, se le enviará el ID designado por el server y se creará 
    # un espacio de memoria en una lista para recibir los mensajes.
    if(mensaje_decode == 'connect' ):
        os.system("clear")
        print("conectando ")
        idClient+=1
        print("Id Client :",idClient)
        envioMsg(str(idClient),address)
        # Agrega una lista a nuestra lista 'nombres' donde se almacenarán los caracteres.
        nombres.append([])
        
    else : 
        # Se genera la pérdida del mensaje y se envía un NAK
        tiempo = generadorDePerdida()
        print("Tiempo perdida",tiempo)
        while(tiempo>=2):
            tiempo = generadorDePerdida()
            time.sleep(tiempo)
            print("Se realizó una pérdida \n")

            print("Enviando aviso al cliente \n")
            msgFromServer ="NAK"
            envioMsg(msgFromServer,address)
            print("esperando data del cliente \n")

            message,address = reciboMsj(bufferSize)
            mensaje_decode = str(message)
        
        # Se recibirá un objeto que podrá tener las siguientes estructuras
        # nº 1: {'idClient': '1', 'mensaje': 'd', 'palabra': '1'}, estructura para recibir carácteres.
        # nº 2: {'idClient': '1', 'mensaje': 'terminar'}, estructura para desconectar al cliente.
        obj = json.loads(mensaje_decode) 

        # Dependiendo de la estructura recibida, se definirán los siguientes parámetros.
        if (len(obj) == 3):
            obj_idClient = int(obj["idClient"]) # ID del cliente
            obj_mensaje = obj["mensaje"] # Cáracter que se recibirá
            obj_palabra = int(obj["palabra"]) # Número de la palabra enviada, ej: palabra nº 1, 2, 3, etc.

        else:
            obj_idClient = int(obj["idClient"])
            obj_mensaje = obj["mensaje"] 
 
            
        # Si el mensaje recibido es un carácter entrará en este ciclo.
        if(obj_mensaje != "terminar"):

            # Si la lista del cliente está vacía, se insertá el mensaje en la primera posición.
            if(not(bool(nombres[obj_idClient-1]))):
                print("Vacio: ")
                nombres[obj_idClient-1].insert(0, obj_mensaje)
            
            
            else:
                # Si se quiere insertar otro mensaje, el primer carácter se almacenará en la siguiente posición de la lista
                # de manera que quede de la siguiente forma: nombres = [ ["mensaje1", "mensaje2"], ["mensaje1", "mensaje2"] ]
                #                                                           idCliente = 0               idCliente = 1
                if(obj_palabra > len(nombres[obj_idClient-1])):
                    print("Cae en esto")
                    nombres[obj_idClient-1].insert(obj_palabra-1, obj_mensaje)
                    
                else: 
                    # Se concatenan los carácteres en el espacio de memoria designada.
                    nombres[obj_idClient-1][obj_palabra-1] += obj_mensaje

            print("nombres insertado :", nombres)

            ## envia un mensaje de confirmacion al cliente
            msgFromServer ="ACK"
            print("enviando respuesta al cliente ")
            envioMsg(msgFromServer,address)
        
        # Aquí se desconectará al cliente
        else:
            msgFromServer ="ACK"
            envioMsg(msgFromServer,address)
        
            print("---------------------------------------")
            print("Se enviará el mensaje recibido al cliente con ID = ", obj_idClient)
            dirUserMessages = len(nombres[obj_idClient-1]) # Direccion de los mensajes recibidos para el cliente 
            texto = ""
            # El server le enviará los mensajes que el cliente había enviado.
            if (dirUserMessages != 0):
                for i in range(dirUserMessages):
                    texto += "Mensaje nº " + str(i) + " es: " + str(nombres[obj_idClient-1][i]) + "\n"
                    print(f"Mensaje nº {i} es: {nombres[obj_idClient-1][i]}")
            # Si el cliente no envió ningún mensaje se le avisará y desconectará.
            else:
                texto = "El usuario no envió mensajes"

            envioMsg(texto, address)
            

