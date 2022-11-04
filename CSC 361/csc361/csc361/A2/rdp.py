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
    openfile = sys.argv[3]
    writefile = sys.argv[4]
except:
	print ('wrong input.') 
	sys.exit()
now = time()
ctime(now)
index = ctime(now).find('2020')
current_time = ctime(now)[:index] + "PDT " + ctime(now)[index:]
s.bind((host_ip,port_number))
s_SYN = "0"
SYN=[]
s_ACK = "1"
ACK=[]
s_DAT = 0
window_size = 2048
s_window = 2048
data = b'0'
window_size = 2048
s_window = 2048
s.settimeout(1)
#start
s.sendto(s_SYN.encode("utf-8"),('10.10.1.100',8888))
print("{time}: Send; SYN; Sequence: {seq}; Length: {dat}".format(time= current_time,seq = s_SYN, dat = s_DAT))
try:
    data, address = s.recvfrom(2048)
    if data.decode() == s_SYN:
        print("{time}: Receive; SYN; Sequence: {seq}; Length: {dat}".format(time= current_time, seq = s_SYN, dat = s_DAT))
        s.sendto(str.encode(s_ACK),('10.10.1.100',8888))
        print("{time}: Send; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_ACK, wind = s_window))
        data, address = s.recvfrom(2048)
    if data.decode() == s_ACK:
        print("{time}: Receive; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_ACK, wind = s_window))
        s_SYN = str(int(s_SYN)+1)
except socket.timeout:
    s.sendto(s_SYN.encode("utf-8"),('10.10.1.100',8888))
    print("{time}: Send; SYN; Sequence: {seq}; Length: {dat}".format(time= current_time,seq = s_SYN, dat = s_DAT))
    data, address = s.recvfrom(2048)
    if data.decode() == s_SYN:
        print("{time}: Receive; SYN; Sequence: {seq}; Length: {dat}".format(time= current_time, seq = s_SYN, dat = s_DAT))
        s.sendto(str.encode(s_ACK),('10.10.1.100',8888))
        print("{time}: Send; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_ACK, wind = s_window))
        data, address = s.recvfrom(2048)
    if data.decode() == s_ACK:
        print("{time}: Receive; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_ACK, wind = s_window))
        s_SYN = str(int(s_SYN)+1)
file = open(openfile,'r')
content = file.read(1024)
#sending...
olddata = []
r_window = 2048
i=0
count = 0
while True:
    rDATA = file.read(1024)
    olddata.append( rDATA)
    if len(rDATA) <= 0:
        break;
    count += 1
file.close()

if count<=1:
    file = open(openfile,'r')
    while True:
        DATA = file.read(1024)
        if DATA:
            s.sendto(DATA.encode("utf-8"),('10.10.1.100',8888))
            print("{time}: Send; DAT; Sequence: {seq}; Length: {dat}".format(time= current_time,seq = s_SYN, dat = len(DATA)))
            r_window-=len(DATA)
            try:
                data, address = s.recvfrom(1024)
            except socket.timeout:
                s.sendto(DATA.encode("utf-8"),('10.10.1.100',8888))
                print("{time}: Send; DAT; Sequence: {seq}; Length: {dat}".format(time= current_time,seq = s_SYN, dat = len(DATA)))
            if data.decode() == DATA: # data receive success
                print("{time}: Receive; DAT; Sequence: {seq}; Length: {dat}".format(time= current_time,seq = s_SYN, dat = len(DATA)))
                #write the data to file
                file2 = open(writefile, "r+")
                contents = file2.read().split("\n")
                file2.seek(0) 
                file2.truncate()
                file2 = open(writefile,'a')
                file2.write(data.decode())
                file2.close()
                s_SYN = str(int(s_SYN)+len(DATA))
                s_ACK = str(int(s_ACK)+len(DATA))
                s_window-=len(DATA)
                if s_window==0:
                    s_window = 1024
                s.sendto(str.encode(s_ACK),('10.10.1.100',8888))
                print("{time}: Send; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_ACK, wind = s_window))
                try:
                    data, address = s.recvfrom(1024)
                except socket.timeout:
                    s.sendto(str.encode(s_ACK),('10.10.1.100',8888))
                    print("{time}: Send; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_SYN, wind = r_window))
                if data.decode() == s_ACK:
                    print("{time}: Receive; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_ACK, wind = s_window))
        else:
            s.sendto(str.encode(s_ACK),('10.10.1.100',8888))
            print("{time}: Send; FIN; Acknowledgment: {ack}; Length: {dat}".format(time= current_time,ack = s_ACK, dat = len(DATA)))
            data, address = s.recvfrom(1024)
            if data.decode() == s_ACK:
                print("{time}: Receive; FIN; Acknowledgment: {ack}; Length: {dat}".format(time= current_time,ack = s_ACK, dat = len(DATA)))
                s_ACK = str(int(s_ACK)+len(DATA)+1)
                s.sendto(str.encode(s_ACK),('10.10.1.100',8888))
                print("{time}: Send; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_ACK, wind = window_size))
                data, address = s.recvfrom(1024)
            if data.decode() == s_ACK:
                print("{time}: Receive; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_ACK, wind = window_size))
                break;
elif count>1:
    for DATA in olddata:
        if len(DATA)<=0:
            break;
        if s_window > 0:
            s.sendto(DATA.encode("utf-8"),('10.10.1.100',8888))
            print("{time}: Send; DAT; Sequence: {seq}; Length: {dat}".format(time= current_time,seq = s_SYN, dat = len(DATA)))
            s_window -= len(DATA)
            s_SYN = str(int(s_SYN)+len(olddata[i]))
        else:
            while True:
                try:
                    data, address = s.recvfrom(1024)
                    s_SYN = s_ACK
                except socket.timeout:
                    s.sendto(DATA.encode("utf-8"),('10.10.1.100',8888))
                    print("{time}: Send; DAT; Sequence: {seq}; Length: {dat}".format(time= current_time,seq = s_SYN, dat = len(DATA)))
                finally:
                    if data.decode() in olddata:
                        print("{time}: Receive; DAT; Sequence: {seq}; Length: {dat}".format(time= current_time,seq = s_SYN, dat = len(olddata[i])))
                        count-=1
                        s_SYN = str(int(s_SYN)+len(olddata[i]))
                        r_window -= len(DATA)
                        s_ACK=str(int(s_ACK)+len(olddata[i]))
                        if r_window == 0:
                            r_window = 1024
                            s_window = 1024
                        s.sendto(str.encode(s_ACK),('10.10.1.100',8888))
                        print("{time}: Send; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_SYN, wind = r_window))
                        #write the data to file
                        file2 = open(writefile, "r+")
                        contents = file2.read().split("\n")
                        file2.seek(0) 
                        file2.truncate()
                        file2 = open(writefile,'a')
                        file2.write(data.decode())
                        file2.close()
                        try:
                            data, address = s.recvfrom(1024)
                        except socket.timeout:
                            s.sendto(str.encode(s_ACK),('10.10.1.100',8888))
                            print("{time}: Send; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_SYN, wind = r_window))
                        if data.decode() == s_ACK:
                            print("{time}: Receive; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_SYN, wind = r_window))
                        else:
                            s.sendto(str.encode(s_ACK),('10.10.1.100',8888))
                            print("{time}: Send; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_SYN, wind = r_window))
                            try:
                                data, address = s.recvfrom(1024)
                            except socket.timeout:
                                s.sendto(str.encode(s_ACK),('10.10.1.100',8888))
                            if data.decode() == s_ACK:
                                print("{time}: Receive; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_SYN, wind = r_window))
                        if s_SYN == s_ACK:
                            break;
                    if count <1:
                        break;
    while True:
        s.sendto(str.encode(s_ACK),('10.10.1.100',8888))
        print("{time}: Send; FIN; Acknowledgment: {ack}; Length: {dat}".format(time= current_time,ack = s_ACK, dat = len(DATA)))
        data, address = s.recvfrom(1024)
        if data.decode() == s_ACK:
            print("{time}: Receive; FIN; Acknowledgment: {ack}; Length: {dat}".format(time= current_time,ack = s_ACK, dat = len(DATA)))
            s_ACK = str(int(s_ACK)+len(DATA)+1)
            s.sendto(str.encode(s_ACK),('10.10.1.100',8888))
            print("{time}: Send; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_ACK, wind = window_size))
            data, address = s.recvfrom(1024)
        if data.decode() == s_ACK:
            print("{time}: Receive; ACK; Acknowledgment: {ack}; Window: {wind}".format(time= current_time,ack = s_ACK, wind = window_size))
            break;
#s.send(FIN)
#prrint("Send FIN")
#if s.receive() == FIN:
#	print("Receive FIN...")
#	s.send(ACK)
#	print("Send ACK")
#if s.receive() == ACK:
#	print("Receive ACK...")
file.close()
s.close()