import socket
import sys
import os
from time import time, ctime

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_ip = sys.argv[1]
port_number = int(sys.argv[2])

s.bind((host_ip,port_number))
s.listen(5)

print("Sever is listening ....")

def main():
	while True:
		command=""
		parameter2=""
		parameter3=""
		parameter=""
		command2=""
		c_sock,c_addr=s.accept()
		c_sock.send("connect server successfully!\n".encode())
		print("Connection from {address} has been established!".format(address=c_addr))
		try:
			user_input = c_sock.recv(1024).decode()
			command = user_input.split()[0]
			if command != "" and len(user_input.split())>= 3:
				parameter2 = user_input.split()[1]
				parameter3 = user_input.split()[2]
			if command == "GET" and parameter3 == "HTTP/1.0":
				user_input = c_sock.recv(1024)
				length = user_input.decode()
				command = user_input.split()[0].decode()
				#print("Filename: "+parameter2)
				#print("command: "+command)
				if user_input.split()[0].decode() != "" and len(length.split())>= 2:
					parameter = user_input.split()[1].decode()
					#print("activity: "+parameter)
				if command == "Connection:" and parameter == "keep-alive":
					c_sock.send("\r\n".encode())
					try :
						f=open(parameter2[1:])
						
						lines=f.read()
						
						c_sock.send("HTTP/1.0 200 OK\r\n\r\n".encode())
						copy = "HTTP/1.0 200 OK\r\n\r\n"
						for i in lines:
							copy = copy + i
							c_sock.send(i.encode())
						f.close()
						c_sock.send("\r\n".encode())
						now = time()
						ctime(now)
						index = ctime(now).find('2020')
						current_time = ctime(now)[:index] + "PDT " + ctime(now)[index:]
						dt_string = current_time+":"+c_addr[0]+":"+str(c_addr[1])+" "+length+"; HTTP/1.0 200 OK\r\n\r\n"
						print(dt_string)
						c_sock.close()
					except FileNotFoundError:
						c_sock.send("HTTP/1.0 404 Not Found\r\n\r\n".encode())
						now = time()
						ctime(now)
						index = ctime(now).find('2020')
						current_time = ctime(now)[:index] + "PDT " + ctime(now)[index:]
						dt_string = current_time+":"+c_addr[0]+":"+str(c_addr[1])+"  "+length+"; HTTP/1.0 404 Not Found\r\n\r\n"
						print(dt_string)
						c_sock.close()
				elif user_input == "":
					try :
						f=open(parameter2[1:])
						
						lines=f.read()
						c_sock.send("IN EMPTY successcully\r\n\r\n".encode())
						c_sock.send("HTTP/1.0 200 OK\r\n\r\n".encode())
						copy = "HTTP/1.0 200 OK\r\n\r\n"
						for i in lines:
							copy = copy + i
							c_sock.send(i.encode())
						f.close()
						c_sock.send("\r\n".encode())
						now = time()
						ctime(now)
						index = ctime(now).find('2020')
						current_time = ctime(now)[:index] + "PDT " + ctime(now)[index:]
						dt_string = current_time+":"+c_addr[0]+":"+str(c_addr[1])+"  "+length+"; HTTP/1.0 200 OK\r\n\r\n"
						print(dt_string)
						c_sock.close()
					except FileNotFoundError:
						c_sock.send("HTTP/1.0 404 Not Found\r\n\r\n".encode())
						now = time()
						ctime(now)
						index = ctime(now).find('2020')
						current_time = ctime(now)[:index] + "PDT " + ctime(now)[index:]
						dt_string = current_time+":"+c_addr[0]+":"+str(c_addr[1])+"  "+length+"; HTTP/1.0 404 Not Found\r\n\r\n"
						print(dt_string)
						c_sock.close()
				elif command == "Connection:" and parameter == "close":
					try :
						f=open(parameter2[1:])
						
						lines=f.read()
						
						c_sock.send("HTTP/1.0 200 OK\r\n\r\n".encode())
						copy = "HTTP/1.0 200 OK\r\n\r\n"
						for i in lines:
							copy = copy + i
							c_sock.send(i.encode())
						f.close()
						c_sock.send("\r\n".encode())
						now = time()
						ctime(now)
						index = ctime(now).find('2020')
						current_time = ctime(now)[:index] + "PDT " + ctime(now)[index:]
						dt_string = current_time+":"+c_addr[0]+":"+str(c_addr[1])+"  "+length+"; HTTP/1.0 200 OK\r\n\r\n"
						print(dt_string)
						c_sock.close()
					except FileNotFoundError:
						c_sock.send("HTTP/1.0 404 Not Found\r\n\r\n".encode())
						now = time()
						ctime(now)
						index = ctime(now).find('2020')
						current_time = ctime(now)[:index] + "PDT " + ctime(now)[index:]
						dt_string = current_time+":"+c_addr[0]+":"+str(c_addr[1])+"  "+length+"; HTTP/1.0 404 Not Found\r\n\r\n"
						print(dt_string)
						c_sock.close()
				else:
					c_sock.send("HTTP/1.0 404 Not Found\r\n\r\n".encode())
					now = time()
					ctime(now)
					index = ctime(now).find('2020')
					current_time = ctime(now)[:index] + "PDT " + ctime(now)[index:]
					dt_string = current_time+":"+c_addr[0]+":"+str(c_addr[1])+"  "+length+"; HTTP/1.0 404 Not Found\r\n\r\n"
					print(dt_string)
					c_sock.close()
			else:
				c_sock.send("HTTP/1.0 400 Bad Request\r\n\r\n".encode())
				now = time()
				ctime(now)
				index = ctime(now).find('2020')
				current_time = ctime(now)[:index] + "PDT " + ctime(now)[index:]
				dt_string = current_time+":"+c_addr[0]+":"+str(c_addr[1])+"  "+user_input+"HTTP/1.0 400 Bad Request\r\n\r\n"
				print(dt_string)
				c_sock.close()
		except IndexError:
			c_sock.send("HTTP/1.0 400 Bad Request\r\n\r\n".encode())
			now = time()
			ctime(now)
			index = ctime(now).find('2020')
			current_time = ctime(now)[:index] + "PDT " + ctime(now)[index:]
			dt_string = current_time+":"+c_addr[0]+":"+str(c_addr[1])+"  "+user_input+"HTTP/1.0 400 Bad Request\r\n\r\n"
			print(dt_string)
			c_sock.close()
		except :
			try :
				f=open(parameter2[1:])
				
				lines=f.read()
				
				c_sock.send("HTTP/1.0 200 OK\r\n\r\n".encode())
				copy = "HTTP/1.0 200 OK\r\n\r\n"
				for i in lines:
					copy = copy + i
					c_sock.send(i.encode())
				f.close()
				c_sock.send("\r\n".encode())
				now = time()
				ctime(now)
				index = ctime(now).find('2020')
				current_time = ctime(now)[:index] + "PDT " + ctime(now)[index:]
				dt_string = current_time+":"+c_addr[0]+":"+str(c_addr[1])+"  "+user_input+"; HTTP/1.0 200 OK\r\n\r\n"
				print(dt_string)
				c_sock.close()
			except FileNotFoundError:
				c_sock.send("HTTP/1.0 404 Not Found\r\n\r\n".encode())
				now = time()
				ctime(now)
				index = ctime(now).find('2020')
				current_time = ctime(now)[:index] + "PDT " + ctime(now)[index:]
				dt_string = current_time+":"+c_addr[0]+":"+str(c_addr[1])+"  "+user_input+"; HTTP/1.0 404 Not Found\r\n\r\n"
				print(dt_string)
				c_sock.close()

	s.close()
	sys.exit()

if __name__ == '__main__':
	main()
		