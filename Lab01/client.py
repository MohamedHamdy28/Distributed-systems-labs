import socket
import os
from sys import getsizeof
import sys
import math 

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ((sys.argv[1]).split(':')[0],int((sys.argv[1]).split(':')[1]))
file_name = sys.argv[2] 
file_name_saved = sys.argv[3]
file_size = os.path.getsize(file_name)
BUFSIZE = 65536
recieved = False
seqno = 0
next_seqno = 0


def start():
    client.settimeout(0.5)
    trial = 1
    while trial < 6:
        try: 
            global BUFSIZE
            
            msg = f"s | {seqno} | {file_name_saved} | {file_size}".encode()
            client.sendto(msg, server_address)
            print("Start message was sent to the server")
            data, addr = client.recvfrom(BUFSIZE)
            data = data.decode('utf-8')
            print(data)
            prefix, rest = data.split(' | ', 1)
            global next_seqno 
            next_seqno, BUFSIZE = rest.split(' | ', 1)
            next_seqno = int(next_seqno)
            BUFSIZE = int(BUFSIZE)
            break
        except socket.timeout:
            print("Timeout happend. I will retry to connect again...")
            trial +=1
    if trial == 6:
        print("Server is malfunctioning, this program will be terminated.")
        exit()


def send_data():
    print("Sending the file now... ")
    c = True
    with open(file_name, "rb") as file: #reading chunks of the file
        while c:
            trial = 1
            while trial < 6:
                client.settimeout(0.5)
                try:    
                    if trial == 1:
                        global seqno, next_seqno
                        seqno = next_seqno
                        msg = f"d | {seqno} | ".encode()
                        msg_size = getsizeof(msg)
                        bytes_read = file.read(BUFSIZE - msg_size)
                        if not bytes_read:
                            c = False
                            print("File transmitted successfuly")
                            return
                        msg += bytes_read
                    client.sendto(msg, server_address)
                    # receiving the ack about the sent data
                    data, addr = client.recvfrom(BUFSIZE)
                    print(data.decode())
                    data = data.decode('utf-8')
                    prefix, next_seqno = data.split(' | ', 1)
                    next_seqno = int(next_seqno)
                    break
                except socket.timeout:
                    print("Timeout happend. I will retry to connect again...")
                    trial +=1
            if trial == 6:
                print("Server is malfunctioning, this program will be terminated.")
                exit()

        return


if __name__ == '__main__':
    print("Client starting...")
    start()
    send_data()
client.close()
