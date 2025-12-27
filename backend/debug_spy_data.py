#!/usr/bin/env python3
"""Debug SPY data and percentage changes"""

import sys
sys.path.insert(0, '/Users/razaool/trading-probabilities')

import pandas as pd
from app.services.data_service import data_service

async def debug_spy():
    """Debug SPY data to check percentage changes"""
    print("Fetching SPY data from database...")
    data = await data_service.fetch_historical_data("SPY")

    print(f"\nTotal records: {len(data)}")
    print(f"Columns: {data.columns.tolist()}")
    print(f"\nFirst 5 rows:")
    print(data.head())
    print(f"\nLast 5 rows:")
    print(data.tail())

    # Calculate percentage changes
    pct_changes = data_service.calculate_percentage_change(data)

    print(f"\n{'='*60}")
    print("PERCENTAGE CHANGE STATISTICS")
    print(f"{'='*60}")
    print(f"Min: {pct_changes.min():.2f}%")
    print(f"Max: {pct_changes.max():.2f}%")
    print(f"Mean: {pct_changes.mean():.2f}%")
    print(f"Median: {pct_changes.median():.2f}%")

    # Count drops less than -5%
    threshold = -5
    mask = pct_changes < threshold
    drops_below_threshold = pct_changes[mask]

    print(f"\nDays with drop < {threshold}%:")
    print(f"  Count: {len(drops_below_threshold)}")

    if len(drops_below_threshold) > 0:
        print(f"\nFirst 20 drops:")
        for i, (date, pct) in enumerate(drops_below_threshold.head(20).items(), 1):
            print(f"  {i}. {date.date()}: {pct:.2f}%")

if __name__ == "__main__":
    import asyncio
    asyncio.run(debug_spy())
