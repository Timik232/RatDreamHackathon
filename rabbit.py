import pika
import time
import threading
import sqlite3
import json
import datetime


conn = sqlite3.connect("RatDream.db")
cursor = conn.cursor()
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_updated TEXT,
    last_mode TEXT,
    chunk TEXT,
    predchunk TEXT,
    metainfo TEXT
)
"""
)


def get_mode(data):
    return "start"


def insert_data(file_name, last_updated, last_mode, chunk, predchunk, metainfo):
    """
    Функция для добавления данных в базу данных
    """
    cursor.execute(
        """
    INSERT INTO data (file_name, last_updated, last_mode, chunk, predchunk, metainfo)
    VALUES (?, ?, ?, ?, ?)
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
    conn.commit()


def update_data(file_name, last_updated, last_mode, chunk, predchunk, metainfo):
    """
    Функция для обновления данных в базе данных
    """
    cursor.execute(
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
    conn.commit()


def update_predchunk(last_updated, predchunk):
    """
    Функция для обновления предсказанных классов в базе данных
    """
    cursor.execute(
        """
    UPDATE data
    SET predchunk = ?
    WHERE last_updated = ?
    """,
        (json.dumps(predchunk), last_updated),
    )
    conn.commit()


def get_data_by_name(file_name):
    """
    Функция для получения данных из базы данных
    """
    cursor.execute(
        """
    SELECT * FROM data
    WHERE file_name = ?
    """,
        (file_name,),
    )
    return cursor.fetchone()


def get_info_from_rabbitmq(data):
    """
    Функция для сохранения данных из RabbitMQ в базу данных
    """
    data = json.loads(data)
    is_exist = get_data_by_name(data.file_name)
    last_updated = datetime.datetime.now()
    last_mode = get_mode(data)
    predchunk = "ds1"
    if not is_exist:
        insert_data(
            data["file_name"],
            str(last_updated),
            last_mode,
            data["chunk"],
            predchunk,
            {"age": data["age"], "pharm": data["pharm"]},
        )
    predict_classes(last_updated)


def predict_classes(last_updated):
    """
    Функция для предсказания классов
    """
    cursor.execute(
        "SELECT last_updated, last_mode, chunk, predchunk, metainfo FROM data ORDER BY id DESC LIMIT 1"
    )
    row = cursor.fetchone()
    last_updated = row[0]
    last_mode = row[1]
    chunk = json.loads(row[2])
    predchunk = json.loads(row[3])
    metainfo = json.loads(row[4])


def process_data(data):
    get_info_from_rabbitmq(data)
    result = data
    return result


def consume_data():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="data_queue")

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        result = process_data(body)
        channel.basic_publish(
            exchange="",
            routing_key=properties.reply_to,
            body=result,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        )
        print(f" [x]  Done processing")

    channel.basic_consume(
        queue="data_queue", on_message_callback=callback, auto_ack=True
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    # Запуск consume_data в отдельном потоке
    consumer_thread = threading.Thread(target=consume_data)
    consumer_thread.start()
