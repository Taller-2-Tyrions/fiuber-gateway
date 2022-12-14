import pika
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Parse CLODUAMQP_URL (fallback to localhost)
URL = os.getenv("CLOUDAMQP_URL")
METRICS_QUEUE = os.getenv("METRICS_QUEUE")

params = pika.URLParameters(URL)
# params = pika.ConnectionParameters(heartbeat=0,
#                                    host=URL)
params.socket_timeout = 5
params.heartbeat = 0


connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
channel = connection.channel()  # start a channel
channel.queue_declare(queue=METRICS_QUEUE)  # Declare a queue
# send a message


def push_metric(data):
    channel.basic_publish(exchange='',
                          routing_key=METRICS_QUEUE,
                          body=json.dumps(data))
    # print("[x] Message sent to consumer")


def close_connection():
    connection.close()
