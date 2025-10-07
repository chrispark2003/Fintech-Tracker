"""
Data fetching service - Fetches data from external APIs (yfinance, FMP, etc.)
"""

import yfinance as yf
from typing import List, Dict, Optional
from datetime import datetime, date, timedelta
import requests
from app.core.config import settings


class DataFetcher:
    """Fetches market data from free API sources"""

    def __init__(self):
        self.fmp_key = settings.FINPREP_API_KEY
        self.marketaux_key = settings.MARKETAUX_API_KEY

    def get_stock_price(self, ticker: str, period: str = "1mo") -> Dict:
        """
        Fetch stock price data using yfinance (FREE)

        Args:
            ticker: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)

        Returns:
            Dict with OHLCV data
        """
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)

            return {
                "ticker": ticker,
                "data": hist.to_dict('records'),
                "metadata": stock.info
            }
        except Exception as e:
            print(f"Error fetching price for {ticker}: {e}")
            return {}

    def get_fundamentals(self, ticker: str) -> Dict:
        """
        Fetch fundamental data using Financial Modeling Prep (FREE tier: 250 calls/day)

        Returns key metrics: P/E, ROE, revenue growth, etc.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v3/key-metrics/{ticker}"
            params = {"apikey": self.fmp_key, "limit": 1}
            response = requests.get(url, params=params)
            response.raise_for_status()

            return response.json()[0] if response.json() else {}
        except Exception as e:
            print(f"Error fetching fundamentals for {ticker}: {e}")
            return {}

    def get_earnings_calendar(self, from_date: date, to_date: date) -> List[Dict]:
        """
        Fetch earnings calendar from FMP (FREE)

        Critical for timing recommendations
        """
        try:
            url = "https://financialmodelingprep.com/api/v3/earning_calendar"
            params = {
                "apikey": self.fmp_key,
                "from": from_date.isoformat(),
                "to": to_date.isoformat()
            }
            response = requests.get(url, params=params)
            response.raise_for_status()

            return response.json()
        except Exception as e:
            print(f"Error fetching earnings calendar: {e}")
            return []

    def get_news(self, ticker: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        Fetch news from Marketaux (FREE tier: 100 requests/day)

        Args:
            ticker: Specific stock ticker (optional)
            limit: Number of articles

        Returns:
            List of news articles
        """
        try:
            url = "https://api.marketaux.com/v1/news/all"
            params = {
                "api_token": self.marketaux_key,
                "symbols": ticker if ticker else "",
                "limit": limit,
                "language": "en"
            }
            response = requests.get(url, params=params)
            response.raise_for_status()

            return response.json().get("data", [])
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def get_sec_filings(self, ticker: str, filing_type: str = "8-K") -> List[Dict]:
        """
        Fetch SEC filings from EDGAR API (FREE, unlimited)

        8-K = Material events (most important for catalysts)
        10-K = Annual report
        10-Q = Quarterly report

        Returns:
            List of filings
        """
        # TODO: Implement SEC EDGAR API integration
        # SEC API: https://www.sec.gov/edgar/sec-api-documentation
        pass

    def get_macro_data(self, series_id: str) -> Dict:
        """
        Fetch macro economic data from FRED API (FREE, unlimited)

        Common series IDs:
        - CPIAUCSL: CPI (inflation)
        - UNRATE: Unemployment rate
        - DFF: Federal Funds Rate
        - GDP: Gross Domestic Product

        Returns:
            Time series data
        """
        # TODO: Implement FRED API integration
        # FRED API: https://fred.stlouisfed.org/docs/api/fred/
        pass


# Singleton instance
data_fetcher = DataFetcher()
