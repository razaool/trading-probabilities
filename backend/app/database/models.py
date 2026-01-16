"""
Database models for market data storage
"""

from sqlalchemy import create_engine, Column, String, Float, Integer, Date, Boolean, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create database engine
# Handle different connection arguments for SQLite vs PostgreSQL
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # For PostgreSQL and other databases
    # Optimize pool settings for Railway and other cloud providers
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=3,          # Reduce from default 5 to save resources
        max_overflow=5,       # Reduce from default 10 to save resources
        pool_recycle=3600,    # Recycle connections every hour to prevent stale connections
        pool_pre_ping=True,   # Test connections before using them
        connect_args={
            "connect_timeout": 10,  # Connection timeout
        }
    )

# Create session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for models
Base = declarative_base()


class Ticker(Base):
    """Ticker metadata table"""
    __tablename__ = "tickers"

    symbol = Column(String(10), primary_key=True)
    name = Column(String(255))
    exchange = Column(String(50))
    type = Column(String(20))  # 'stock', 'etf', 'index', 'indicator'
    data_available = Column(Boolean, default=True)
    earliest_date = Column(Date)
    latest_date = Column(Date)
    last_updated = Column(Date)


class HistoricalPrice(Base):
    """Historical OHLCV price data"""
    __tablename__ = "historical_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    adjusted_close = Column(Float)

    __table_args__ = (
        Index('idx_ticker_date', 'ticker', 'date', unique=True),
    )


class DailyReturn(Base):
    """Pre-computed daily returns for faster queries"""
    __tablename__ = "daily_returns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    return_pct = Column(Float)

    __table_args__ = (
        Index('idx_returns_ticker_date', 'ticker', 'date', unique=True),
    )


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
