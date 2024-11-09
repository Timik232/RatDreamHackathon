"""
Клиент для тестирования отправки данных и получения с сервера
"""
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
        request = cardio_pb2.SetFileToProcessRequest(
            # file_to_process="data/Ati4x1_15m_BL_6h.edf"
            # file_to_process="data/Ati4x1_15m_BL_6h_fully_marked.edf"
            file_to_process="data/Ati4x1_15m_H2O_6h.edf"
        )
        # request = cardio_pb2.SetFileToProcessRequest(file_to_process="data/Ati4x1_15m_BL_6h.edf")
        response = stub.SetFileToProcess(request)
        print(f"SetFileToProcess response: {response.success}")
        print(f"{response.age}, {response.pharm}, {response.label1}")
        # request = cardio_pb2.SetFileToProcessRequest(file_to_process="data/Ati4x1_15m_BL_6h.edf")
        # response = stub.SetFileToProcess(request)
        # print(f"SetFileToProcess response: {response.success}")
        request = cardio_pb2.CardioRequest()
        # responses = stub.StreamAnnotatedData(request)
        responses = stub.StreamCardioData(request)

        for response in responses:
            print(
                f"Received data at timestamp {response.timestamp[:5]} with class: {response.annotation}, "
                f"with vector: {response.vector1[:5]}..."
            )


if __name__ == "__main__":
    run()
