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
    ClientM = str(message)
    print("message: ", message)
    # decoded_message = json.load(message.decode())
    # print("decoded_message: ", decoded_message)


    print("mensaje recibido")
    ## si se  conecta un cliente 
    if(ClientM == 'connect' ):
        os.system("clear")
        print("conectando ")
        idClient+=1
        print("Id Client :",idClient)
        envioMsg(str(idClient),address)
        ## agrega una lista a nuestra lista nombres donde se almacenaran los caracteres 
        nombres.append([])
        
    else : 

        ####################################################################################################################
        tiempo = generadorDePerdida()
        print("tiempo perdida",tiempo)
        while(tiempo>=2):
            tiempo = generadorDePerdida()
            time.sleep(tiempo)
            print("se realizo perdida ")
            print()
            print("enviando aviso al  cliente")
            msgFromServer ="NAK"
            envioMsg(msgFromServer,address)
            print()
            print("esperando data del cliente")
            message,address = reciboMsj(bufferSize)
            ClientM = str(message)
        
        mensaje_decode = ClientM
        print("MENSJAEEEEE: ", mensaje_decode)
        obj = json.loads(mensaje_decode) # {'idClient': '1', 'mensaje': 'd', 'palabra': '1'}
        print("obj :  ",obj)

        if (len(mensaje_decode)==3):
            
            obj_idClient = int(obj["idClient"])
            obj_mensaje = obj["mensaje"]
            obj_palabra = int(obj["palabra"])
        else:
            obj_idClient = int(obj["idClient"])
            obj_mensaje = obj["mensaje"] 
            




        ## id del cliente con la cual estamos conversdando
        


       

        print("obj men ",obj_mensaje)
        if(obj_mensaje!= "terminar"):

            print("len: ", len(nombres[obj_idClient-1]))
            print("obj_p")

            if(not(bool(nombres[obj_idClient-1]))):
                print("Vacio: ")
                nombres[obj_idClient-1].insert(0, obj_mensaje)
                
            else:
                print(f'obj_palabra: {obj_palabra} \n lenNombre: {len(nombres[obj_idClient-1])} \n idCLient : {obj_idClient}')

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
            texto = ""
            for i in range(len(nombres[obj_idClient-1])):
                texto += "Mensaje nº " + str(i) + " es: " + str(nombres[obj_idClient-1][i]) + "\n"
                print(f"Mensaje nº {i} es: {nombres[obj_idClient-1][i]}")

            envioMsg(texto, address)
            


##b
## 1b1
## 2a1







    #perdida = random.randint(1,11)
    #print("perdida: ", perdida)
    # 30% de prob de que ocurra un error
    # if(perdida <=3):
    #     print("Error al recibir el paquete")
    #     UDPServerSocket.sendto(msgError, address)
    #     bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    #     message = bytesAddressPair[0] # mensaje recibido
    #     address = bytesAddressPair[1] # (ip, puerto)
    #     clientMsg = "Message from Client:{}".format(message)
    #     print("Canal Ocupado")
    #     clientMsg = format(message) 
    #     print(clientMsg)

    # clientMsg = "Message from Client:{}".format(message)
    # print("Canal Ocupado")
    # clientMsg = format(message) 
    # print(clientMsg)
    # time.sleep(30) # Segundos


    # # Enviando respuesta al cliente
    # UDPServerSocket.sendto(bytesToSend, address)
    # print("bytesToSend: ", bytesToSend)
    


    # print("Link Available")



