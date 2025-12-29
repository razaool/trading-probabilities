# Historical Pattern Analysis Tool

A web application that allows users to query historical market data based on specific conditions and analyze forward returns to identify trading patterns.

## Features

- Query historical data by market conditions (e.g. stock declined 3%, VIX exceeded 30)
- Forward returns analysis at 1 day, 1 week, 1 month, and 1 year
- Multi-asset support: stocks, ETFs, commodities, volatility indicators
- Summary statistics: average returns, median, win rate, best/worst cases
- Interactive React-based interface with Material-UI components

## Technology Stack

### Backend
- FastAPI
- PostgreSQL for data storage
- pandas for data manipulation
- yfinance for fetching market data

### Frontend
- React 18 with TypeScript
- Vite build tool
- Material-UI (MUI) components
- React Query for data fetching

## Deployment

- Backend: Railway (PostgreSQL database)
- Frontend: Vercel

## Database

The application uses PostgreSQL to store:
- 530 ticker symbols with metadata
- 4.46M historical price records
- 4.46M daily return records

All historical data is pre-loaded for fast query performance.

## API Endpoints

- `GET /health` - Health check
- `GET /api/tickers` - List available tickers
- `GET /api/tickers/suggest?q=<query>` - Search for tickers
- `POST /api/query` - Query historical patterns (requires API key)

## Usage Examples

### Percentage Change Query
- Ticker: NVDA
- Condition: Percentage Change
- Operator: less than
- Threshold: -3
- Result: Finds all days where NVDA declined more than 3%

### Absolute Threshold Query
- Ticker: VIX
- Condition: Absolute Threshold
- Operator: greater than
- Threshold: 30
- Result: Finds all days where VIX exceeded 30

## Supported Assets

- Market Indices: SPY, QQQ, DIA
- Sector ETFs: XLF, XLE, XLK, XLV, XLY, XLP
- Volatility: VIX, VXN
- Sentiment: Put/Call Ratio
- Commodities: GLD, USO, SLV
- 500+ stocks from major indices

## Development

### Backend
```bash
source venv/bin/activate
uvicorn backend.app.main:app --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

## License

MIT
