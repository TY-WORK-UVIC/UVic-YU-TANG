import socket
#from: https://pythonprogramming.net/sockets-tutorial-python-3/
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 1234))

full_msg = ''
while True:
	msg=s.recv(1024)
	if len(msg) <= 0:
		break
	full_msg += msg.decode("utf-8")
	
	if (len(full_msg) >0):
		print(full_msg)

