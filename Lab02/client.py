# echo-client.py

import socket
import sys

SERVER = ((sys.argv[1]).split(':')[0],int((sys.argv[1]).split(':')[1]))

numbers = [15492781, 15492787, 15492803,
15492811, 15492810, 15492833,
15492859, 15502547, 15520301,
15527509, 15522343, 1550784]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect(SERVER)
        print(f"Connected to {SERVER}")
        for num in numbers:
            s.send(str(num).encode())
            data = s.recv(102400)
            print(f"{num} {data.decode()}")
        print("Completed")
    except:
        print("Server is unavaliable")