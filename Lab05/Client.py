from urllib import response
import grpc
import chord_pb2 as pb2
import chord_pb2_grpc as pb2_grpc
import sys

def main():
    registry = False
    channel = None
    stub = None
    try:
        while True:
            inp = input('>')
            # connecting with either the registry or the node
            if inp[:7] == 'connect':
                addr = inp[8:]
                channel = grpc.insecure_channel(addr)
                stub = pb2_grpc.ChordServicesStub(channel)
                msg = pb2.connection_type_input()
                response = stub.connection_type(msg)
                if response.type == 'Registry':
                    registry = True
                    print("Connected to Registry")
                else:
                    registry = False
                    print(f"Connected to Node")
            # calling the node to save a key and text
            if inp[:4] == 'save':
                if not registry:
                    key = inp[6:inp.find('”')]
                    text = inp[inp.find('”')+2:]
                    msg = pb2.save_input(key=key, text=text)
                    response = stub.save(msg)
                    if response.state:
                        print(f'{response.state}, {key} is saved in node {response.message}')
                    else:
                        print(f'{response.state}, {key} is already exist in node {response.message}')
                else:
                    print('You are not connected with a node')
            # calling the node to remove a key and text
            elif inp[:6] == 'remove':
                if not registry:
                    key = inp[7:]
                    msg = pb2.remove_input(key=key)
                    response = stub.remove(msg)
                    if response.state:
                        print(f'True, {key} is removed from node {response.message}')
                    else:
                        print(f'False, {response.message}')
                else:
                    print('You are not connected with a node')
            # calling the node to find a key and text
            elif inp[:4] == 'find':
                if not registry:
                    key = inp[5:]
                    msg = pb2.find_input(key=key)
                    response = stub.find(msg)
                    print(response.message)
                else:
                    print('You are not connected with a node')
            elif inp[:8] == 'get_info':
                # getting info about the chord from the registry
                if registry:
                    msg = pb2.gci_input()
                    response = stub.get_chord_info(msg)
                    for item in response.info:
                        id = int(item[1:item.find(',')])
                        addr = item[item.find(',')+2:]
                        addr = addr[:-1]
                        print(f'{id}: {addr}')
                # getting info about the node we are connecting with
                else:
                    msg = pb2.gft_input()
                    response = stub.get_finger_table(msg)
                    print(f'Node id: {response.id}')
                    for item in response.finger_table:
                        id = int(item[1:item.find(',')])
                        addr = item[item.find(',')+2:]
                        addr = addr[:-1]
                        print(f'{id}: {addr}')
            # quiting the program
            elif inp[:4] == 'quit':
                print('Terminating')
                sys.exit(0)
    except KeyboardInterrupt:
        print('Terminating')
        sys.exit(0)
                
                

        
            
if __name__ == '__main__':
    main()