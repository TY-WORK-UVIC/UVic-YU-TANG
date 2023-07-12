"""
1. server hostname and port number : command line arguments 
2. time in second 
3. create UDP client socket (DGRAM) 
4. set socket timeout as 1 second 
5. change the port into int 
6. msg format (see lab2.pdf) 
7. while loop running 10 times:
		a. keep track of sent time A
		b. send the UDP packet
		c. recieve the sever respond
		d. keep track of recieved time B
		e. display server response
		f. calculate the round trip time (RTT) B - A
		g. exception: 
				case for assuming the packet loss
		NOTE: order matters!
		NOTE: using function is more accurate than using wireshark to calculate the RTT (this indicates ther may be different)
8. close connetion

NOTE: open the wireshark inside mininet VM, otherwise it won't be able to capture packets
NOTE: TA will ask even previous questions
"""

import sys
import datetime
import time
from socket import *

host_ip = sys.argv[1] 
host_port =  int(sys.argv[2])

# Create a UDP socket 
# Notice the use of SOCK_DGRAM for UDP packets
clientSocket = socket(AF_INET, SOCK_DGRAM)

#don't need connection because UDP is connectionless

clientSocket.settimeout(1.0) # set a one-second pause

for i in range(1, 11):
	try:
		curtime = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
		#print send_time
		#print time
		msg = 'ping ' + str(i) + " " + curtime
		
		sentmsg = msg.encode()
		send_time = time.time()
		clientSocket.sendto(msg, (host_ip,host_port))

		receivedmsg = "Reply from " + host_ip + ": " + clientSocket.recvfrom(1024)[0].decode()
		print receivedmsg
		#sys.stdout.flush()
	
		RTT = time.time() - send_time
		RTTinfo = "RTT: " + str(RTT)
		print RTTinfo				
		
		

	except timeout:
		print "Request Timed Out"
clientSocket.close()
