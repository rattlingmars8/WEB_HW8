import time

import source.db_connect
from PT2.source.models import User, WayToContact
from source.RABBIT_connect import rMQ_connect
from seeds import seed_users

channel = rMQ_connect()
channel.queue_declare(queue="EMAIL")
channel.queue_declare(queue="SMS")


def main():
    User.objects().delete()
    users = seed_users()
    print("....Робимо магію....")

    for user in users:
        user.save()
    print("\n....Дані користувачів згенеровано....\n")

    channel.queue_purge(queue='SMS')
    channel.queue_purge(queue='EMAIL')

    db_users = User.objects.all()

    print("\n....Готово до опрацювання....\n")

    for db_user in db_users:
        if db_user.way_to_contact == WayToContact.PHONE:
            channel.basic_publish(exchange="", routing_key="SMS", body=f'{db_user.id}'.encode())
        elif db_user.way_to_contact == WayToContact.EMAIL:
            channel.basic_publish(exchange="", routing_key="EMAIL", body=f'{db_user.id}'.encode())

        time.sleep(0.3)

        print(f"Sent to {db_user.fullname} => {db_user.id}\n")
    channel.close()


if __name__ == "__main__":
    main()
