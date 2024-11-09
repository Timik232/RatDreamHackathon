import pika
import time
import threading
import sqlite3
import json


conn = sqlite3.connect('RatDream.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_updated TEXT,
    last_mode TEXT,
    chunk TEXT,
    predchunk TEXT,
    metainfo TEXT
)
''')


def insert_data(last_updated, last_mode, chunk, predchunk, metainfo):
    cursor.execute('''
    INSERT INTO data (last_updated, last_mode, chunk, predchunk, metainfo)
    VALUES (?, ?, ?, ?, ?)
    ''', (last_updated, last_mode, json.dumps(chunk), json.dumps(predchunk), json.dumps(metainfo)))
    conn.commit()


def get_info_from_rabbitmq(data):
    predict_classes(data.time)

def predict_classes(time):
    pass

def process_data(data):
    get_info_from_rabbitmq(data)
    predict_classes(time)

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

