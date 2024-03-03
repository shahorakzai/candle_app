import asyncio
from datetime import datetime
from trading_system.data_fetcher import TradingSignal, CandleDataFetcher, SignalAnalyzer
from trading_system.database_connector import MySQLConnector
from trading_system.kafka_consumer import KafkaCandleConsumer
from trading_system.kafka_producer import KafkaCandleProducer


class TradeExecutor:
    def execute_trade(self, symbol: str, action: str, quantity: int):
        pass

class TradingAlgorithm:
    def __init__(self,
                 kafka_connector,
                 kafka_consumer,
                 mysql_connector,
                 data_fetcher,
                 signal_analyzer,
                 trading_executor):
        self.kafka_producer = kafka_connector
        self.kafka_consumer = kafka_consumer
        self.db_connector = mysql_connector
        self.data_fetcher = data_fetcher
        self.signal_analyzer = signal_analyzer
        self.trading_executor = trading_executor

    async def write_offset(self, timestamp):
        self.db_connector.save_offset(timestamp)

    async def run(self, symbol):
        await self.kafka_producer.start()
        while True:
            start_time = self.db_connector.get_offset()
            end_time = datetime.now()
            interval = end_time - start_time
            candle_data = await self.data_fetcher.fetch_candle_data(symbol, start_time, end_time)

            trading_signal = await self.signal_analyzer.analyze_signals(candle_data)

            if trading_signal == TradingSignal.BUY:
                await self.trade_executor.execute_trade(symbol, TradingSignal.BUY, quantity=100)
            elif trading_signal == TradingSignal.SELL:
                await self.trade_executor.execute_trade(symbol, TradingSignal.SELL, quantity=100)

            await self.kafka_producer.send_to_kafka(candle_data)
            await self.write_offset(candle_data["timestamp"])
            await asyncio.sleep(interval)

if __name__ == "__main__":
    kafka_producer = KafkaCandleProducer(broker_url='kafka-service:9092', topic='candle_data')
    kafka_consumer = KafkaCandleConsumer(broker_url='kafka-service:9092', topic='candle_data')
    mysql_connector = MySQLConnector(host='mysql-service', port=3306, username='root', password='root',
                                     database='trading_algorithm')

    data_fetcher = CandleDataFetcher(api_url='your_candle_api_url')
    signal_analyzer = SignalAnalyzer()
    trade_executor = TradeExecutor()
    trading_algo = TradingAlgorithm(
        kafka_producer,
        kafka_consumer,
        mysql_connector,
        data_fetcher,
        signal_analyzer,
        trade_executor
    )

    asyncio.run(trading_algo.run())