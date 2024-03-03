from typing import List

import aiohttp
from datetime import datetime

class Candle:
    def __init__(self, timestamp: datetime, open_price: float, close_price: float, high_price: float, low_price: float):
        self.timestamp = timestamp
        self.open_price = open_price
        self.close_price = close_price
        self.high_price = high_price
        self.low_price = low_price
class TradingSignal:
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class SignalAnalyzer:
    async def analyze_signals(self, candle_data: List[Candle]) -> TradingSignal:
        last_candle = candle_data[-1]
        if last_candle.close_price > last_candle.open_price:
            return TradingSignal.BUY
        elif last_candle.close_price < last_candle.open_price:
            return TradingSignal.SELL
        else:
            return TradingSignal.HOLD

class CandleDataFetcher:
    def __init__(self, api_url):
        self.api_url = api_url

    async def fetch_candle_data(self, symbol, start_time, end_time):
        url = f"{self.api_url}/{symbol}?start_time={start_time}&end_time={end_time}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    raise Exception(f"Failed to fetch data. Status code: {response.status}")

