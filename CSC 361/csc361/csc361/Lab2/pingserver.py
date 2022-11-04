# We will need the following module to generate randomized lost packets
import random
from socket import *

# Create a UDP socket 
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)	#understand and explain this 

# Assign IP address and port number to socket
serverSocket.bind(('', 12000)) 

while True:
	# Generate random number in the range of 0 to 10
	rand = random.randint(0, 10)  #0 - 9  

	# Receive the client packet along with the address it is coming from 
	message, address = serverSocket.recvfrom(1024) #buffer size :1024

	# Capitalize the message from the client
	message = message.upper() #change to uppercase

	# If rand is less is than 4, we consider the packet lost and do not respond
	if rand < 4: # modify this for packet loss assumption
		continue
	# Otherwise, the server responds    
	serverSocket.sendto(message, address)