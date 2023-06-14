import pika


def rMQ_connect():
    creds = pika.PlainCredentials('guest', 'guest')
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=creds)
    )
    channel = conn.channel()
    return channel
