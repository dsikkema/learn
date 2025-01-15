# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "confluent-kafka",
# ]
# ///
from confluent_kafka import Consumer, KafkaException
import json

conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'python-consumer-group-1',
        'auto.offset.reset': 'earliest'
        }

consumer = Consumer(conf)

topic = "test-topic"
consumer.subscribe([topic])

try:
    for i in range(8):
        print(f"Loop {i=}")
        msg = consumer.poll(0.5)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")

        val = json.loads(msg.value()) 
        print(f"Received successfully: {val}")
except KafkaException:
    print("Handling...")
    pass
finally:
    consumer.close()

