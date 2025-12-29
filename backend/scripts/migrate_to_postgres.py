"""
Migrate data from SQLite to PostgreSQL database

This script exports data from the local SQLite database and imports it into Railway PostgreSQL
"""

import sys
import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
from tqdm import tqdm

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings


def migrate_data():
    """Migrate all data from SQLite to PostgreSQL"""

    print("=" * 60)
    print("MIGRATING DATA FROM SQLite TO PostgreSQL")
    print("=" * 60)

    # SQLite connection (local)
    sqlite_db_path = os.path.join(os.path.dirname(__file__), '../data/trading_patterns.db')
    sqlite_engine = create_engine(f'sqlite:///{sqlite_db_path}')

    # PostgreSQL connection (Railway)
    postgres_engine = create_engine(settings.DATABASE_URL)

    print(f"\nSQLite DB: {sqlite_db_path}")
    print(f"PostgreSQL DB: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Railway'}")

    # Migrate tickers table
    print("\n" + "=" * 60)
    print("1. MIGRATING TICKERS TABLE")
    print("=" * 60)

    try:
        tickers_df = pd.read_sql("SELECT * FROM tickers", sqlite_engine)
        print(f"Found {len(tickers_df)} tickers in SQLite")

        with postgres_engine.connect() as conn:
            for idx, row in tqdm(tickers_df.iterrows(), total=len(tickers_df), desc="Inserting tickers"):
                conn.execute(
                    text("""
                        INSERT INTO tickers (symbol, name, type, data_available, earliest_date, latest_date, last_updated)
                        VALUES (:symbol, :name, :type, :data_available, :earliest_date, :latest_date, :last_updated)
                        ON CONFLICT (symbol) DO UPDATE SET
                            name = EXCLUDED.name,
                            type = EXCLUDED.type,
                            data_available = EXCLUDED.data_available,
                            earliest_date = EXCLUDED.earliest_date,
                            latest_date = EXCLUDED.latest_date,
                            last_updated = EXCLUDED.last_updated
                    """),
                    {
                        'symbol': row['symbol'],
                        'name': row['name'],
                        'type': row['type'],
                        'data_available': row['data_available'],
                        'earliest_date': row['earliest_date'],
                        'latest_date': row['latest_date'],
                        'last_updated': row['last_updated']
                    }
                )
            conn.commit()
        print(f"✅ Successfully migrated {len(tickers_df)} tickers")
    except Exception as e:
        print(f"❌ Error migrating tickers: {e}")
        import traceback
        traceback.print_exc()

    # Migrate historical_prices table in batches
    print("\n" + "=" * 60)
    print("2. MIGRATING HISTORICAL PRICES TABLE")
    print("=" * 60)

    try:
        # Get total count first
        with sqlite_engine.connect() as conn:
            total_count = conn.execute(text("SELECT COUNT(*) FROM historical_prices")).scalar()
        print(f"Found {total_count:,} price records in SQLite")

        # Read and insert in batches of 10,000
        batch_size = 10000
        offset = 0

        with postgres_engine.connect() as pg_conn:
            with sqlite_engine.connect() as sqlite_conn:
                while offset < total_count:
                    # Read batch
                    batch_df = pd.read_sql(
                        f"SELECT * FROM historical_prices ORDER BY ticker, date LIMIT {batch_size} OFFSET {offset}",
                        sqlite_conn
                    )

                    # Insert batch
                    for idx, row in tqdm(batch_df.iterrows(), total=len(batch_df),
                                        desc=f"Inserting prices {offset:,}-{offset+len(batch_df):,}"):
                        pg_conn.execute(
                            text("""
                                INSERT INTO historical_prices
                                (ticker, date, open, high, low, close, volume, adjusted_close)
                                VALUES (:ticker, :date, :open, :high, :low, :close, :volume, :adj_close)
                                ON CONFLICT (ticker, date) DO UPDATE SET
                                    open = EXCLUDED.open,
                                    high = EXCLUDED.high,
                                    low = EXCLUDED.low,
                                    close = EXCLUDED.close,
                                    volume = EXCLUDED.volume,
                                    adjusted_close = EXCLUDED.adjusted_close
                            """),
                            {
                                'ticker': row['ticker'],
                                'date': row['date'],
                                'open': float(row['open']) if pd.notna(row['open']) else None,
                                'high': float(row['high']) if pd.notna(row['high']) else None,
                                'low': float(row['low']) if pd.notna(row['low']) else None,
                                'close': float(row['close']) if pd.notna(row['close']) else None,
                                'volume': int(row['volume']) if pd.notna(row['volume']) else None,
                                'adj_close': float(row['adjusted_close']) if pd.notna(row['adjusted_close']) else None
                            }
                        )

                    # Commit batch
                    pg_conn.commit()
                    offset += len(batch_df)

        print(f"✅ Successfully migrated {total_count:,} price records")
    except Exception as e:
        print(f"❌ Error migrating prices: {e}")
        import traceback
        traceback.print_exc()

    # Migrate daily_returns table in batches
    print("\n" + "=" * 60)
    print("3. MIGRATING DAILY RETURNS TABLE")
    print("=" * 60)

    try:
        # Get total count first
        with sqlite_engine.connect() as conn:
            total_count = conn.execute(text("SELECT COUNT(*) FROM daily_returns")).scalar()
        print(f"Found {total_count:,} return records in SQLite")

        # Read and insert in batches
        batch_size = 10000
        offset = 0

        with postgres_engine.connect() as pg_conn:
            with sqlite_engine.connect() as sqlite_conn:
                while offset < total_count:
                    # Read batch
                    batch_df = pd.read_sql(
                        f"SELECT * FROM daily_returns LIMIT {batch_size} OFFSET {offset}",
                        sqlite_conn
                    )

                    # Insert batch
                    for idx, row in tqdm(batch_df.iterrows(), total=len(batch_df),
                                        desc=f"Inserting returns {offset:,}-{offset+len(batch_df):,}"):
                        if pd.notna(row['return_pct']):
                            pg_conn.execute(
                                text("""
                                    INSERT INTO daily_returns (ticker, date, return_pct)
                                    VALUES (:ticker, :date, :return_pct)
                                    ON CONFLICT (ticker, date) DO UPDATE SET
                                        return_pct = EXCLUDED.return_pct
                                """),
                                {
                                    'ticker': row['ticker'],
                                    'date': row['date'],
                                    'return_pct': float(row['return_pct'])
                                }
                            )

                    # Commit batch
                    pg_conn.commit()
                    offset += len(batch_df)

        print(f"✅ Successfully migrated {total_count:,} return records")
    except Exception as e:
        print(f"❌ Error migrating returns: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("MIGRATION COMPLETE!")
    print("=" * 60)

    # Verify counts in PostgreSQL
    print("\nVerifying PostgreSQL data:")
    with postgres_engine.connect() as conn:
        ticker_count = conn.execute(text("SELECT COUNT(*) FROM tickers")).scalar()
        price_count = conn.execute(text("SELECT COUNT(*) FROM historical_prices")).scalar()
        return_count = conn.execute(text("SELECT COUNT(*) FROM daily_returns")).scalar()

        print(f"  Tickers: {ticker_count:,}")
        print(f"  Price records: {price_count:,}")
        print(f"  Return records: {return_count:,}")


if __name__ == "__main__":
    migrate_data()
