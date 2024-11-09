import copy
import math
import os
import random
import time
from concurrent import futures
from typing import Optional

import grpc
import pyedflib

import cardio_pb2
import cardio_pb2_grpc


class ECGSimulator:
    def __init__(self):
        self.edf_data = self.read_edf_file("data/Ati4x1_15m_BL_6h.edf")
        self.vectors = list(self.edf_data["data"])
        self.slice = 10
        self.previous_slice = 0
        self.working_directory = "output"
        self.number_to_save = 0

    def StreamCardioData(self, request, context):
        """
        Потоковая передача данных ЭКГ клиенту.
        """
        print(f"Client {request.client_id} connected.")

        while True:
            timestamp = int(time.time())
            sliced_vectors = [vector[self.previous_slice : self.previous_slice + self.slice] for vector in self.vectors]
            self.previous_slice += self.slice
            sliced_vectors = self.process_data(sliced_vectors)
            cardio_data = cardio_pb2.CardioData(timestamp=timestamp, vector=sliced_vectors)
            # self.save_edf_file(self.edf_data)
            yield cardio_data
            time.sleep(0.03)

    def SetWorkingDirectory(self, request, context):
        """
        Установка рабочего каталога для сохранения файлов.
        """
        try:
            if not os.path.exists(request.working_directory):
                os.makedirs(request.working_directory)
            else:
                if not os.path.isdir(request.working_directory):
                    raise Exception("Path is not a directory.")
            self.working_directory = request.working_directory
            return cardio_pb2.SetWorkingDirectoryResponse(success=True)
        except Exception as e:
            print(f"Error setting working directory: {e}")
            return cardio_pb2.SetWorkingDirectoryResponse(success=False)

    def SetFileToProcess(self, request, context):
        """
        Обработка файла, переданного клиентом.
        """
        try:
            edf_data = self.read_edf_file(request.file_to_process)
            vectors = list(self.edf_data["data"])
        except Exception as e:
            print(f"Error setting file to process: {e}")
            return cardio_pb2.SetFileToProcessResponse(success=False)
        for i in range(0, len(vectors[0]), self.slice):
            sliced_vectors = [vector[i : i + self.slice] for vector in self.vectors]
            self.previous_slice += self.slice
            sliced_vectors = self.process_data(sliced_vectors)

        self.save_edf_file(edf_data)
        return cardio_pb2.SetFileToProcessResponse(success=True)

    def process_data(self, data):
        print("Processing data...")
        # Обработка данных
        return data

    def save_edf_file(self, data: dict):
        """
        Сохранение данных в файл EDF.

        Args:
            data (dict): Данные для сохранения в файле EDF.
        """
        file_path = os.path.join(
            self.working_directory, f"ecg_output{self.number_to_save}.edf"
        )
        self.number_to_save += 1
        data_to_write = copy.deepcopy(data)
        with pyedflib.EdfWriter(
            file_path,
            len(data_to_write["data"]),
            file_type=pyedflib.FILETYPE_EDFPLUS,
        ) as f:
            f.setHeader(data_to_write["header"])
            f.setSignalHeaders(
                [{"label": label} for label in data_to_write["data"].keys()]
            )
            samples = [
                data_to_write["data"][label] for label in data_to_write["data"].keys()
            ]
            f.writeSamples(samples)

    def read_edf_file(self, file_path: str):
        """
        Чтение данных из файла EDF.

        Args:
            file_path (str): Путь к файлу EDF.

        Returns:
            dict: Словарь с данными из файла EDF.
        """
        with pyedflib.EdfReader(file_path) as f:
            header = f.getHeader()
            signal_labels = f.getSignalLabels()
            signals = [f.readSignal(i) for i in range(f.signals_in_file)]

        data = {}
        data_buf = dict(zip(signal_labels, signals))
        data["data"] = data_buf
        data["header"] = header
        return data

    def generate_ecg_vector(self, num_points=5) -> list:
        """
        Симуляция простой синусоидальной ЭКГ с добавлением шума.

        Args:
            num_points (int): Количество точек данных для генерации ЭКГ.

        Returns:
            list: Список y-значений, представляющих ЭКГ-сигнал.
        """
        vector = []
        phase_shift = random.uniform(
            0, 2 * math.pi
        )  # случайный сдвиг фазы для вариации

        for i in range(num_points):
            # Генерация синусоидального сигнала
            base_wave = math.sin(i * 0.1 + phase_shift) * 1.5  # 1.5 — амплитуда
            # Добавление шума от -0.5 до 0.3
            noise = random.uniform(-0.5, 0.3)
            # Итоговое значение с добавлением шума
            y_value = base_wave + noise
            vector.append(y_value)

        return vector


def serve():
    """
    Запуск сервера gRPC.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cardio_pb2_grpc.add_CardioServiceServicer_to_server(ECGSimulator(), server)

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
