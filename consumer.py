from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer(
    'test1',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    auto_commit_interval_ms=1000,
    group_id='counters',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    # print(message)
    print(message.value)