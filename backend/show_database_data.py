#!/usr/bin/env python3
"""Display database contents"""

import sys
sys.path.insert(0, '/Users/razaool/trading-probabilities')

from app.database.models import SessionLocal, Ticker, HistoricalPrice, DailyReturn
from sqlalchemy import func

def show_database():
    """Display database contents"""
    db = SessionLocal()

    try:
        print("=" * 80)
        print("DATABASE CONTENTS - REAL HISTORICAL DATA")
        print("=" * 80)
        print()

        # Show tickers
        print("📊 TICKERS IN DATABASE:")
        print("-" * 80)
        tickers = db.query(Ticker).order_by(Ticker.symbol).all()

        print(f"{'Symbol':<8} | {'Name':<30} | {'Type':<6} | {'Records':>8} | {'Date Range'}")
        print("-" * 80)

        total_records = 0
        for t in tickers:
            price_count = db.query(HistoricalPrice).filter(HistoricalPrice.ticker == t.symbol).count()
            total_records += price_count
            date_range = f"{t.earliest_date} to {t.latest_date}"
            print(f"{t.symbol:<8} | {t.name:<30} | {t.type:<6} | {price_count:>8,} | {date_range}")

        print()
        print(f"Total price records in database: {total_records:,}")
        print()

        # Show sample data for SPY
        print("\n📈 SPY SAMPLE DATA (first 5 days):")
        print("-" * 80)
        spy_prices = db.query(HistoricalPrice).filter(
            HistoricalPrice.ticker == 'SPY'
        ).order_by(HistoricalPrice.date).limit(5).all()

        print(f"{'Date':<12} | {'Open':>8} | {'High':>8} | {'Low':>8} | {'Close':>8} | {'Volume':>12}")
        print("-" * 80)
        for p in spy_prices:
            print(f"{p.date} | ${p.open:>7.2f} | ${p.high:>7.2f} | ${p.low:>7.2f} | ${p.close:>7.2f} | {p.volume:>12,}")

        # Show latest SPY data
        print("\n📈 SPY LATEST DATA (last 5 days):")
        print("-" * 80)
        spy_latest = db.query(HistoricalPrice).filter(
            HistoricalPrice.ticker == 'SPY'
        ).order_by(HistoricalPrice.date.desc()).limit(5).all()

        print(f"{'Date':<12} | {'Open':>8} | {'High':>8} | {'Low':>8} | {'Close':>8} | {'Volume':>12}")
        print("-" * 80)
        for p in reversed(spy_latest):
            print(f"{p.date} | ${p.open:>7.2f} | ${p.high:>7.2f} | ${p.low:>7.2f} | ${p.close:>7.2f} | {p.volume:>12,}")

        # Show price statistics for all tickers
        print("\n📉 PRICE STATISTICS:")
        print("-" * 80)
        print(f"{'Symbol':<8} | {'Min Price':>10} | {'Max Price':>10} | {'Avg Price':>10} | {'Current':>10}")
        print("-" * 80)

        for t in tickers:
            min_price = db.query(func.min(HistoricalPrice.close)).filter(
                HistoricalPrice.ticker == t.symbol
            ).scalar()
            max_price = db.query(func.max(HistoricalPrice.close)).filter(
                HistoricalPrice.ticker == t.symbol
            ).scalar()
            avg_price = db.query(func.avg(HistoricalPrice.close)).filter(
                HistoricalPrice.ticker == t.symbol
            ).scalar()
            current_price = db.query(HistoricalPrice.close).filter(
                HistoricalPrice.ticker == t.symbol
            ).order_by(HistoricalPrice.date.desc()).first()

            if current_price:
                current_price = current_price[0]
                print(f"{t.symbol:<8} | ${min_price:>9.2f} | ${max_price:>9.2f} | ${avg_price:>9.2f} | ${current_price:>9.2f}")

        # Show some daily returns
        print("\n📊 RECENT DAILY RETURNS (SPY, last 10 days):")
        print("-" * 80)
        spy_returns = db.query(DailyReturn).filter(
            DailyReturn.ticker == 'SPY'
        ).order_by(DailyReturn.date.desc()).limit(10).all()

        print(f"{'Date':<12} | {'Return %':>10} | {'Move'}")
        print("-" * 80)
        for r in reversed(spy_returns):
            emoji = "🟢" if r.return_pct > 0 else "🔴" if r.return_pct < 0 else "⚪"
            print(f"{r.date} | {r.return_pct:>9.2f}% | {emoji}")

        print()
        print("=" * 80)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    show_database()
