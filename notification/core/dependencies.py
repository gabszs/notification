import pika

from notification.core.settings import settings

rabbit_credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
rabbit_connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=settings.RABBIT_URL, credentials=rabbit_credentials)
)

__all__ = ["rabbit_credentials", "rabbit_connection"]
