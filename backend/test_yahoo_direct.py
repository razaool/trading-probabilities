#!/usr/bin/env python3
"""Test direct Yahoo Finance URL access"""

import requests
import json
from datetime import datetime, timedelta

print("=" * 60)
print("Testing Direct Yahoo Finance API Access")
print("=" * 60)
print()

# Try to access Yahoo Finance directly
symbol = "SPY"

# Calculate date range for 1 month of data
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Yahoo Finance query URL format
base_url = "https://query2.finance.yahoo.com/v8/finance/chart/"
params = {
    "symbol": symbol,
    "period1": int(start_date.timestamp()),
    "period2": int(end_date.timestamp()),
    "interval": "1d",
    "includePrePost": True,
}

print(f"Fetching {symbol} data from {start_date.date()} to {end_date.date()}")
print(f"URL: {base_url}{symbol}")
print()

# Test different headers
headers_list = [
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    },
    {}
]

for i, headers in enumerate(headers_list, 1):
    print(f"Test {i}: Headers = {headers if headers else 'None'}")
    print("-" * 60)
    try:
        response = requests.get(
            f"{base_url}{symbol}",
            params=params,
            headers=headers,
            timeout=10
        )

        print(f"  Status Code: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"  Content Length: {len(response.content)} bytes")

        if response.status_code == 200:
            try:
                data = response.json()
                result = data.get("chart", {}).get("result", [])

                if result:
                    meta = result[0].get("meta", {})
                    timestamps = result[0].get("timestamp", [])
                    quotes = result[0].get("indicators", {}).get("quote", [{}])[0]

                    print(f"  ✅ SUCCESS!")
                    print(f"  Currency: {meta.get('currency', 'N/A')}")
                    print(f"  Data Points: {len(timestamps)}")

                    if timestamps:
                        print(f"  First Date: {datetime.fromtimestamp(timestamps[0])}")
                        print(f"  Last Date: {datetime.fromtimestamp(timestamps[-1])}")

                        # Show first few data points
                        print(f"\n  Sample Data:")
                        for j in range(min(3, len(timestamps))):
                            dt = datetime.fromtimestamp(timestamps[j])
                            open_p = quotes.get('open', [])[j]
                            close_p = quotes.get('close', [])[j]
                            print(f"    {dt.date()}: Open=${open_p:.2f}, Close=${close_p:.2f}")
                else:
                    print(f"  ❌ No results in response")
                    print(f"  Response keys: {list(data.keys())}")
            except json.JSONDecodeError as e:
                print(f"  ❌ JSON Decode Error: {e}")
                print(f"  First 200 chars of response: {response.text[:200]}")
        else:
            print(f"  ❌ Failed - Status: {response.status_code}")
            print(f"  Response: {response.text[:200]}")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    print()

print("=" * 60)
print("\nNext: Try alternative data sources")
print("=" * 60)

# Test yfinance with different settings
print("\nTesting yfinance with 'auto_adjust' parameter:")
try:
    import yfinance as yf
    ticker_obj = yf.Ticker("SPY")

    # Try different methods
    print("\n  Method 1: ticker.history()")
    hist = ticker_obj.history(period="1mo", auto_adjust=False)
    print(f"    Result: {len(hist)} rows" if not hist.empty else "    Result: Empty")

    print("\n  Method 2: ticker.history() with prepost")
    hist = ticker_obj.history(period="1mo", prepost=True)
    print(f"    Result: {len(hist)} rows" if not hist.empty else "    Result: Empty")

    print("\n  Method 3: ticker.history() with actions=False")
    hist = ticker_obj.history(period="1mo", actions=False)
    print(f"    Result: {len(hist)} rows" if not hist.empty else "    Result: Empty")

except Exception as e:
    print(f"  Error: {e}")
    import traceback
    traceback.print_exc()
