from cgitb import text
import service_pb2_grpc as pb2_grpc
import service_pb2 as pb2
import grpc
from concurrent import futures
import sys
PORT = sys.argv[1]

class ReverseHandler(pb2_grpc.ReverseServicer):
    def reverse(self, request, context):
        text = request.text
        text = text[::-1]
        reply = {"message": text}
        return pb2.reverse_output(**reply)


class SplitHandler(pb2_grpc.SplitServicer):
    def split(self, request, context):
        text = request.text
        delim = request.delim
        words = text.split(delim)
        n = len(words)
        reply = {"n": n,
                "text": words}
        return pb2.split_output(**reply)

class IsprimeHandler(pb2_grpc.IsprimeServicer):
    def isprime(self, request_iterator, context):
        for request in request_iterator:
            n = request.num
            out = False
            if n in (2, 3):
                reply = {"text": f"{n} is prime"}
                yield pb2.isprime_output(**reply)
                out = True
            if n % 2 == 0 and not out:
                reply = {"text": f"{n} is not prime"}
                yield pb2.isprime_output(**reply)
                out = True
            for divisor in range(3, n, 2):
                if n % divisor == 0 and not out:
                    reply = {"text": f"{n} is not prime"}
                    yield pb2.isprime_output(**reply)
                    out = True
            if not out:
                reply = {"text": f"{n} is prime"}
                yield pb2.isprime_output(**reply)
        


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ReverseServicer_to_server(
        ReverseHandler(), server)
    pb2_grpc.add_SplitServicer_to_server(
        SplitHandler(), server)
    pb2_grpc.add_IsprimeServicer_to_server(
        IsprimeHandler(), server
    )
    server.add_insecure_port(f'127.0.0.1:{PORT}')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down")
if __name__ == '__main__':
    server()