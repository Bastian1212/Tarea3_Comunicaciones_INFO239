from base64 import encode
import socket
import os
import time

def envioMsg(msg, direccion):
    bytesToSend =str.encode(msg[0]+idClient)
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



print("esperando servidor")
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

        msgServer = str(input("Ingrese su nombre  : ")).lower()

        if (msgServer  != "terminar"):
            
            for i in msgServer : 
                print("enviando mensaje")
                envioMsg(i,serverAddressPort)
                print("esperando respuesta del servidor ")
                respuesta = recibirRespuestaS(bufferSize) 
                while(respuesta =="b'NAK'"):
                    print("Hubo una perdida del mensaje")
                    envioMsg(i,serverAddressPort)
                    respuesta = recibirRespuestaS(bufferSize)
                   
                if(respuesta=="b'ACK'"):
                    os.system("clear")
                    print("el mensaje se recibio con exito")
                    cont+=1
                time.sleep(2)
                



    

    #Envia mensaje de terminado al server
    UDPClientSocket.sendto(str.encode("listo"+ idClient), serverAddressPort)
    os.system("clear")
    print("-----------------------------------------------------------------------------")
    texto = recibirRespuestaS(bufferSize)[2:]
    print(texto)




