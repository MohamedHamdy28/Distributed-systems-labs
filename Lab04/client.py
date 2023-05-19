import grpc
import service_pb2 as pb2
import service_pb2_grpc as pb2_grpc
import sys

SERVER = ((sys.argv[1]).split(':')[0],int((sys.argv[1]).split(':')[1]))


def generate_messages(numbers):
    for n in numbers:
        msg = pb2.isprime_input(num=int(n))
        yield msg

def client():
    channel = grpc.insecure_channel(f'{SERVER[0]}:{SERVER[1]}')
    while True:
        try:
            request = input('>')
            if len(request) != 0:
                if request[:7] == "reverse":
                    request = request[8:]
                    stub = pb2_grpc.ReverseStub(channel)
                    msg = pb2.reverse_input(text=request)
                    response = stub.reverse(msg)
                    print(response)
                if request[:5] == "split":
                    request = request[6:]
                    stub = pb2_grpc.SplitStub(channel)
                    msg = pb2.split_input(text=request, delim=' ')
                    response = stub.split(msg)
                    print(f"number: {response.n}")
                    words = response.text
                    for word in words:
                        print(f'parts: "{word}"')
                    print()
                if request[:7] == 'isprime':
                    numbers = request[8:].split()
                    stub = pb2_grpc.IsprimeStub(channel)
                    for response in stub.isprime(generate_messages(numbers)):
                        print(f"{response.text}")
                if request == 'exit':
                    print("Shutting down")
                    exit()
        except KeyboardInterrupt:
            print("Shutting down")
            exit()
if __name__ == '__main__':
    client()