#import socket module
from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a server socket
#?????????????????
#host = gethostbyname(gethostname())
host = '10.0.0.1'
#print host
port = 6789
serverSocket.bind((host, port))
serverSocket.listen(1)

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr =  serverSocket.accept() 
          
    try:
	
        message = connectionSocket.recv(1024) #?????????????????       
       	#print message
        filename = message.split()[1]                 
	
        f = open(filename[1:]) 
	#f = open('hello.html')
	
        outputdata = f.read()#???????????????                  
        #Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.0 200 OK\r\n')
	connectionSocket.send("Content-Type: text/html\r\n\r\n")
	


        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):           
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
     	
   	#connectionSocket.send('Thank you for the connetion')
        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        connectionSocket.send('error: 404 Not Found')

        #Close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
