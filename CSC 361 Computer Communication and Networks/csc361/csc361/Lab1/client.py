#import socket module
from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a server socket
#?????????????????
host = sys.argv[1]
port = int(sys.argv[2])
fileName = sys.argv[3]

serverSocket.connect((host, port))
print('connected to server')
serverSocket.send('GET /'+ fileName + ' HTTP/1.0'.encode())
print('message sent')

print serverSocket.recv(1024)

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
