from aiokafka import AIOKafkaProducer
import json

class KafkaCandleProducer:
    def __init__(self, broker_url, topic):
        self.producer = AIOKafkaProducer(bootstrap_servers=broker_url,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.topic = topic
    async def start(self):
        await self.producer.start()

    async def send_to_kafka(self, data):
        await self.producer.send_and_wait(self.topic, value=data.encode('utf-8'))
