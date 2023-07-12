import select
import socket
import sys
import queue
import time
import re


from socket import *

s=socket(AF_INET, SOCK_STREAM)
s.bind(("",9000))
s.listen(5)
print('waiting for connection')
while True:
    c,a=s.accept()
    print("Received from ",a)
    c.send("hello, welcome")


    s.close()