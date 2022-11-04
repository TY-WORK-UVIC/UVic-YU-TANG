import select
import socket
import sys
import queue
import time
import re
import os.path
from time import gmtime, strftime
import codecs
import __main__ as main
import os
time1=strftime("%a %b %d %H:%M:%S %Z %Y:", gmtime())   #Time header 
temp=[]                                                # Few glboal variables to store data 
final=[]
connection_type=" "
correct_f=re.compile("GET .+ HTTP/1.0")                       # Three formats 
C2=re.compile("Connection\: ?keep-alive",re.IGNORECASE)   
C3=re.compile("Connection\: ?close",re.IGNORECASE)
time_list=[]
temp2=[]
Header_close='Connection: Close'                          # Three headers for printing out 
Header_alive='Connection: Keep-alive' 
empty_line="\r\n\r\n"
def check_for_format_GET(msg):                   #Check if the GET format is right 
    if correct_f.search(msg)!=None:
        return True
    else:
        return False

def check_for_format_CON_alive(msg):            # Check if the connection: keep-alive is correct
    if C2.search(msg)!=None:
        return True
    else:
        return False
    
def check_for_format_CON_close(msg):          # Check if the connection: close is correct
    if C3.search(msg)!=None:
        return True
    else:
        return False  

def file_name(msg):                             #Find the file name
    filelname=re.split('/', msg)[1]
    filelname=re.split(' ', filelname)[0]
    return filelname


def File_exist(a_connetion,filename,outputs,line,inputs,s,b_login,request_line): # When the file exist 
    global temp                    # Few global variables
    global connection_type         # Time list store the print message for server
    global time_list               #Temp store all the input
    global temp2
    if(connection_type!= " "):    # When the connection_type is not empty, it means Either close or keep-alive
        final_connection_type=re.split(":",connection_type)[1].strip().lower()
        if(final_connection_type!="close"):    # If connection_type is not close, store all the require message in to output 
            outputs.append('HTTP/1.0 200 OK\n')
            outputs.append(Header_alive)
            outputs.append(empty_line)
            outputs.append(line)
            final_time=time1+str(b_login[0])+":"+str(b_login[1])+" "+request_line+";"+' HTTP/1.0 200 OK' #The message print from server
            time_list.append(final_time)
            temp2.clear()
            connection_type=" "
        elif(final_connection_type=="close"): # If connection_type is close, store all the require message in to output
            outputs.append('HTTP/1.0 200 OK\n')
            outputs.append(Header_close)
            outputs.append(empty_line)
            outputs.append(line)
            connection_type="Close"           # Set connection_type=close 
            final_time=time1+str(b_login[0])+":"+str(b_login[1])+" "+request_line+";"+' HTTP/1.0 200 OK'  #The message print from server
            time_list.append(final_time)
            temp2.clear()
            
    else:
        outputs.append('HTTP/1.0 200 OK\n') #If connection_type is empty, it means we handle the request then close the connection 
        outputs.append(Header_close)
        outputs.append(empty_line)
        outputs.append(line)
        connection_type="Close"   # Set connection_type=close
        final_time=time1+str(b_login[0])+":"+str(b_login[1])+" "+request_line+";"+' HTTP/1.0 200 OK'
        time_list.append(final_time)  # Add the message in to list
        temp2.clear()
    return outputs

def File_not_exist(a_connetion,filename,outputs,inputs,s,b_login,request_line): # When the file not exist 
    global temp                  # Few global variables
    global connection_type       #Temp store all the input
    global time_list             # Time list store the print message for server
    global temp2
    if(connection_type!= " "):  # When the connection_type is not empty, it means Either close or keep-alive
        final_connection_type=re.split(":",connection_type)[1].strip().lower()
        if(final_connection_type!="close"):    # If connection_type is not close, store all the require message in to output 
            outputs.append('HTTP/1.0 404 Not Found\n')
            outputs.append(Header_alive)
            outputs.append(empty_line)
            final_time=time1+str(b_login[0])+":"+str(b_login[1])+" "+request_line+";"+' HTTP/1.0 404 Not Found' #The message print from server
            time_list.append(final_time)
            temp2.clear()
            connection_type=" "
        elif(final_connection_type=="close"):  # If connection_type is close, store all the require message in to output
            outputs.append('HTTP/1.0 404 Not Found\n')
            outputs.append(Header_close)
            outputs.append(empty_line)
            connection_type="Close"        # Set connection_type=close
            final_time=time1+str(b_login[0])+":"+str(b_login[1])+" "+request_line+";"+' HTTP/1.0 404 Not Found'
            time_list.append(final_time)
            temp2.clear()
            
    else:
        outputs.append('HTTP/1.0 404 Not Found\n')  #If connection_type is empty, it means we handle the request then close the connection 
        outputs.append(Header_close)
        connection_type="Close"         # Set connection_type=close
        final_time=time1+str(b_login[0])+":"+str(b_login[1])+" "+request_line+";"+' HTTP/1.0 404 Not Found'
        time_list.append(final_time)   # Add the message in to list
        temp2.clear() 
    return outputs                  

def check_exist(a_connetion,filename,outputs,inputs,s,b_login,request_line): #Check if the file exist 
    global temp             # Few global variables
    global connection_type   #Temp store all the input
    global temp2
    file_exists = os.path.exists(filename)
    if file_exists is True:                 # If the file exist, open and read file 
        f=codecs.open(filename, "r", "utf-8")
        line=f.read()                 
        outputs=File_exist(a_connetion,filename,outputs,line,inputs,s,b_login,request_line) # File exist go to File_exist to handle request 
    else:
        # File does not exist, go to File_not_exist
        outputs=File_not_exist(a_connetion,filename,outputs,inputs,s,b_login,request_line)    

    return outputs
def correct_format(s,a_connetion,temp,b_login,outputs,inputs): # Check if GET message is in the right format 
    global connection_type
    global time_list
    global temp2
    for line in temp:
        if(line!=''):
            if(line[0].lower()=="g"):
                if(check_for_format_GET(line)==True): # If it is in right format, find the file name 
                    file1=file_name(line)
                    outputs=check_exist(a_connetion,file1,outputs,inputs,s,b_login,line) # Use check_exist to check if file exist 
                    print(1)
                else:              #If it is not in right format, store the require message then close 

                    outputs.append('HTTP/1.0 400 Bad request\n') # Store require messages 
                    outputs.append(Header_close)
                    outputs.append(empty_line)
                    connection_type="Close"             # Set connection_type to close 
                    final_time=time1+str(b_login[0])+":"+str(b_login[1])+" "+line+";"+' HTTP/1.0 400 Bad request'
                    time_list.append(final_time)
                    temp2.clear()
                
  
    return outputs
        
     
def handle_output(temp,s,a_connetion,b_login,outputs,inputs): # Receive input from s.recv(), then read them line by line 
    global connection_type
    global final
    for a in temp:
        print(f"a",a)
        temp2.append(a)
        if(a!='' and a[0].lower()=="c"):            #Check format of connection type and set connection type
            if(check_for_format_CON_alive(a)==True):
                connection_type=a
                print("alive")
            elif(check_for_format_CON_close(a)==True):
                connection_type=a
                print("close")    
            else:
                print("not correct format")         #If it is not in correct format, set connection type to None

        if(a==''):
            final=correct_format(s,a_connetion,temp2,b_login,outputs,inputs) # When it receive an empty line, it means we have one complete request then we can
        if(connection_type=="Close"):                                        # process it in serveral functions step by step
            break            #If connection_type is close, break the function immediately 
    #return final

def print_outputs(a_connetion,inputs,outputs,s):   #Print out the data in outputs and time_list
    global connection_type
    global time_list
    global final
    if(final!=[]):          #Insure there is data in list final is final list with all the require messages that we should send to client
        for line in final:
            a_connetion.send(bytes(str(line),'utf-8')) #Send all the messages to client 
            print(line)
                        
            
        for t in time_list:   #Print all the data in server 
            print(t)
        outputs.clear()
        time_list.clear()
        if(connection_type=="Close"): #Check connnection status, if it is close, close the connection, if not continue 
            inputs.remove(s)
            a_connetion.close()
            connection_type=" "      #Set connection_type to None because we already close connection, means we have to handle new request 
def main():
    host=sys.argv[1]                #Get data from command line ip_address and port number 
    ip_address=sys.argv[2]
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Basic socket requirments
    server.setblocking(0)
    server.bind((host, int(ip_address)))
    server.listen(5)
    inputs = [server]
    outputs = []
    
   
    global temp                   #few global variables
    global temp2
    global connection_type
    global time_list
    global final
    response_messages = {}
    request_message = {}

    print("Listening...")
    #print(f"server", server)
    while True:

        readable, writable, exceptional = select.select(inputs, outputs, inputs) # Select the data we need 
        print(" ")
        print(f"inputs ", inputs)
        print(f"readable ", readable)
        print(f"writable ", writable)
        print(f"exceptional ", exceptional)
        print(" ")
        #server.settimeout(5)
        if not (readable or writable or exceptional):
            #inputs.remove(s)
            server.close()
            #print('  timed out, do some other work here', file=sys.stderr)
            continue
        #print(f"inputs ", inputs)
        #print(f"readable ", readable)
        #print(f"writable ", writable)
        print(f"exceptional ", exceptional)
        for s in readable:
            if (s==server):                 # Capture the data we need 
    
                a_connetion,b_login=s.accept()    
                inputs.append(a_connetion)
                
            else:
                #print (sys.flags.interactive)
                
                msg = s.recv(1024).decode() # Receive messages from client 
                print(f"msg",msg)
                print(" ")
                
                temp=re.split("\n\n",msg)  # Split the message so it is line by line 
                temp=re.split("\n",msg)
                
                #print(f"temp[1]", temp[1])
                if(temp[1]==''):          #Remove the ending empty line 
                    temp.remove('')
  
                    
                handle_output(temp,s,a_connetion,b_login,outputs,inputs) #Handle the data receive from client 
                print_outputs(a_connetion,inputs,outputs,s)          #Print out the messages in outputs and time_list
                #f(final!=[]): 
                 #  for line in final:
                  #     a_connetion.send(bytes(str(line),'utf-8'))
                  #     print(line)
                        
                    #time=strftime("%a, %b %d %Z %Y %H:%M:%S:", gmtime()),b_login[0],temp[0].strip()+";"+' HTTP/1.0 400 Bad request'
                  # for t in time_list:
                  #     print(t)
                  # outputs.clear()
                  # time_list.clear()
                  # if(connection_type=="Close"):
                  #     inputs.remove(s)
                  #     a_connetion.close()
                  #     connection_type=" "
              
                
                
                
if __name__ == "__main__":
    main()