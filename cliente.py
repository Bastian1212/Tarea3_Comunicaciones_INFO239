from base64 import encode
import socket
import os
import time

def envioMsg(msg, direccion):
    bytesToSend =str.encode(str(cont)+msg[0]+idClient)
    UDPClientSocket.sendto(bytesToSend, direccion)

def recibirRespuestaS(bs):
    msgServer = UDPClientSocket.recvfrom(bs) 
    return str(msgServer[0]) 



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

    msgToServer = ""
    cont = 1    
    
    while (msgToServer != "terminar"):

        msgToServer = str(input("Ingrese su nombre por caracter : ")).lower()

        if (msgToServer  != "terminar"):
            
            ## se envia el mensaje al servidor 
            print("enviando mensaje")
            envioMsg(msgToServer,serverAddressPort)
            print("esperando respuesta del servidor ")
            respuesta = recibirRespuestaS(bufferSize) 

            while(respuesta =="b'NAK'"):
                print("Hubo una perdida del mensaje")
                envioMsg(msgToServer,serverAddressPort)
                respuesta = recibirRespuestaS(bufferSize)
                time.sleep(2)


            if(respuesta=="b'ACK'"):
                print("el mensaje se recibio con exito")
                cont+=1
            

# BASTIAN
# B1, A2, S3 ...
# B2, A3, S4, T5, I6, A7, N0

    

    #Envia un mensaje del formato "terminado" al server
    UDPClientSocket.sendto(str.encode("listo"+ idClient), serverAddressPort)
    os.system("clear")
    print("-----------------------------------------------------------------------------")
    texto = recibirRespuestaS(bufferSize)[2:]
    print(texto)




