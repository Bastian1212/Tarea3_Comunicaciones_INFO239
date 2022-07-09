import socket
import time
import random
import os


def reciboMsj(buff):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    return bytesAddressPair[0], bytesAddressPair[1]

def envioMsg(msj, direccion):
    bytesToSend = str.encode(msj)
    UDPServerSocket.sendto(bytesToSend, direccion)



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
    print("mensaje recibido")
    ## si se  conecta un cliente 
    if(ClientM == "b'conect'" ):
        os.system("clear")
        print("conectando ")
        idClient+=1
        print("Id Client :",idClient)
        envioMsg(str(idClient),address)
        ## agrega una lista a nuestra lista nombres donde se almacenaran los caracteres 
        nombres.append([])
        
    else : 
        ## id del cliente con la cual estamos conversdando 
        idClientAct = int(ClientM[4]) 
        if(ClientM!= "b'listo'"):
               
            caracter = str(ClientM[3])
            nombres[idClientAct-1] += caracter
            print(nombres)

            ## envia un mensaje de confirmacion al cliente
            msgFromServer ="ACK"
            print("enviando respuesta al cliente ")
            envioMsg(msgFromServer,address)
        else:
           
            print("se enviara el mensaje recibido")
            textonombre = ""
            listo =  nombres[idClientAct-1]
            for i in nombres:
                textonombre+=i
            envioMsg(textonombre, address)
            break







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



