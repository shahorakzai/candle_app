from kafka import KafkaConsumer
import json
import logging

class KafkaCandleConsumer:
    def __init__(self, broker_url, topic):
        self.consumer = KafkaConsumer(topic,
                                      bootstrap_servers=broker_url,
                                      auto_offset_reset='earliest',
                                      enable_auto_commit=False,
                                      group_id='candle_consumer_group',
                                      value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    async def consume_candle_data(self, start_offset=None):
        try:
            if start_offset is not None:
                for partition in self.consumer.partitions_for_topic(self.topic):
                    self.consumer.seek_to_offset(topic_partition=(self.topic, partition), offset=start_offset)

            for message in self.consumer:
                yield message.value

        except Exception as e:
            logging.error(f"Error while consuming messages: {str(e)}")
            raise e  # Re-raise the exception to be handled by the caller
