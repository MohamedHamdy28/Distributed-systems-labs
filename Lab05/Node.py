from cgitb import text
from genericpath import exists
from urllib import response
import grpc
import chord_pb2 as pb2
import chord_pb2_grpc as pb2_grpc
import sys
import zlib
from concurrent import futures
import time


# Global variables
REGISTRY_ADDR = ((sys.argv[1]).split(':')[0],int((sys.argv[1]).split(':')[1]))
MY_ADDR = ((sys.argv[2]).split(':')[0],int((sys.argv[2]).split(':')[1]))
MY_ID = None
M = None
MY_FINGER_TABLE = []
PREDECESSOR = None
SUCCESSOR = None
SUCCESSOR_ADDR = None
IDS = []
DATA = {}

# Class to handle the grpc functions
class ChordServicesHandler(pb2_grpc.ChordServicesServicer):

    # Saves the key and the text on the corresponding node.
    def save(self, request, context):
        key = request.key
        text = request.text
        print(f'Save id {key}')
        if key.isalpha():
            hash_value = zlib.adler32(key.encode())
            target_id = hash_value % 2 ** M
        else:
            target_id = int(key)
        target = lookup(target_id)
        if target == MY_ID:
            if target_id in DATA:
                reply = {
                'state': False,
                'message': str(MY_ID)
                }
                return pb2.save_output(**reply)
            else:
                DATA[target_id] = text
                reply = {
                    'state': True,
                    'message': str(MY_ID)
                }
                return pb2.save_output(**reply)
        else:
            for item in MY_FINGER_TABLE:
                if item[0] == target:
                    # connecting with the target node
                    channal = grpc.insecure_channel(item[1])
                    stub = pb2_grpc.ChordServicesStub(channal)
                    msg = pb2.save_input(key=request.key, text=request.text)
                    response = stub.save(msg)
                    reply = {
                    'state': response.state,
                    'message': response.message
                    }
                    return pb2.save_output(**reply)


    # Similar to the save method. But removes the key and the text from the corresponding node.                
    def remove(self, request, context):
        key = request.key
        hash_value = zlib.adler32(key.encode())
        target_id = hash_value % 2 ** M
        target = lookup(target_id)
        if target == MY_ID:
            if target_id in DATA:
                del DATA[target_id]
                reply = {
                'state': True,
                'message': str(MY_ID)
                }
                return pb2.save_output(**reply)
            else:
                reply = {
                    'state': False,
                    'message': "the key you are trying to remove doesn't exists"
                }
                return pb2.save_output(**reply)
        else:
            for item in MY_FINGER_TABLE:
                if item[0] == target:
                    # connecting with the target node
                    channal = grpc.insecure_channel(item[1])
                    stub = pb2_grpc.ChordServicesStub(channal)
                    msg = pb2.remove_input(key=request.key)
                    response = stub.remove(msg)
                    reply = {
                    'state': response.state,
                    'message': response.message
                    }
                    return pb2.remove_output(**reply)


    # Find the node, the key and the text should be saved on.
    def find(self, request, context):
        key = request.key
        hash_value = zlib.adler32(key.encode())
        target_id = hash_value % 2 ** M
        target = lookup(target_id)
        if target == MY_ID:
            if target_id in DATA:
                reply = {
                'state': True,
                'id': MY_ID,
                'addr': f"{MY_ADDR[0]}:{MY_ADDR[1]}",
                'message': f"True, {key} is saved in node {MY_ID}"
                }
                return pb2.find_output(**reply)
            else:
                reply = {
                'state': False,
                'id': MY_ID,
                'addr': f"{MY_ADDR[0]}:{MY_ADDR[1]}",
                'message': f"False, {key} does not exist in node {MY_ID}"
                }
                return pb2.find_output(**reply)
        else:
            for item in MY_FINGER_TABLE:
                if item[0] == target:
                    # connecting with the target node
                    channal = grpc.insecure_channel(item[1])
                    stub = pb2_grpc.ChordServicesStub(channal)
                    msg = pb2.find_input(key=request.key)
                    response = stub.find(msg)
                    reply = {
                    'state': response.state,
                    'id': response.id,
                    'addr': response.addr,
                    'message': response.message
                    }
                    return pb2.find_output(**reply)


    # deligate the ids that the node is holding to the new node which has the right to hold these ids
    def deligate_ids(self, request, context):
        ids = request.ids
        keys = []
        texts = []
        for id in ids:
            if id in DATA:
                keys.append(id)
                texts.append(str(DATA[id]))
                del DATA[id]
        reply = {
            'key': keys,
            'text': list(texts),
        }
        return pb2.deligate_output(**reply)
    

    # This method is called by the client to know that it is connected with a node
    def connection_type(self, request, context):
        reply = {
            'type': 'Node'
        }
        return pb2.connection_type_output(**reply)

    # This method returns the finger table of the node
    def get_finger_table(self, request, context):
        ft = []
        for item in MY_FINGER_TABLE:
            ft.append(f'({item[0]}, {item[1]})')
        reply = {
            'id': MY_ID,
            'finger_table': ft
        }
        return pb2.gft_output(**reply)


# This method is responsible for calling the deregister method of the Registry to quit
# the chord and then shut down the Node.
def quit():
    channel = grpc.insecure_channel(f'{REGISTRY_ADDR[0]}:{REGISTRY_ADDR[1]}')
    stub = pb2_grpc.ChordServicesStub(channel)
    msg = pb2.deregister_input(id=MY_ID)
    response = stub.deregister(msg)
    # wait for 1.5 sec to make sure that the finger tables for all nodes are updated
    time.sleep(1.5)
    # connect to successor and save the ids this node had
    channel = grpc.insecure_channel(SUCCESSOR_ADDR)
    stub = pb2_grpc.ChordServicesStub(channel)
    for key in list(DATA.keys()):
        msg = pb2.save_input(key=str(key), text=str(DATA[key]))
        response = stub.save(msg)
        print(response.message)
        

# This function helps to extract the ids and addresses from the finger table
def extract_table(table):
    global IDS
    finger_table = []
    for item in table:
        id = int(item[1:item.find(',')])
        addr = item[item.find(',')+2:]
        addr = addr[:-1]
        finger_table.append((id, addr))
        IDS.append(id)
    return finger_table

# This method is used to get the closest preceding node for a given id
# it is helpful when we do lookups 
def get_closest_preceding_node(k):
    search_space = [i for i in reversed(range(0,k))]
    search_space.extend([i for i in reversed(range(k, 2**M))])
    for i in search_space:
        if i in IDS:
            return i # found the predecessor
            

# This funciton carry out the lookup procedure explained in the assigment file. 
def lookup(k):
    if PREDECESSOR > MY_ID:
        if k <= MY_ID or k > PREDECESSOR:
            return MY_ID
    elif k in range(PREDECESSOR + 1, MY_ID +1):
        return MY_ID
    if SUCCESSOR < MY_ID:
        if k > MY_ID or k <= SUCCESSOR:
            return SUCCESSOR
    elif k in range(MY_ID+1, SUCCESSOR+1):
        return SUCCESSOR
    return get_closest_preceding_node(k)


# this function request the ids that the node should be holding from its successor
# it is called as soon as the node enter the chord
def request_ids():
    if SUCCESSOR != MY_ID:
        ids = []
        if PREDECESSOR > MY_ID:
            ids = [i for i in reversed(range(0,MY_ID+1))]
            ids.extend([i for i in reversed(range(PREDECESSOR+1, 2**M))])
        else:
            ids = [i for i in reversed(range(PREDECESSOR+1, MY_ID+1))]
        # asking the successor for those ids
        channal = grpc.insecure_channel(SUCCESSOR_ADDR)
        stub = pb2_grpc.ChordServicesStub(channal)
        msg = pb2.deligate_input(ids=ids)
        response = stub.deligate_ids(msg)
        keys = response.key
        texts = response.text
        for k in keys:
            DATA[k] = texts
    


def main():
    global MY_ID, M, PREDECESSOR, SUCCESSOR, MY_FINGER_TABLE, SUCCESSOR_ADDR
    # connecting with the registry
    channel = grpc.insecure_channel(f'{REGISTRY_ADDR[0]}:{REGISTRY_ADDR[1]}')
    stub = pb2_grpc.ChordServicesStub(channel)

    # Register the node
    msg = pb2.register_input(ipaddr=MY_ADDR[0], port=str(MY_ADDR[1]))
    response = stub.register(msg) # response should be the id and m
    MY_ID = response.id
    M = int(response.m)

    # get the node's finger table to know it's successor
    msg = pb2.pft_input(id=MY_ID)
    response = stub.populate_finger_table(msg)
    PREDECESSOR = response.predecessor
    MY_FINGER_TABLE = extract_table(response.finger_table)
    SUCCESSOR = MY_FINGER_TABLE[0][0]
    SUCCESSOR_ADDR = MY_FINGER_TABLE[0][1]
    print(f'predecessor = {PREDECESSOR}, my id = {MY_ID}, successor = {SUCCESSOR}')
    request_ids()

    # from here the node will start to act as a server so that the client can connect with it
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ChordServicesServicer_to_server(
        ChordServicesHandler(), server)
    server.add_insecure_port(f'{MY_ADDR[0]}:{MY_ADDR[1]}')
    server.start()
    while True:
        try:
            # calling populate_finger_table() every 1 sec
            x = server.wait_for_termination(1)
            if x:
                msg = pb2.pft_input(id=MY_ID)
                response = stub.populate_finger_table(msg)
                PREDECESSOR = response.predecessor
                MY_FINGER_TABLE = extract_table(response.finger_table)
                SUCCESSOR = MY_FINGER_TABLE[0][0]
        except grpc.RpcError:
            print("Registry terminated")
            sys.exit(0)
        except KeyboardInterrupt:
            # transfer data to the node's successor before leaving the program
            print("Shutting down")
            quit()
            sys.exit(0)


if __name__ == '__main__':
    main()