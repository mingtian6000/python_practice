from confluent_kafka import Consumer, KafkaException

c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['test-topic'])

try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        print(f"Received message: {msg.value().decode('utf-8')}")
finally:
    c.close()