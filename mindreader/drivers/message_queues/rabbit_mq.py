import pika


class RabbitMQ:
    prefix = 'rabbitmq'

    def __init__(self, host, port):
        self.host = host
        self.port = port

        try:  # test connection
            pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port,
                                                              connection_attempts=6, retry_delay=20))  # 2 minutes timeout
        except pika.exceptions.AMQPConnectionError:
            raise ConnectionError

    def publish(self, topic, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
        channel = connection.channel()
        channel.exchange_declare(exchange=topic, exchange_type='fanout')
        channel.basic_publish(exchange=topic, routing_key='', body=message)
        connection.close()

    def consume(self, topic, handler, queue):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
        channel = connection.channel()
        channel.exchange_declare(exchange=topic, exchange_type='fanout')
        result = channel.queue_declare(queue=queue, exclusive=False)
        queue_name = result.method.queue
        channel.queue_bind(exchange=topic, queue=queue_name)

        def callback(channel, method, properties, body):
            handler(body)

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
