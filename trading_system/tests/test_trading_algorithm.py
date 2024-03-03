import asyncio
import pytest
from unittest.mock import patch
from datetime import datetime
from aioresponses import aioresponses
from trading_system.data_fetcher import CandleDataFetcher

@pytest.mark.asyncio
async def test_fetch_candle_data():
    api_url = 'https://api.example.com/candle_data'
    candle = CandleDataFetcher(api_url)
    with aioresponses() as mock_responses:
        mock_responses.get(api_url, status=200, payload="Mocked Candle Data")
        result = await candle.fetch_candle_data(datetime.now())
        assert result == "Mocked Candle Data"

@pytest.mark.asyncio
async def test_fetch_candle_data_failure():
    api_url = 'https://api.example.com/candle_data'
    with patch('trading_system.data_fetcher.aiohttp.ClientSession.get') as mock_get:
        mock_response = mock_get.return_value.__aenter__.return_value
        mock_response.status = 500
        candle = CandleDataFetcher(api_url)
        with aioresponses() as mock_responses:

            mock_responses.get(api_url, status=500)

            with pytest.raises(Exception, match="Failed to fetch data. Status code: 500"):
                await candle.fetch_candle_data(datetime.now())