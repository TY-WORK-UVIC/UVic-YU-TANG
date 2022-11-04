
import socket

s=socket.socket()
s.bind(("localhost",9999))
s.listen(3)
print('waiting for connection')
while True:
    c,addr=s.accept()
    name=c.recv(1024).decode()
    print("connected with ",addr,name)
    
    
    c.send(bytes('hello, welcome','utf-8'))
    c.close()