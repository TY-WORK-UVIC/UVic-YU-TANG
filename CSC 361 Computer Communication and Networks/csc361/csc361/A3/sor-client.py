import socket
import sys
import os
from time import time, ctime

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print ('Socket could not be created.') 
	sys.exit()
try:
    host_ip = sys.argv[1]
    port_number = int(sys.argv[2])
    buffer_size = int(sys.argv[3])
    payload_length = int(sys.argv[4])
    openfile = sys.argv[5]
    writefile = sys.argv[6]
except:
	print ('wrong input.') 
	sys.exit()
	
now = time()
ctime(now)
index = ctime(now).find('2020')
current_time = ctime(now)[:index] + "PDT " + ctime(now)[index:]
s.settimeout(1)

s_SYN = "0"
s_ACK = "1"
c_ACK = "1"
s_DAT = 0
FIN = "FIN"
FNF = "404 NOT FOUND"
content=""
window_size = buffer_size
recive_size = payload_length
data=b""

s.sendto(str(payload_length).encode(),(host_ip,port_number))
print("{time}: Send; SYN; Sequence: {seq}; Length: {dat}; Acknowledgment: -1; Window: {win}".format(time= current_time,seq = s_SYN, dat = s_DAT,win = window_size))
try:
	data, address = s.recvfrom(2048)
except socket.timeout:
    s.sendto(str(payload_length).encode(),(host_ip,port_number))
    print("{time}: Send; SYN; Sequence: {seq}; Length: {dat}; Acknowledgment: -1; Window: {win}".format(time= current_time,seq = s_SYN, dat = s_DAT,win = window_size))
if data.decode() == s_ACK:
    while True:
        print("{time}: Receive; SYN|ACK; Sequence: {seq}; Length: {dat}; Acknowledgment: {ack}; Window: {win}".format(time= current_time,seq = s_SYN, dat = s_DAT,ack=s_ACK,win = window_size))
        s_SYN = s_ACK
        DATA="\r\nGET /{file} HTTP/1.0Connection: keep-alive\r\n".format(file=openfile)
        s_DAT=len(DATA)
        c_ACK =str(s_DAT+int(s_ACK))
        s.sendto(DATA.encode(),(host_ip,port_number))
        print("{time}: Send; DAT|ACK; Sequence: {seq}; Length: {dat}; Acknowledgment: {ack}; Window: {win}".format(time= current_time,seq = s_SYN, dat = s_DAT,ack=s_ACK,win = window_size))
        break;
i=0
if data!=b"":
    while True:
        try:
            data, address = s.recvfrom(2048)
        except socket.timeout:
            s.sendto(s_ACK.encode(),(host_ip,port_number))
            print("{time}: Send; ACK; Sequence: {seq}; Length: {dat}; Acknowledgment: {ack}; Window: {win}".format(time= current_time,seq = c_ACK, dat = 0,ack=s_ACK,win = window_size))
        if len(data.decode()) == payload_length:
            s_DAT=len(data.decode())
            print("{time}: Receive; DAT|ACK; Sequence: {seq}; Length: {dat}; Acknowledgment: {ack}; Window: {win}".format(time= current_time,seq = s_SYN, dat = s_DAT,ack=c_ACK,win = window_size))
            content = content+data.decode()
            s_ACK =str(s_DAT+int(s_ACK))
            s_SYN = str(int(s_SYN)+len(data.decode()))
            s.sendto(s_ACK.encode(),(host_ip,port_number))
            print("{time}: Send; ACK; Sequence: {seq}; Length: {dat}; Acknowledgment: {ack}; Window: {win}".format(time= current_time,seq = c_ACK, dat = 0,ack=s_ACK,win = window_size))
        elif len(data.decode()) < payload_length:
            s_DAT=len(data.decode())
            print("{time}: Receive; DAT|ACK; Sequence: {seq}; Length: {dat}; Acknowledgment: {ack}; Window: {win}".format(time= current_time,seq = s_SYN, dat = s_DAT,ack=c_ACK,win = window_size))
            content = content+data.decode()
            file2 = open(writefile, "r+")
            contents = file2.read().split("\n")
            file2.seek(0) 
            file2.truncate()
            file2 = open(writefile, "a")
            file2.write(content)
            file2.close()
            s_ACK =str(s_DAT+int(s_ACK))
            s_SYN = str(int(s_SYN)+len(data.decode()))
            print("{time}: Send; ACK; Sequence: {seq}; Length: {dat}; Acknowledgment: {ack}; Window: {win}".format(time= current_time,seq = c_ACK, dat = 0,ack=s_ACK,win = window_size- s_DAT))
            s.sendto(FIN.encode(),(host_ip,port_number))
            print("{time}: Send; FIN; Sequence: {seq}; Length: {dat}; Acknowledgment: {ack}; Window: {win}".format(time= current_time,seq = c_ACK, dat = 0,ack=s_ACK,win = window_size))
            break;
    while True:
        try:
            data, address = s.recvfrom(2048)
        except socket.timeout:
            s.sendto(FIN.encode(),(host_ip,port_number))
            print("{time}: Send; FIN; Sequence: {seq}; Length: {dat}; Acknowledgment: {ack}; Window: {win}".format(time= current_time,seq = c_ACK, dat = 0,ack=s_ACK,win = window_size))
        if (data.decode() == FIN) | (data.decode() == FNF):
            print("{time}: Receive; FIN|ACK; Sequence: {seq}; Length: {dat}; Acknowledgment: {ack}; Window: {win}".format(time= current_time,seq = s_SYN, dat = 0,ack=str(int(c_ACK)+1),win = window_size))
            s.sendto(FIN.encode(),(host_ip,port_number))
            print("{time}: Send; ACK; Sequence: {seq}; Length: {dat}; Acknowledgment: {ack}; Window: {win}".format(time= current_time,seq = str(int(c_ACK)+1), dat = 0,ack=str(int(s_SYN)+1),win = window_size))
            break;
s.close()