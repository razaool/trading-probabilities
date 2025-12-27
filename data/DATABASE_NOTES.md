# Database Information

## Current Database Status

**Last Updated:** December 27, 2025

- **Total Tickers:** 518
- **Total Price Records:** 4,402,970
- **SPY Components:** 501/503 (99.6%)

## Data Sources

The database contains historical stock data from Yahoo Finance for:
- All QQQ (Nasdaq-100) components
- 501/503 SPY (S&P 500) components
- Major market indices (SPY, QQQ)

## Known Limitations

### Dot Notation Tickers

The following tickers could not be fetched due to Yahoo Finance API limitations with dot notation in ticker symbols:

- **BF.B** (Brown-Forman)
- **BRK.B** (Berkshire Hathaway Class B)

These tickers consistently fail with `YFPricesMissingError` and `YFTzMissingError` when fetched through yfinance. This is a known issue with the yfinance library when handling ticker symbols containing periods.

## Database File

The SQLite database file is located at:
```
backend/data/trading_patterns.db
```

**Note:** The database file is excluded from Git via .gitignore due to its size (170+ MB). Users who clone this repository will need to fetch the data separately using the data fetching scripts.

## Fetching Data

To fetch stock data, use the data service:
```python
from app.services.data_service import data_service

# Fetch historical data for a ticker
data = await data_service.fetch_historical_data("AAPL", period="max")
```

## Database Schema

### Tables

1. **historical_prices** - Daily OHLCV data
   - ticker, date, open, high, low, close, volume, adjusted_close

2. **daily_returns** - Calculated daily percentage changes
   - ticker, date, return_pct

3. **tickers** - Ticker metadata
   - symbol, name, type, data_available, earliest_date, latest_date, last_updated
