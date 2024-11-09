import math
import time
import grpc
from concurrent import futures
import random

# Import the generated classes
import cardio_pb2
import cardio_pb2_grpc


class ECGSimulator:
    def StreamCardioData(self, request, context):
        print(f"Client {request.client_id} connected.")

        while True:
            # Генерируем данные ЭКГ в виде вектора
            timestamp = int(time.time())
            vector = self.generate_ecg_vector()

            # Логирование отправляемых данных
            print(
                f"Sending data at timestamp {timestamp} with vector: {vector[:5]}..."
            )  # Выводим первые 5 значений для краткости

            # Создаем и отправляем сообщение-ответ
            cardio_data = cardio_pb2.CardioData(timestamp=timestamp, vector=vector)
            yield cardio_data
            time.sleep(0.5)  # Задержка для имитации передачи в реальном времени

    def generate_ecg_vector(self, num_points=5):
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
    serve()
