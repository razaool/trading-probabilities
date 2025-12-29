"""
Initialize Railway PostgreSQL database tables

Run this script to create the database tables on Railway if they don't exist.
"""

import sys
import os
from sqlalchemy import create_engine, text

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings


def init_tables():
    """Create database tables manually"""

    print("=" * 60)
    print("INITIALIZING POSTGRESQL DATABASE TABLES")
    print("=" * 60)

    engine = create_engine(settings.DATABASE_URL)

    print(f"\nConnecting to: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Railway'}")

    with engine.connect() as conn:
        # Create tickers table
        print("\nCreating tickers table...")
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS tickers (
                symbol VARCHAR(10) PRIMARY KEY,
                name VARCHAR(255),
                type VARCHAR(20),
                data_available BOOLEAN DEFAULT TRUE,
                earliest_date DATE,
                latest_date DATE,
                last_updated DATE
            )
        """))
        print("✅ tickers table created")

        # Create historical_prices table
        print("\nCreating historical_prices table...")
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS historical_prices (
                id SERIAL PRIMARY KEY,
                ticker VARCHAR(10) NOT NULL,
                date DATE NOT NULL,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume BIGINT,
                adjusted_close FLOAT,
                UNIQUE (ticker, date)
            )
        """))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_ticker_date ON historical_prices (ticker, date)"))
        print("✅ historical_prices table created")

        # Create daily_returns table
        print("\nCreating daily_returns table...")
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS daily_returns (
                id SERIAL PRIMARY KEY,
                ticker VARCHAR(10) NOT NULL,
                date DATE NOT NULL,
                return_pct FLOAT,
                UNIQUE (ticker, date)
            )
        """))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_returns_ticker_date ON daily_returns (ticker, date)"))
        print("✅ daily_returns table created")

        conn.commit()

    print("\n" + "=" * 60)
    print("DATABASE INITIALIZATION COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    init_tables()
