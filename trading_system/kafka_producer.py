from kafka import KafkaProducer
import json

class KafkaCandleProducer:
    def __init__(self, broker_url, topic):
        self.producer = KafkaProducer(bootstrap_servers=broker_url,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.topic = topic

    def send_candle_data(self, candle_data):
        self.producer.send(self.topic, value=candle_data)
        self.producer.flush()
