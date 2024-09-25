import os
import sys

from icecream import ic

from notification.core.dependencies import rabbit_connection
from notification.core.settings import settings
from notification.services import Notification


def main():
    try:
        notification = Notification()
        notification.connect()
        channel = rabbit_connection.channel()

        channel.queue_declare(queue=settings.audio_queue, durable=True)

        def callback(channel, method, properties, body):
            print("Received message:", body.decode())
            err = notification(body)
            if err:
                channel.basic_nack(delivery_tag=method.delivery_tag)
            else:
                channel.basic_ack(delivery_tag=method.delivery_tag)


        channel.basic_consume(queue=settings.audio_queue, on_message_callback=callback)
        print('Waiting for messages in the "audio" queue. To exit press CTRL+C')
        channel.start_consuming()

    except Exception as error:
        notification.close()
        channel.close()
        raise error


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            ic("Queue interrupted")
            sys.exit(0)
        except SystemExit:
            os._exit(0)
