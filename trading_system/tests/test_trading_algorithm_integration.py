import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import asyncio
from trading_system.data_fetcher import CandleDataFetcher
from trading_system.trading_algorithm import TradeExecutor, TradingAlgorithm


class TestTradingSystemIntegration(unittest.IsolatedAsyncioTestCase):
    async def test_trading_system_integration(self):
        mock_fetch_candle_data = AsyncMock(return_value={'symbol': 'BTC/USD', 'candles': [1, 2, 3, 4, 5]})

        with patch.object(CandleDataFetcher, 'fetch_candle_data', new=mock_fetch_candle_data):
            mock_execute_trades = MagicMock()
            with patch.object(TradeExecutor, 'execute_trades', new=mock_execute_trades):
                await TradingAlgorithm.run()
                mock_fetch_candle_data.assert_called_once_with('BTC/USD')
                mock_execute_trades.assert_called_once_with(['BUY', 'SELL', 'HOLD'])

if __name__ == '__main__':
    unittest.main()
