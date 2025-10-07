"""
Database models for stock data
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Text, Boolean, Index
from sqlalchemy.sql import func
from app.core.database import Base


class Stock(Base):
    """Stock metadata"""
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    sector = Column(String(100))
    industry = Column(String(100))
    market_cap = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class StockPrice(Base):
    """Daily OHLCV price data"""
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float, nullable=False)
    volume = Column(Float)
    adj_close = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('idx_ticker_date', 'ticker', 'date', unique=True),
    )


class StockFundamentals(Base):
    """Fundamental data"""
    __tablename__ = "stock_fundamentals"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)

    # Valuation
    pe_ratio = Column(Float)
    pb_ratio = Column(Float)
    ps_ratio = Column(Float)

    # Profitability
    roe = Column(Float)
    roa = Column(Float)
    profit_margin = Column(Float)

    # Growth
    revenue_growth = Column(Float)
    earnings_growth = Column(Float)

    # Financial Health
    debt_to_equity = Column(Float)
    current_ratio = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class News(Base):
    """News articles"""
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True)
    headline = Column(String(500), nullable=False)
    summary = Column(Text)
    url = Column(String(1000))
    source = Column(String(100))
    sentiment_score = Column(Float)  # -1 to 1
    published_at = Column(DateTime(timezone=True), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SECFiling(Base):
    """SEC filings (8-K, 10-K, 10-Q, etc.)"""
    __tablename__ = "sec_filings"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True, nullable=False)
    filing_type = Column(String(20), index=True, nullable=False)  # 8-K, 10-K, 10-Q, etc.
    filing_date = Column(Date, index=True, nullable=False)
    url = Column(String(1000))
    summary = Column(Text)
    is_material = Column(Boolean, default=False)  # Material event flag
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Recommendation(Base):
    """Daily stock recommendations"""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True, nullable=False)
    recommendation_date = Column(Date, index=True, nullable=False)

    # Scores
    technical_score = Column(Float, nullable=False)  # 0-10
    fundamental_score = Column(Float, nullable=False)  # 0-10
    catalyst_score = Column(Float, nullable=False)  # 0-10
    total_score = Column(Float, nullable=False)  # Weighted average

    # Recommendation details
    action = Column(String(10))  # BUY, SELL, HOLD, WATCH
    reasoning = Column(Text)
    catalyst = Column(Text)
    risk_reward = Column(Float)
    stop_loss = Column(Float)
    target_price = Column(Float)

    # Ranking
    rank = Column(Integer)  # Daily rank (1 = top pick)
    is_top_pick = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
