import copy
import sqlite3
import os
import numpy as np
import time
from concurrent import futures
import threading
import re

import grpc
import pyedflib

import cardio_pb2
import cardio_pb2_grpc
from RPCclient import external_function
from rabbit import init_rabbit


def get_age_pharm(data: dict) -> tuple:
    """
    Получение возраста и наличия фармакологической карточки из данных.
    """
    splitted = data["file_name"].split("_")
    age = re.sub(r"[\D]+", "", splitted[1])
    pharm = True if "Pharm!" in data else False
    return age, pharm


class ECGSimulator:
    """
    Класс для работы с данными ЭКГ.
    """

    def __init__(self):
        # self.edf_data = self.read_edf_file("data/Ati4x1_15m_BL_6h.edf")
        # self.vectors = list(self.edf_data["data"].values())
        self.edf_data = {}
        self.vectors = []
        self.step = 400
        self.slice = 1000
        self.working_directory = "output"
        self.number_to_save = 0

    def StreamCardioData(self, request, context):
        """
        Потоковая передача данных ЭКГ клиенту.
        """
        timestamps = np.linspace(0, self.edf_data["duration"], self.vectors[0].shape[0])
        for i in range(0, self.vectors[0].shape[0], self.slice):
            if i + self.slice > self.vectors[0].shape[0]:
                break
            timestamp = list(timestamps[i : i + self.slice])
            sliced_vectors = [
                list(vector[i : i + self.slice]) for vector in self.vectors
            ]
            chunks = {"x": timestamp, "y": sliced_vectors}
            return_data = external_function(self.edf_data, chunks)
            print(return_data)
            cardio_data = cardio_pb2.CardioData(
                timestamp=timestamp,
                vector1=sliced_vectors[0],
                vector2=sliced_vectors[1],
                vector3=sliced_vectors[2],
                annotation=return_data["y"],
                x_annotation=return_data["x"],
            )
            yield cardio_data
        self.save_edf_file(self.edf_data)

    def SetWorkingDirectory(self, request, context):
        """
        Сохранение файла в рабочую директорию.
        """
        try:
            if not os.path.exists(request.working_directory):
                os.makedirs(request.working_directory)
            else:
                if not os.path.isdir(request.working_directory):
                    raise Exception("Path is not a directory.")
            self.working_directory = request.working_directory
            self.save_edf_file(self.edf_data)
            return cardio_pb2.SetWorkingDirectoryResponse(success=True)
        except Exception as e:
            print(f"Error setting working directory: {e}")
            return cardio_pb2.SetWorkingDirectoryResponse(success=False)

    def SetFileToProcess(self, request, context):
        """
        Обработка файла, переданного клиентом.
        """
        try:
            self.edf_data = self.read_edf_file(request.file_to_process)
            self.vectors = list(self.edf_data["data"].values())
        except Exception as e:
            print(f"Error setting file to process: {e}")
            return cardio_pb2.SetFileToProcessResponse(success=False)
        age, pharm = get_age_pharm(self.edf_data)
        self.edf_data["age"] = age
        self.edf_data["pharm"] = pharm
        labels = list(self.edf_data["data"].keys())
        if "annotations" in self.edf_data.keys():
            annotation = True
        else:
            annotation = False
        return cardio_pb2.SetFileToProcessResponse(
            success=True,
            age=age,
            pharm=pharm,
            label1=labels[0],
            label2=labels[1],
            label3=labels[2],
            is_annotated=annotation,
        )

    def StreamAnnotatedData(self, request, context):
        """
        Потоковая передача аннотированных данных клиенту.
        """
        time_to_change = 0
        change_number = 0
        timestamps = np.linspace(0, self.edf_data["duration"], self.vectors[0].shape[0])
        if "annotations" in self.edf_data.keys():
            for i in range(0, self.vectors[0].shape[0], self.slice):
                if i + self.slice > self.vectors[0].shape[0]:
                    break
                timestamp = list(timestamps[i : i + self.slice])
                time_to_change += 2.5
                sliced_vectors = [
                    list(vector[i : i + self.slice]) for vector in self.vectors
                ]
                if time_to_change > self.edf_data["annotations"][0][change_number]:
                    if (
                        time_to_change - self.edf_data["annotations"][0][change_number]
                        > 1
                    ):
                        change_number += 1
                        x_annotation = self.edf_data["annotations"][0][change_number]
                        annotated_class = self.edf_data["annotations"][2][change_number]
                    else:
                        x_annotation = self.edf_data["annotations"][0][change_number]
                        annotated_class = self.edf_data["annotations"][2][change_number]
                        change_number += 1
                else:
                    x_annotation = self.edf_data["annotations"][0][change_number]
                    annotated_class = self.edf_data["annotations"][2][change_number]
                annotated_class = str(annotated_class)
                cardio_data = cardio_pb2.CardioData(
                    timestamp=timestamp,
                    vector1=sliced_vectors[0],
                    vector2=sliced_vectors[1],
                    vector3=sliced_vectors[2],
                    annotation=annotated_class,
                    x_annotation=x_annotation,
                )
                yield cardio_data

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
            if not "annotations" in data_to_write.keys():
                conn = sqlite3.connect("Annotations.db")
                cursor = conn.cursor()
                # read all data from the table
                try:
                    cursor.execute(
                        """
                    SELECT * FROM annotation
                    """
                    )
                    annotations = cursor.fetchall()
                    for annotation in annotations:
                        f.writeAnnotation(annotation[1], -1, annotation[2])
                    print(f"Writed with annotations. to {file_path}")
                except Exception as e:
                    print(f"Error reading annotations: {e}")
            else:
                for i in range(len(data_to_write["annotations"][0])):
                    f.writeAnnotation(
                        data_to_write["annotations"][0][i],
                        data_to_write["annotations"][1][i],
                        data_to_write["annotations"][2][i],
                    )
                print(f"Writed with annotations. to {file_path}")

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
            duration = f.getFileDuration()
            annotations = f.readAnnotations()
            if len(annotations[0]) == 0:
                print("No annotations found.")
                annotations = None
        data = {}
        if annotations is not None:
            data["annotations"] = annotations
            # print(annotations)
        data_buf = dict(zip(signal_labels, signals))
        data["data"] = data_buf
        data["header"] = header
        data["file_name"] = os.path.basename(file_path)
        data["duration"] = duration
        return data


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
    consumer_thread = threading.Thread(target=init_rabbit, daemon=True)
    consumer_thread.start()
    serve()
