# Assuming the proto file is saved as 'hello.proto'
# Generate the Python code from the proto file using the following command:
# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. hello.proto

# After generating the files, you will have 'hello_pb2.py' and 'hello_pb2_grpc.py'

# Import the necessary modules
from concurrent import futures
import grpc
import hello_pb2
import hello_pb2_grpc


# Define the server-side implementation of the HelloService
class HelloServiceServicer(hello_pb2_grpc.HelloServiceServicer):
    def SayHello(self, request, context):
        # Implement the SayHello RPC method
        response = hello_pb2.HelloReply()
        response.message = f"Hello, {request.name}!"
        return response


# Function to serve the gRPC server
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServiceServicer_to_server(HelloServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
