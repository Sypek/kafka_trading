from time import sleep
from json import dumps
from kafka import KafkaProducer

from get_forex_data import PriceGetter

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], 
    value_serializer=lambda x: dumps(x).encode('utf-8'))

price_getter = PriceGetter(['USD', 'PLN'])

while True:
    current_price = price_getter.get_price()
    producer.send('btc001', value=current_price)
    print(current_price)
    sleep(20)