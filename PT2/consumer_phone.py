import time

import source.db_connect
from PT2.source.models import User
from source.RABBIT_connect import rMQ_connect
from bson import ObjectId

channel = rMQ_connect()
channel.queue_declare(queue="SMS")


def callback_sms(ch, method, props, body):
    """
    Обробник повідомлення з черги "SMS".

    :param ch: Канал зв'язку з RabbitMQ.
    :param method: Інформація про метод передачі повідомлення.
    :param props: Властивості повідомлення.
    :param body: Тіло повідомлення.
    :return: None
    """
    uid_str = body.decode()
    user = User.objects.get(id=ObjectId(uid_str))
    if not user.sent:
        user.sent = True
        print(f'User {user.fullname} on {user.phone} received:\n{uid_str}\n')
        user.save()
        time.sleep(0.3)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.queue_declare(queue='SMS')
channel.basic_consume(queue="SMS", on_message_callback=callback_sms)

if __name__ == "__main__":
    channel.start_consuming()
