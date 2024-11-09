import grpc
import cardio_pb2
import cardio_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = cardio_pb2_grpc.CardioServiceStub(channel)
        response = stub.SetWorkingDirectory(
            cardio_pb2.SetWorkingDirectoryRequest(working_directory="output")
        )
        print(f"SetWorkingDirectory response: {response.success}")
        # request = cardio_pb2.SetFileToProcessRequest(file_to_process="data/Ati4x1_15m_BL_6h.edf")
        # response = stub.SetFileToProcess(request)
        # print(f"SetFileToProcess response: {response.success}")
        request = cardio_pb2.CardioRequest(client_id="client1")
        responses = stub.StreamCardioData(request)

        for response in responses:
            print(
                f"Received data at timestamp {response.timestamp} with vector: {response.vector1}..."
            )  # Выводим первые 5 значений для краткости


if __name__ == "__main__":
    run()
