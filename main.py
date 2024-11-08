import time
import grpc
from concurrent import futures
import random

# Import the generated classes
import cardio_pb2
import cardio_pb2_grpc


class CardioService(cardio_pb2_grpc.CardioServiceServicer):
    def StreamCardioData(self, request, context):
        print(f"Client {request.client_id} connected.")

        while True:
            # Generate ECG data as a vector of float values
            timestamp = int(time.time())
            vector = self.generate_ecg_vector()

            # Log the data being sent
            print(
                f"Sending data at timestamp {timestamp} with vector: {vector[:5]}..."
            )  # Print first 5 values for brevity

            # Create and send the response message
            cardio_data = cardio_pb2.CardioData(timestamp=timestamp, vector=vector)
            yield cardio_data
            time.sleep(0.5)  # Delay to simulate real-time data

    def generate_ecg_vector(self):
        """Simulate a simple sinusoidal ECG-like waveform with added noise."""
        vector = []
        for i in range(100):  # Generate 100 points for a single waveform cycle
            # Create a sinusoidal wave with random noise
            value = 1.0 * (i % 25) - 12.5  # Base wave
            noise = random.uniform(-2, 2)  # Add some noise
            vector.append(value + noise)
        return vector


def serve():
    # Initialize the server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cardio_pb2_grpc.add_CardioServiceServicer_to_server(CardioService(), server)

    # Bind to a port
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server is running on port 50051.")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Server stopped.")


if __name__ == "__main__":
    serve()
