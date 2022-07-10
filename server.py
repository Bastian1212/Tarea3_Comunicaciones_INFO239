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



MensajeNombre = ""
ClientM =""
idMen = 0 
idClient = 0 
idClientAct = 0
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
#UDPServerSocket.listen(N)
time.sleep(1)

# Listen for incoming datagrams
while(True):
    
    message,address = reciboMsj(bufferSize)
    mensaje_decode = str(message)
    print("message: ", message)
    # decoded_message = json.load(message.decode())
    # print("decoded_message: ", decoded_message)


    print("mensaje recibido")
    ## si se  conecta un cliente 
    if(mensaje_decode == 'connect' ):
        os.system("clear")
        print("conectando ")
        idClient+=1
        print("Id Client :", idClient)
        envioMsg(str(idClient),address)

        ## agrega una lista a nuestra lista nombres donde se almacenaran los caracteres 
        nombres.append([])
        
    else : 
        # Si el mensaje recibido es un objeto, quiere decir que se está enviando información
        if (mensaje_decode[0] == '{'):
            obj = json.loads(mensaje_decode) # {'idClient': '1', 'mensaje': 'd', 'palabra': '1'}
            obj_idClient = int(obj["idClient"])
            obj_mensaje = obj["mensaje"]
            obj_numPalabra = int(obj["palabra"])
        
        # Si no es un objeto, quiere decir que el usuario se va a desconectar
        else:
            obj_mensaje = mensaje_decode

        # Si no es el mensaje para terminar, se empieza a agregar los caracteres en la lista
        if(obj_mensaje!= "listo"+str(obj_idClient)):

            # Si la lista del Cliente está vacía, se inserta el mensaje en la primera posicion
            if(not(bool(nombres[obj_idClient-1]))):
                print("Vacio: ")
                nombres[obj_idClient-1].insert(0, obj_mensaje)
            
            else:
                # Si se quiere insertar otro mensaje, el primer caracter se almacenará en la siguiente posición de la lista
                # de manera que quede de la siguiente forma: nombres = [ ["mensaje1", "mensaje2"], ["mensaje1", "mensaje2"] ]
                #                                                           idCliente = 0               idCliente = 1

                if(obj_numPalabra > len(nombres[obj_idClient-1])):
                    print("Cae en esto")
                    nombres[obj_idClient-1].insert(obj_numPalabra-1, obj_mensaje)

                # Se van concatenando los caracteres en la lista .
                else: 
                    nombres[obj_idClient-1][obj_numPalabra-1] += obj_mensaje
                
           
            print("nombres insertados :", nombres)

            ## envia un mensaje de confirmacion al cliente
            msgFromServer ="ACK"
            print("enviando respuesta al cliente ")
            envioMsg(msgFromServer,address)
        
        # Si el cliente desea terminar el proceso, el server le enviará los mensajes que el cliente había enviado.
        else:
            print("---------------------------------------")
            print("se enviara el mensaje recibido al cliente con ID = ", obj_idClient)
            texto = ""
            for i in range(len(nombres[obj_idClient-1])):
                texto += "Mensaje nº " + str(i) + " es: " + str(nombres[obj_idClient-1][i]) + "\n"
                print(f"Mensaje nº {i} es: {nombres[obj_idClient-1][i]}")

            envioMsg(texto, address)
