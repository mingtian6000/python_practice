#I want to write a kafka consumer group which conenct to my local cluster and consume message from gievn topic
# and consumer group will have 10 consumer threads.

from kafka import KafkaConsumer
import json
import datetime

bootstrap_servers = 'localhost:9092'
topic = 'test'
group_id = 'test_group'


consumer = KafkaConsumer(topic, group_id=group_id, bootstrap_servers=bootstrap_servers, auto_offset_reset='earliest')
print("start consuming messages: ", datetime.datetime.now())
try:
    for message in consumer:
        print("message: ", message.value)
except Exception as e:
    print("Error: ", e)
