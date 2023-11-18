import grpc
from concurrent import futures

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
