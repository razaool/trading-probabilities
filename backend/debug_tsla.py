#!/usr/bin/env python3
"""Debug TSLA query"""

import sys
sys.path.insert(0, '/Users/razaool/trading-probabilities')

import pandas as pd
from app.services.data_service import data_service

async def debug_query():
    """Debug the query to see what's happening"""

    # Fetch TSLA data
    print("Fetching TSLA data...")
    data = await data_service.fetch_historical_data("TSLA")

    print(f"Total records: {len(data)}")
    print(f"Date range: {data.index[0]} to {data.index[-1]}")
    print()

    # Calculate percentage changes
    pct_changes = data_service.calculate_percentage_change(data)

    print("Percentage change stats:")
    print(f"  Min: {pct_changes.min():.2f}%")
    print(f"  Max: {pct_changes.max():.2f}%")
    print(f"  Mean: {pct_changes.mean():.2f}%")
    print()

    # Filter for drops less than -20%
    threshold = -20
    mask = pct_changes < threshold
    matching_dates = data[mask].index.tolist()

    print(f"Days with drop < {threshold}%:")
    print(f"  Count: {len(matching_dates)}")

    if len(matching_dates) > 0:
        print(f"\nFirst 10 matching dates:")
        for i, date in enumerate(matching_dates[:10], 1):
            idx = data.index.get_loc(date)
            pct = pct_changes.iloc[idx]
            print(f"  {i}. {date.date()}: {pct:.2f}%")

        if len(matching_dates) > 10:
            print(f"\n... and {len(matching_dates) - 10} more")

if __name__ == "__main__":
    import asyncio
    asyncio.run(debug_query())
