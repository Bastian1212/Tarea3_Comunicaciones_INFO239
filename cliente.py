from base64 import encode
import socket
import os
import time

def envioMsg(msg, direccion):
    bytesToSend =str.encode(str(cont)+msg[0]+idClient)
    UDPClientSocket.sendto(bytesToSend, direccion)





msgFromClient       ="Using Link Client 1"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

print("Enviando ping al servidor")
#Envía ping a servidor
bytesToSend = str.encode("conect")
UDPClientSocket.sendto(bytesToSend, serverAddressPort)


print("Recibiendo respuesta del servidor")
#Recibe respuesta del server
msgServer = UDPClientSocket.recvfrom(bufferSize)
idClient = str(msgServer[0])[2]
print("ID de cliente es:", idClient)


if __name__ == '__main__':

    time.sleep(1)

    os.system("clear")
    print("-----------------------------------------------------------------------------")
    print("Cliente : ", idClient)
    print("para finalizar escriba : terminar ")

    msgServer = ""
    cont = 1    
    
    while (msgServer != "terminar"):

        msgServer = str(input("Ingrese su nombre por caracter : ")).lower()

        if (msgServer  != "terminar"):
            
            ## se envia el mensaje al servidor 
            print("enviando mensaje")
            envioMsg(msgServer,serverAddressPort)
            print("esperando respuesta del servidor ")
            



    

    #Envia mensaje de terminado al server
    UDPClientSocket.sendto(str.encode("done" + idClient), serverAddressPort)



