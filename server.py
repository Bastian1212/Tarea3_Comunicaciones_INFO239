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
    ## si se  conecta un cliente nuevo
    if(ClientM == "b'conect'" ):
        os.system("clear")
        print("conectando ")
        idClient+=1
        print("Id Client :",idClient)
        envioMsg(str(idClient),address)
        ## agrega una lista a nuestra lista nombres donde se almacenaran los caracteres 
        nombres.append([])
    
    # Empieza a recibir mensajes    
    else : 
        ## id del cliente con la cual estamos conversando
        # Si es un caracter, el id estara en la pos 4
        if str(ClientM)[4].isnumeric():
            idClientAct = int(ClientM[4])    

        # Si se quiere terminar el proceso, se recibira un mensaje mas 
        # largo por lo que el id estara en la pos 7
        else: 
            idClientAct = int(ClientM[7])   
        
        # Si el mensaje recibido no es de la formato para terminar el proceso,
        # se recibe el mensaje y se envia un ACK
        if(ClientM!= "b'listo"+str(idClientAct)+"'"):
            caracter = str(ClientM[3])

            if(idClientAct>len(nombres)):
                nombres[idClientAct-2] += caracter
                print(nombres)
            else:
                nombres[idClientAct-1] += caracter
                print(nombres)
            
            

# A = [ [] ] id = 2  / len = 1
# 

            ## envia un mensaje de confirmacion al cliente
            msgFromServer ="ACK"
            print("enviando respuesta al cliente ")
            envioMsg(msgFromServer,address)
        # Si el mensaje recibido es del formato "terminar proceso", se entrega
        # el mensaje al usuario y se elimina de la memoria.
        else:
            if(idClientAct>len(nombres)):
                aux = 2
            else:
                aux = 1

            print("se enviara el mensaje recibido")
            textonombre = ""
            lista = nombres[idClientAct-aux]
            if(len(nombres)>=1):
                for i in lista:
                    textonombre+=i
                envioMsg(textonombre, address)
                # Se elimina el mensaje del server
                nombres.pop(idClientAct-aux)
            print(nombres)
            idClientAct = 0 







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



