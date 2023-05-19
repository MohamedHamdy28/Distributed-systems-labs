import socket
import time
import os
import sys
PORT = int(sys.argv[1])
BUFSIZE = 1024
sessions = {}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('localhost', PORT))
class Session:
    def __init__(self, file_size, file_name, seqno):
        self.file_size = file_size
        self.file_name = file_name
        self.seqno = seqno
        self.file_content = b''
        self.done = False
        self.last_time_active = time.time()
def handel_start(rest, addr, seqno):
    global sessions
    if sessions.get(addr) is not None:
        print("This client aready exists")
        return
    print('starting message was recieved from client: '+str(addr))
    file_name, file_size = rest.split(' | '.encode(), 1)
    print(f"File name is: {file_name}\n Total size is: {file_size}")
    file_name = file_name.decode()
    file_size = int(file_size.decode())
    s.sendto(f"a | {seqno} | {BUFSIZE}".encode(), addr)
    sessions[addr] = Session(file_size, file_name, seqno)

def handel_receiving(rest, addr, seqno):
    client_session = sessions[addr]
    if seqno == client_session.seqno - 1:
        print("Received duplicate")
        s.sendto(f"a | {client_session.seqno}".encode(), addr)
    else:
        print("data is being sent over")
        client_session.seqno += 1
        s.sendto(f"a | {client_session.seqno}".encode(), addr)
        with open(client_session.file_name, 'wb') as f:
            client_session.file_content += rest
            len_yet = len(client_session.file_content)
            print(f"Size of the data sent until now: {len_yet}, file_size = {client_session.file_size}")
            client_session.last_time_active = time.time()

            if len_yet >= client_session.file_size:
                print('File download complete=========================================================')
                f.write(client_session.file_content)
                client_session.done = True
                return

def clean():
    for key in list(sessions.keys()):
        time_spent = time.time() -sessions[key].last_time_active 
        if sessions[key].done:
            if time_spent > 1.0: # keeping the file for 1s after it was transmitted
                del sessions[key]
        elif time.time() - sessions[key].last_time_active > 3.0:
            print(f'Client was inactive for 3s, the session will be deleted {key}')
            del sessions[key]


def main():
    s.settimeout(1)
    print("Server is ready to recieve messages")
    while True:
        
        try:
            data, addr = s.recvfrom(BUFSIZE)
        except socket.timeout:
            clean()
            continue
        print(data[:20])
        prefix, rest = data.split(' | '.encode(), 1)
        print(rest[:20])
        seqno, rest = rest.split(' | '.encode(), 1)
        print(rest[:20])
        prefix = prefix.decode()
        seqno = int(seqno.decode())+1
        if prefix == 's':
            handel_start(rest, addr, seqno)
        elif prefix == 'd':
            handel_receiving(rest, addr, seqno)
if __name__ == '__main__':
    main()