import asyncio
import logging
from kafka_producer import KafkaCandleProducer
from kafka_consumer import KafkaCandleConsumer
from database_connector import MySQLConnector
from candle_data_fetcher import CandleDataFetcher


class TradingAlgorithm:
    def __init__(self):
        self.kafka_producer = KafkaCandleProducer(broker_url='kafka-service:9092', topic='candle_data')
        self.kafka_consumer = KafkaCandleConsumer(broker_url='kafka-service:9092', topic='candle_data')
        self.db_connector = MySQLConnector(host='mysql-service', port=3306, username='root', password='password',
                                           database='trading_system')
        self.data_fetcher = CandleDataFetcher(api_url='your_candle_api_url')

    async def run(self):
        try:
            # Get last offset from MySQL
            last_offset = self.db_connector.get_offset('candle_data', 0)

            # Start consuming from the last known offset
            async for candle_data in self.kafka_consumer.consume_candle_data(last_offset):
                # Process candle_data
                # Save candle_data to MySQL or perform other operations

                # Update offset
                self.db_connector.save_offset('candle_data', 0, candle_data.offset)

        except Exception as e:
            # Handle exception (log, notify, etc.)
            logging.error(f"An error occurred: {str(e)}")
            # Resume running the algorithm
            await self.run()


if __name__ == "__main__":
    algorithm = TradingAlgorithm()
    asyncio.run(algorithm.run())
