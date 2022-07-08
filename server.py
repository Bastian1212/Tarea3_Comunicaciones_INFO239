import socket
import time
import random


localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
msgFromServer       = "Datagram Acepted"
bytesToSend         = str.encode(msgFromServer)

msgError = str.encode("Error")
N = 5

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip, conexion (host, puerto)
UDPServerSocket.bind((localIP, localPort))
# peticiones que puede manejar en cola
#UDPServerSocket.listen(N)

print("Link Available")

# Listen for incoming datagrams
while(True):
    # Conexion con el cliente
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0] # mensaje recibido
    address = bytesAddressPair[1] # (ip, puerto)

    #perdida = random.randint(1,11)
    #print("perdida: ", perdida)
    perdida = 1
    # 30% de prob de que ocurra un error
    if(perdida <=3):
        print("Error al recibir el paquete")
        UDPServerSocket.sendto(msgError, address)
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0] # mensaje recibido
        address = bytesAddressPair[1] # (ip, puerto)
        clientMsg = "Message from Client:{}".format(message)
        print("Canal Ocupado")
        clientMsg = format(message) 
        print(clientMsg)

    clientMsg = "Message from Client:{}".format(message)
    print("Canal Ocupado")
    clientMsg = format(message) 
    print(clientMsg)
    time.sleep(30) # Segundos


    # Enviando respuesta al cliente
    UDPServerSocket.sendto(bytesToSend, address)
    print("bytesToSend: ", bytesToSend)
    


    print("Link Available")