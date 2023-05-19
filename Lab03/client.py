import zmq
import sys
from threading import Thread
import os

port = sys.argv[1]
port2 = sys.argv[2]


context = zmq.Context()
client_input = context.socket(zmq.REQ)
client_input.connect("tcp://localhost:%s" % port)

context2 = zmq.Context()
client_output = context2.socket(zmq.SUB)
client_output.connect("tcp://localhost:%s" % port2)
client_output.setsockopt(zmq.SUBSCRIBE, b'')
client_output.RCVTIMEO = 100


try:
    try:
        while True:
            line = input("> ")
            if len(line) != 0:
                client_input.send(line.encode())
                client_input.recv()
            try:
                msg = client_output.recv_string()
                if len(msg) != 0:
                    print(msg)
            except zmq.Again:
                continue
            except KeyboardInterrupt:
                print("Terminating client")
                os._exit(0)
    except KeyboardInterrupt:
        print("Terminating client")
        os._exit(0)
except KeyboardInterrupt:
    print("Terminating client")
    os._exit(0)
    
    
    