from base64 import encode
import socket
import os
import time
import json

def envioMsg(msg, direccion):
    obj = {
        'idClient' : idClient,
        'mensaje': msg[0],
        'palabra': str(cont)
    }

    # A = [[]]
    converted_obj = json.dumps(obj)
    bytesToSend = converted_obj.encode()
    UDPClientSocket.sendto(bytesToSend, direccion)

def recibirRespuestaS(bs):
    msgServer = UDPClientSocket.recvfrom(bs) 
    return str(msgServer[0].decode()) 

# b'1a1'
# b'10a1'

msgFromClient       ="Using Link Client 1"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)



print("Enviando ping al servidor")
#Envía ping a servidor
bytesToSend = str.encode("connect")
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
    cont = 0
    
    while (msgServer != "terminar"):

        msgServer = str(input("Ingrese su nombre  : ")).lower()
        cont += 1
        if (msgServer  != "terminar"):
            for caracter in msgServer : 
                print("enviando mensaje")
                envioMsg(caracter,serverAddressPort)

                print("esperando respuesta del servidor ")
                respuesta = recibirRespuestaS(bufferSize) 

                while(respuesta =="b'NAK'"):
                    print("Hubo una perdida del mensaje")
                    envioMsg(caracter,serverAddressPort)
                    respuesta = recibirRespuestaS(bufferSize)
                    time.sleep(2)

                if(respuesta=="b'ACK'"):
                    print("el mensaje se recibio con exito")
                    
                time.sleep(2)
                



    

    #Envia mensaje de terminado al server
    UDPClientSocket.sendto(str.encode("listo"+ idClient), serverAddressPort)
    os.system("clear")
    print("-----------------------------------------------------------------------------")
    print("Proceso Terminado")
    print("-----------------------------------------------------------------------------")

    texto = recibirRespuestaS(bufferSize)
    print(texto)




