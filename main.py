from concurrent import futures

import grpc

from ratdream import HelloService, add_HelloServiceServicer_to_server


class ExampleService(HelloService):
    def SayHello(self, request):
        return HelloReply(message=f"Hello, {request.name}!")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_HelloServiceServicer_to_server(ExampleServicep(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
