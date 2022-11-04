import socket
import sys
import os
import re
from random import randrange
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
except:
	print ('wrong input.') 
	sys.exit()
def r_number():
	return randrange(100000)
s.bind((host_ip,port_number))


i = -1
j = -1
s_SYN='0'
s_ACK='1'
s_DAT=0
FIN="FIN"
FNF = "404 NOT FOUND"
olddata=[]
window_size = buffer_size
recive_size = payload_length
c_payload_length=0
''''data, address = s.recvfrom(2048)
if int(data.decode()) <= payload_length:
    while (True):
            i+=1
            s_SYN.append('0')
            s_ACK.append('1')
            s_DAT.append('0')
            s.sendto((s_ACK[i]).encode(),address)
            data, address = s.recvfrom(2048)
            print(data.decode())'''
while (True):
    now = time()
    ctime(now)
    index = ctime(now).find('2020')
    current_time = ctime(now)[:index] + "PDT " + ctime(now)[index:]
    try:
        data, address = s.recvfrom(2048)
    except socket.timeout:
        data, address = s.recvfrom(2048)
    i= -1
    j= -1
    if (data.decode()).isnumeric():
        if int(data.decode()) <= payload_length:
            c_payload_length=int(data.decode())
            number = r_number()
            ipar,portn = address
            while True:
                i+=1
                s_SYN="0"
                s_ACK="1"
                s_DAT=0
                s.sendto((s_ACK).encode(),address)
                try:
                    data, address = s.recvfrom(2048)
                    fname = re.findall(r'\w+', data.decode())
                    filename = fname[1] + "." + fname[2]
                    file = open(filename,'r')
                    content=file.read(c_payload_length)
                    olddata.append(content)
                    j+=1
                    s.sendto(content.encode(),address)
                    s_ACK=str(int(s_ACK)+len(content))
                    while True:
                        try:
                            data, address = s.recvfrom(2048)
                        except:
                            s.sendto(olddata[j].encode(),address)
                        content = file.read(c_payload_length)
                        olddata[j]=content
                        if data.decode()==s_ACK:
                            s.sendto(content.encode(),address)
                            s_ACK=str(int(s_ACK)+len(content))
                        elif data.decode()==FIN:
                            file.close()
                            s.sendto(FIN.encode(),address)
                            print("{time}: {ip}:{rad} GET /{fname} HTTP/1.0;HTTP/1.0 200 OK".format(time=current_time,ip=ipar,rad=number,fname=filename))
                            break;
                except:
                    s.sendto(FNF.encode(),address)
                    print("{time}: {ip}:{rad} GET /{fname} HTTP/1.0;HTTP/1.0 404 Not Found".format(time=current_time,ip=ipar,rad=number,fname=filename))
                    break;
                break;
s.close()