from confluent_kafka import Producer

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

p = Producer({'bootstrap.servers': 'localhost:9092'})

for _ in range(5):
    p.produce('test-topic', 'Hello, Kafka!', callback=delivery_report)

p.flush()