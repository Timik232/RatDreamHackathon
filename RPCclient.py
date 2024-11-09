import uuid
import pika
import json
class RpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost")
        )
        self.channel = self.connection.channel()

        # Создаем временную очередь для получения ответа
        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body

    def send_data_and_get_result(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key="data_queue",
            body=message,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=self.corr_id
            ),
        )

        # Ждем, пока не получим ответ
        while self.response is None:
            self.connection.process_data_events()

        return self.response


def external_function(data):
    client = RpcClient()
    message = json.dumps(data)
    response = client.send_data_and_get_result(message.encode())
    print(f"Received response: {response.decode()}")
    return json.loads(response.decode())