import zmq
import sys
from threading import Thread
import os


port = sys.argv[1]
port2 = sys.argv[2]


context = zmq.Context()
worker_input = context.socket(zmq.SUB)
worker_input.connect("tcp://localhost:%s" % port)
worker_input.setsockopt_string(zmq.SUBSCRIBE, 'gcd')
worker_input.RCVTIMEO = 100

context2 = zmq.Context()
worker_output = context2.socket(zmq.PUB)
worker_output.connect("tcp://localhost:%s" % port2)

def hcfnaive(a, b):
    if(b == 0):
        return abs(a)
    else:
        return hcfnaive(b, a % b)
try:
    while True:
        try:
            msg = worker_input.recv_string()
        except zmq.Again:
            continue
        try:
            nums = msg[4:]
            num1, num2 = nums.split(' ')
            result = hcfnaive(int(num1), int(num2))
            worker_output.send(f"gcd for {num1} {num2} is {result}".encode())
        except:
            continue
except KeyboardInterrupt:
    print("Terminating worker")
    os._exit(0)
    
    
    