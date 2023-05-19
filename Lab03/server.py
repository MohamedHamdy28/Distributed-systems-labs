from multiprocessing import context
import zmq
import time
import sys
import os

port1 = int(sys.argv[1]) # client input
port2 = int(sys.argv[2]) # client ouptut
port3 = int(sys.argv[3]) # worker input 
port4 = int(sys.argv[4]) # worker output


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port1)

context2 = zmq.Context()
clients_pub = context2.socket(zmq.PUB)
clients_pub.bind("tcp://*:%s" % port2)

context3 = zmq.Context()
worker_pub = context.socket(zmq.PUB)
worker_pub.bind("tcp://*:%s" % port3)

context4 = zmq.Context()
worker_sub = context.socket(zmq.SUB)
worker_sub.bind("tcp://*:%s" % port4)
worker_sub.setsockopt_string(zmq.SUBSCRIBE, '')
try:
    while True:
        # receiving messages from client input
        message = socket.recv()
        print(f"Received request: {message}")
        socket.send(f"Message received {port1}".encode())
        # receiving messages from workers
        if message.decode()[:7] == 'isprime'  or message.decode()[:3] == 'gcd':
            # forwarding messages to workers channels
            worker_pub.send(message)
            print("found keywords")
            try:
                workers_message = worker_sub.recv_string()
                print(workers_message)
            except zmq.ZMQError:
                continue
            except KeyboardInterrupt:
                os._exit(0)
            except:
                continue
            clients_pub.send(workers_message.encode())
        else:
            clients_pub.send(message)
except KeyboardInterrupt:
    os._exit(0)
    


    