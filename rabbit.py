"""
Модуль для работы с RabbitMQ и локальной базой данных
"""
import pika
import time
import threading
import sqlite3
import json
import datetime
from ML import MLModels


class Rabbit:
    """
    Класс для работы с RabbitMQ
    """
    def __init__(self):
        self.conn = sqlite3.connect("RatDream.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            last_updated TEXT,
            last_mode TEXT,
            chunk TEXT,
            predchunk TEXT,
            metainfo TEXT
        )
        """
        )
        self.conn_annotation = sqlite3.connect("Annotations.db")
        self.cursor_annotation = self.conn_annotation.cursor()
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS annotation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time REAL,
            annotation TEXT
        )
        """
        )
        self.clear_table()
        self.ml = MLModels()

    def get_mode(self, data):
        return "start"

    def insert_data(
        self,
        file_name: str,
        last_updated: datetime,
        last_mode: str,
        chunk: dict,
        predchunk: str,
        metainfo: dict,
    ):
        """
        Функция для добавления данных в базу данных
        """
        self.cursor.execute(
            """
        INSERT INTO data (file_name, last_updated, last_mode, chunk, predchunk, metainfo)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                file_name,
                last_updated,
                last_mode,
                json.dumps(chunk),
                json.dumps(predchunk),
                json.dumps(metainfo),
            ),
        )
        self.conn.commit()

    def clear_table(self):
        """
        Функция для очистки всех строк в таблице
        """
        self.cursor.execute("DELETE FROM data")
        self.conn.commit()
        print("Table cleared")

    def update_data(
        self,
        file_name: str,
        last_updated: datetime,
        last_mode: str,
        chunk: dict,
        predchunk: str,
        metainfo: dict,
    ):
        """
        Функция для обновления данных в базе данных
        """
        self.cursor.execute(
            """
        UPDATE data
        SET last_updated = ?, last_mode = ?, chunk = ?, predchunk = ?, metainfo = ?
        WHERE file_name = ?
        """,
            (
                last_updated,
                last_mode,
                json.dumps(chunk),
                json.dumps(predchunk),
                json.dumps(metainfo),
                file_name,
            ),
        )
        self.conn.commit()

    def update_predchunk(self, last_updated: datetime, predchunk: str, last_mode: str):
        """
        Функция для обновления предсказанных классов в базе данных
        """
        self.cursor.execute(
            """
        UPDATE data
        SET predchunk = ?, last_mode = ?
        WHERE last_updated = ?
        """,
            (json.dumps(predchunk), json.dumps(last_mode), last_updated),
        )
        self.conn.commit()

    def get_data_by_name(self, file_name: str):
        """
        Функция для получения данных из базы данных
        """
        self.cursor.execute(
            """
        SELECT * FROM data
        WHERE file_name = ?
        """,
            (file_name,),
        )
        return self.cursor.fetchone()

    def insert_annotation(self, time, annotation: str):
        """
        Функция для добавления аннотаций в базу данных
        """
        self.cursor_annotation.execute(
            """
        INSERT INTO annotation (time, annotation)
        VALUES (?, ?)
        """,
            (time, annotation),
        )
        self.conn_annotation.commit()

    def get_info_from_rabbitmq(self, data: dict) -> str:
        """
        Функция для сохранения данных из RabbitMQ в базу данных
        """
        data = json.loads(data)
        is_exist = self.get_data_by_name(data["file_name"])
        last_updated = datetime.datetime.now()
        last_mode = self.get_mode(data)
        predchunk = "ds1"
        if not is_exist:
            self.insert_data(
                data["file_name"],
                str(last_updated),
                last_mode,
                data["chunk"],
                predchunk,
                {"age": data["age"], "pharm": data["pharm"]},
            )
        print("Data inserted")
        return self.predict_classes()

    def predict_classes(self) -> str:
        """
        Функция для предсказания классов
        """
        self.cursor.execute(
            "SELECT last_updated, last_mode, chunk, predchunk, metainfo FROM data ORDER BY id DESC LIMIT 1"
        )
        row = self.cursor.fetchone()
        last_updated = row[0]
        last_mode = row[1]
        chunk = json.loads(row[2])
        predchunk = json.loads(row[3])
        metainfo = json.loads(row[4])
        print("Data loaded")
        result = self.ml.predict(predchunk, chunk, metainfo, last_mode)
        if result["y"] != "none":
            self.update_predchunk(last_updated, result["y"], result["mode"])
            self.insert_annotation(result["x"], result["y"])
        return result["y"]

    def process_data(self, data: dict) -> str:
        result = self.get_info_from_rabbitmq(data)
        return result

    def consume_data(self):
        """
        Функция для получения данных
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.queue_declare(queue="data_queue")

        def callback(ch, method, properties, body):
            print(f" [x] Received {body}")
            result = self.process_data(body)
            print(result)
            result = result.encode()
            channel.basic_publish(
                exchange="",
                routing_key=properties.reply_to,
                body=result,
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id
                ),
            )
            print(f" [x]  Done processing")

        channel.basic_consume(
            queue="data_queue", on_message_callback=callback, auto_ack=True
        )

        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()


def init_rabbit():
    rabbit = Rabbit()
    rabbit.consume_data()


if __name__ == "__main__":
    # Запуск consume_data в отдельном потоке
    consumer_thread = threading.Thread(target=init_rabbit)
    consumer_thread.start()
