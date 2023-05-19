import zmq
import sys
from threading import Thread
import os

port = sys.argv[1]
port2 = sys.argv[2]


context = zmq.Context()
print ("Connecting to server...")
worker_input = context.socket(zmq.SUB)
worker_input.connect("tcp://localhost:%s" % port)
worker_input.setsockopt_string(zmq.SUBSCRIBE, 'isprime')
worker_input.RCVTIMEO = 100

context2 = zmq.Context()
worker_output = context2.socket(zmq.PUB)
worker_output.connect("tcp://localhost:%s" % port2)

def is_prime(n):
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    for divisor in range(3, n, 2):
        if n % divisor == 0:
            return False
    return True
try:
    while True:
        try:
            msg = worker_input.recv_string()
        except zmq.Again:
            continue
        try:
            num = int(msg[7:])
            print(num)
            if is_prime(num):
                worker_output.send(f"{num} is prime".encode())
            else:
                worker_output.send(f"{num} is not prime".encode())
        except:
            continue
except KeyboardInterrupt:
    print("Terminating worker")
    os._exit(0)
    
    
    