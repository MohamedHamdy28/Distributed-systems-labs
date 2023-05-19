import grpc
import chord_pb2 as pb2
import chord_pb2_grpc as pb2_grpc
import sys
import random
from concurrent import futures




# Global variables
M = int(sys.argv[2])
CHORD_LEN = 2**M
CHORD_SEQUENCE = [0 for i in range(0,CHORD_LEN)] # keeping track of registered nodes
CHORD_COUNT = 0
MY_ADDR = ((sys.argv[1]))

# Class to hold the attributes of a node
class Node:
    def __init__(self, id, ipaddr, port,successor=None, predecessor=None):
        self.successor = successor
        self.predecessor = predecessor
        self.id = id
        self.ipaddr = ipaddr
        self.port = port

# This function finds the successor and predecessor for a given id using the methods explained in the lecture
def find_neighbors(id):
    successor = None
    predecessor = None
    for j in range(1, CHORD_LEN+1):
        i = (id + j) % CHORD_LEN
        if CHORD_SEQUENCE[i] != 0:
            successor = CHORD_SEQUENCE[i]
            break
    search_space = [i for i in reversed(range(0,id))]
    search_space.extend([i for i in reversed(range(id, CHORD_LEN))])
    for i in search_space:
        if CHORD_SEQUENCE[i] != 0:
            predecessor = CHORD_SEQUENCE[i]
            break
    return successor, predecessor


# Handling the functions of the grpc
class ChordServicesHandler(pb2_grpc.ChordServicesServicer):

    # This method is invoked by a new node to register itself. It is responsible to register
    # the node with given ipaddr and port.
    def register(self, request, context):
        ipaddr = request.ipaddr
        port = request.port
        random.seed(0)
        global CHORD_COUNT
        # If the chord is empty
        if CHORD_COUNT == 0:
            id = random.randint(0,(CHORD_LEN)-1)
            node = Node(id=id, ipaddr=ipaddr, port=port)
            node.successor = node
            node.predecessor = node
            CHORD_COUNT += 1
            CHORD_SEQUENCE[id] = node
            reply = {
                'id': id,
                'm': f'{M}'
            }
            return pb2.register_output(**reply)
        # when the chord is full
        elif CHORD_COUNT == CHORD_LEN:
            reply = {
                'id': -1,
                'm': "The chord is currently full"
            }
            print("Can't assign nodes now, the chord is full.")
            return pb2.register_output(**reply)
        # Assigning the node a random position in the chord
        else:
            while True:
                id = random.randint(0,(CHORD_LEN)-1)
                if CHORD_SEQUENCE[id] == 0:
                    successor, predecessor = find_neighbors(id)
                    node = Node(id=id, ipaddr=ipaddr, port=port)
                    node.successor = successor
                    node.predecessor = predecessor
                    successor.predecessor = node
                    predecessor.successor = node
                    CHORD_COUNT += 1
                    CHORD_SEQUENCE[id] = node
                    reply = {
                        'id': id,
                        'm': f'{M}'
                    }
                    print(f'assigned node_id={node.id}, successor_id={node.successor.id}, predecessor_id={node.predecessor.id}')
                    return pb2.register_output(**reply)


    # This method is responsible for deregistering the node with the given id.
    def deregister(self, request, context):
        id = request.id
        if CHORD_SEQUENCE[id] != 0:
            successor, predecessor = find_neighbors(id)
            CHORD_SEQUENCE[successor.id].predecessor = predecessor
            CHORD_SEQUENCE[predecessor.id].successor = successor
            global CHORD_COUNT
            CHORD_COUNT -= 1
            node = CHORD_SEQUENCE[id]
            del node
            CHORD_SEQUENCE[id] = 0
            reply = {
                'state':True,
                'message': f'Node {id} was deleted successfully'
            }
            return pb2.deregister_output(**reply)
        else:
            reply = {
                'state':False,
                'message': f'The node {id} is not in the chord.'
            }
            return pb2.deregister_output(**reply)

    # This method is responsible for generating the dictionary of the pairs (id, ipaddr:port)
    # that the node with the given id can directly communicate with.
    def populate_finger_table(self, request, context):
        id = request.id
        finger_table = []
        ids = []
        for i in range(M):
            identifier = (id + 2**i) % CHORD_LEN
            if CHORD_SEQUENCE[identifier] != 0:
                node = CHORD_SEQUENCE[identifier]
            else:
                node, _ = find_neighbors(identifier)
            addr = f'{node.ipaddr}:{node.port}'
            duplicate = False
            for element in ids:
                if node.id == element:
                    duplicate = True
                    break
            if not duplicate:
                finger_table.append(f'({node.id}, {addr})')
                ids.append(node.id)
        reply = {
            'predecessor': CHORD_SEQUENCE[id].predecessor.id,
            'finger_table': finger_table
        }
        return pb2.pft_output(**reply)


    # This method returns the information about the chord ring (all registered nodes):    
    def get_chord_info(self, request, context):
        chord_info = []
        for node in CHORD_SEQUENCE:
            if node != 0:
                chord_info.append(f'({node.id}, {node.ipaddr}:{node.port})')            
        reply = {
            'info': chord_info,
        }
        return pb2.gci_output(**reply)

    # This method is called by the client to know that it is connected with the registry
    def connection_type(self, request, context):
        reply = {
            'type': 'Registry'
        }
        return pb2.connection_type_output(**reply)
    

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ChordServicesServicer_to_server(
        ChordServicesHandler(), server)
    server.add_insecure_port(f'{MY_ADDR}')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down")
if __name__ == '__main__':
    main()


