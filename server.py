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

def generadorDePerdida():
    perdida =random.randint(1,11)
    time = 0
    if perdida <= 3:
        time = random.randint(2001,3000)/1000
    else: 
        time = random.randint(500,3000)/1000
    
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
       
        if str(ClientM)[4].isnumeric():
            idClientAct = int(ClientM[4])    
        else: 
            idClientAct = int(ClientM[7])   
        
        if(ClientM!= "b'listo"+str(idClientAct)+"'"):
               
            caracter = str(ClientM[3])
            nombres[idClientAct-1] += caracter
            print(nombres)
            print(generadorDePerdida())
            tiempo = generadorDePerdida()
            time.sleep(tiempo)    
            ## envia un mensaje de confirmacion al cliente
            msgFromServer ="ACK"
            print("enviando respuesta al cliente ")
            envioMsg(msgFromServer,address)
        else:
           
            print("se enviara el mensaje recibido")
            textonombre = ""
            lista=  nombres[idClientAct-1]
            if(len(nombres)>=1):
                for i in lista:
                    textonombre+=i
                envioMsg(textonombre, address)
            idClientAct = 0 


