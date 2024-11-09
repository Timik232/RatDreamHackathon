import math
import time
import grpc
from concurrent import futures
import random
import pyedflib

import cardio_pb2
import cardio_pb2_grpc


class ECGSimulator:
    def __init__(self):
        self.vector = list(read_edf_file("data/Ati4x1_15m_BL_6h.edf")["FrL"])
        self.slice = 10
        self.previous_slice = 0


    def StreamCardioData(self, request, context):
        print(f"Client {request.client_id} connected.")

        while True:
            # Генерируем данные ЭКГ в виде вектора
            timestamp = int(time.time())
            # vector = self.generate_ecg_vector()
            vector = self.vector[self.previous_slice:self.previous_slice + self.slice]
            self.previous_slice += self.slice
            # Логирование отправляемых данных
            print(
                f"Sending data at timestamp {timestamp} with vector: {vector[:5]}..."
            )  # Выводим первые 5 значений для краткости

            # Создаем и отправляем сообщение-ответ
            cardio_data = cardio_pb2.CardioData(timestamp=timestamp, vector=vector)
            yield cardio_data
            time.sleep(0.5)  # Задержка для имитации передачи в реальном времени

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


def read_edf_file(file_path: str):
    """
    Чтение данных из файла EDF.

    Args:
        file_path (str): Путь к файлу EDF.

    Returns:
        dict: Словарь с данными из файла EDF.
    """
    with pyedflib.EdfReader(file_path) as f:
        header = f.getHeader()
        print("Header:" + str(header))

        signal_labels = f.getSignalLabels()
        signals = [f.readSignal(i) for i in range(f.signals_in_file)]

    data = dict(zip(signal_labels, signals))
    return data


def serve():
    # Initialize the server
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
    # serve()
    data = read_edf_file("data/Ati4x1_15m_BL_6h.edf")
    print(data)
    data = read_edf_file("data/Ati4x1_15m_BL_6h_fully_marked.edf")
    print(data)
