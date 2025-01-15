# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "confluent-kafka",
# ]
# ///
from confluent_kafka import Producer
import json

# Producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092'
}

# Create Producer instance
producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Produce messages
topic = "test-topic"
for i in range(5):
    message = {
        "count": i,
        "message": f"Hello Kafka #{i}"
    }
    producer.produce(
        topic,
        key=str(i),
        value=json.dumps(message),
        callback=delivery_report
    )

# Wait for messages to be delivered
producer.flush()
