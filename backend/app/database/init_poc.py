"""
Proof of Concept: Initialize database with popular tickers

Run this script to populate the database with initial data:
    python -m app.database.init_poc
"""

import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from app.database.models import Base, engine, SessionLocal, Ticker, HistoricalPrice, DailyReturn
from app.services.yahoo_direct_fetcher import yahoo_fetcher

# POC: Start with popular tickers
POC_TICKERS = {
    "SPY": "SPDR S&P 500 ETF",
    "QQQ": "Invesco QQQ Trust",
    "NVDA": "NVIDIA Corporation",
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com Inc.",
    "TSLA": "Tesla Inc.",
    "META": "Meta Platforms Inc.",
}


def init_database():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created\n")


def populate_ticker_data(ticker: str, name: str, db: Session):
    """
    Fetch data from Yahoo Finance API and store in database

    Args:
        ticker: Ticker symbol
        name: Company name
        db: Database session
    """
    print(f"Fetching {ticker} ({name})...")

    try:
        # Fetch maximum historical data using our custom fetcher
        data = yahoo_fetcher.fetch_data(ticker, period="max")

        if data is None or data.empty:
            print(f"  ⚠️  No data available for {ticker}")
            return False

        # Insert ticker metadata
        ticker_obj = Ticker(
            symbol=ticker,
            name=name,
            type="stock" if ticker not in ["SPY", "QQQ"] else "etf",
            data_available=True,
            earliest_date=data.index[0].date(),
            latest_date=data.index[-1].date(),
            last_updated=datetime.now().date()
        )
        db.merge(ticker_obj)

        # Insert price data
        price_count = 0
        for date_idx, row in data.iterrows():
            # Convert Timestamp to date
            date_val = date_idx.date() if hasattr(date_idx, 'date') else date_idx

            price = HistoricalPrice(
                ticker=ticker,
                date=date_val,
                open=float(row['Open']),
                high=float(row['High']),
                low=float(row['Low']),
                close=float(row['Close']),
                volume=int(row['Volume']),
                adjusted_close=float(row['Adj Close'])
            )
            db.merge(price)
            price_count += 1

        # Calculate and insert daily returns
        data_copy = data.copy()
        data_copy['daily_return'] = data_copy['Close'].pct_change() * 100

        return_count = 0
        for date_idx, row in data_copy.iterrows():
            date_val = date_idx.date() if hasattr(date_idx, 'date') else date_idx

            if pd.notna(row['daily_return']):
                ret = DailyReturn(
                    ticker=ticker,
                    date=date_val,
                    return_pct=float(row['daily_return'])
                )
                db.merge(ret)
                return_count += 1

        db.commit()
        print(f"  ✅ Loaded {price_count} price records, {return_count} return records")
        return True

    except Exception as e:
        print(f"  ❌ Error loading {ticker}: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False


def main():
    """Main entry point for database initialization"""
    print("=" * 60)
    print("Proof of Concept: Database Initialization")
    print("=" * 60)
    print()

    # Step 1: Create tables
    init_database()

    # Step 2: Populate data
    print("Populating database with proof of concept data...")
    print()

    db = SessionLocal()
    try:
        success_count = 0
        for ticker, name in POC_TICKERS.items():
            if populate_ticker_data(ticker, name, db):
                success_count += 1

        print()
        print("=" * 60)
        print(f"✅ Database initialization complete!")
        print(f"   Successfully loaded: {success_count}/{len(POC_TICKERS)} tickers")
        print("=" * 60)

        # Show summary
        from app.database.models import Ticker
        tickers = db.query(Ticker).all()
        print(f"\n📊 Database Summary:")
        for t in tickers:
            print(f"   • {t.symbol}: {t.earliest_date} to {t.latest_date}")

    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
