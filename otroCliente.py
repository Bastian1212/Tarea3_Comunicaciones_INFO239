from base64 import encode
import socket
import os
import time
import json

# Se envia un objeto en caso de que se este enviando los caracteres de una palabra ingresada
def envioMsg(msg, direccion):
    obj = {
        'idClient' : idClient,
        'mensaje': msg[0],
        'palabra': str(cont)
    }
    converted_obj = json.dumps(obj)
    bytesToSend = converted_obj.encode()
    UDPClientSocket.sendto(bytesToSend, direccion)

# Se envia un objeto en caso de que el cliente se quiera desconectar
def envioMsgTerminar(msg, direccion):
    obj = {
        'idClient' : idClient,
        'mensaje': msg
    }
    converted_obj = json.dumps(obj)
    bytesToSend = converted_obj.encode()
    UDPClientSocket.sendto(bytesToSend, direccion)

# Recibe la respuesta del servidor
def recibirRespuestaS(bs):
    msgServer = UDPClientSocket.recvfrom(bs) 
    return str(msgServer[0].decode()) 

msgFromClient       ="Using Link Client 1"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("192.168.194.100", 20001)

bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
print("Enviando ping al servidor")

#Envía ping a servidor
bytesToSend = str.encode("connect")
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

print("Recibiendo respuesta del servidor")
msgServer = UDPClientSocket.recvfrom(bufferSize)

idClient = str(msgServer[0])[2]
print("ID de cliente es:", idClient)


if __name__ == '__main__':

    time.sleep(1)

    os.system("clear")
    print("-----------------------------------------------------------------------------")
    print("Cliente : ", idClient)
    print("para finalizar escriba : terminar ")

    msgToServer = "" # Se almacenaran las palabras que el cliente ingrese
    n_word = 0 # Contador para controlar la cantidad de palabras que el cliente ha ingresado
    
    while (msgToServer != "terminar"):
        msgToServer = str(input("Ingrese su nombre  : ")).lower()
        n_word += 1

        if (msgToServer  != "terminar"):
            for caracter in msgToServer : 
                print("enviando mensaje")
                envioMsg(caracter,serverAddressPort)

                print("esperando respuesta del servidor ")
                respuesta = recibirRespuestaS(bufferSize) 

                while(respuesta =="NAK"):
                    print("Hubo una perdida del mensaje\n")
                    envioMsg(caracter,serverAddressPort)
                    respuesta = recibirRespuestaS(bufferSize)
                    time.sleep(2)

                if(respuesta=="ACK"):
                    print("el mensaje se recibio con exito\n")
                    
                    
                time.sleep(2)

    #Envia mensaje de terminado al server
    envioMsgTerminar("terminar",serverAddressPort)
    respuesta = recibirRespuestaS(bufferSize)
    while(respuesta =="NAK"):
        print("Hubo una perdida del mensaje\n")
        envioMsgTerminar("terminar",serverAddressPort)
        respuesta = recibirRespuestaS(bufferSize)

    if(respuesta=="ACK"):
        os.system("clear")
        print("-----------------------------------------------------------------------------")
        print("Proceso Terminado")
        print("-----------------------------------------------------------------------------")
        texto = recibirRespuestaS(bufferSize)
        print(texto)
    



