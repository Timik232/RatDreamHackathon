import pika
import time
import threading


def process_data(data):
    # Симуляция длительной обработки данных ML-сервисом
    print(f"Processing data: {data}")
    time.sleep(5)  # Замените на реальный код обработки данных
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

