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
        'palabra': str(n_word)
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
#serverAddressPort   = ("192.168.194.100", 20001) # ip para ZeroTier
serverAddressPort   = ("127.0.0.1", 20001) # ip local
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
    
    # Si el mensaje del cliente no es terminar, quiere decir que enviará mensajes.
    while (msgToServer != "terminar"):
        # Se recibe la palabra que el usuario ingresó
        msgToServer = str(input("Ingrese su nombre  : ")).lower()
        n_word += 1
        print("Enviando mensaje \n")

        # Si el mensaje del cliente no es terminar, se enviará carácter por carácter 
        # la palabra que ha ingresado el cliente.
        if (msgToServer  != "terminar"):
            for caracter in msgToServer : 
                
                print("Enviando caracter")
                envioMsg(caracter,serverAddressPort)

                print("Esperando respuesta del servidor ")
                respuesta = recibirRespuestaS(bufferSize) 

                # Si recibe un NAK, tendrá que reenviar el mensaje.
                while(respuesta =="NAK"):
                    print("Hubo una pérdida del caracter\n")
                    envioMsg(caracter,serverAddressPort)
                    respuesta = recibirRespuestaS(bufferSize)
                    time.sleep(2)

                # Si recibe un ACK, quiere decir que el servido recibió bien el mensaje.
                if(respuesta=="ACK"):
                    print("El carácter se recibió con éxito\n")
                    
                time.sleep(2)
            print("mensaje enviado \n")

    #Envia mensaje de terminado al server
    envioMsgTerminar("terminar",serverAddressPort)
    respuesta = recibirRespuestaS(bufferSize)

    # Si recibe un NAK tendrá que reenviar el mensaje de terminar
    while(respuesta =="NAK"):
        print("Hubo una perdida del mensaje\n")
        envioMsgTerminar("terminar",serverAddressPort)
        respuesta = recibirRespuestaS(bufferSize)

    # Si el mensaje se recibió correctamente, el cliente se desconectará 
    # y recibirá los mensajes enviados al servidor.
    if(respuesta=="ACK"):
        os.system("clear")
        print("-----------------------------------------------------------------------------")
        print("Proceso Terminado")
        print("-----------------------------------------------------------------------------")
        texto = recibirRespuestaS(bufferSize)
        print(texto)
    



