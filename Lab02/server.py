import socket
import time
from threading import Thread
from multiprocessing import Queue
import os
import sys

HOST = "127.0.0.1"
PORT = int(sys.argv[1])
q = Queue()

def is_prime(n):
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    for divisor in range(3, n, 2):
        if n % divisor == 0:
            return False
    return True
def worker():
    while True:
        while not q.empty():
            conn, addr = q.get()
            print(f"{addr} connected")
            while True:
                data = conn.recv(160000)
                if data:
                    result = is_prime(int(data.decode()))
                    if result:
                        conn.send("is prime".encode())
                    else:
                        conn.send("is not prime".encode())
                else:
                    print(f"{addr} disconnected")
                    conn.close()
                    break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        t1 = Thread(target=worker)
        t2 = Thread(target=worker)
        t3 = Thread(target=worker)
        t1.start()
        t2.start()
        t3.start()
        try:
            while True:
                conn, addr = s.accept() 
                global q
                q.put((conn,addr),block=True)
        except KeyboardInterrupt:
            print("\nShutting down")
            print("Done")
            os._exit(0)

if __name__ == '__main__':
    main()