# Historical Pattern Analysis Tool for Trading

A web application that allows users to query historical market data based on specific conditions and analyze forward returns to identify trading patterns.

## Features

- **Query Historical Data**: Search for specific market conditions (e.g., "NVDA declined 3%", "VIX exceeded 30")
- **Forward Returns Analysis**: See what happened after those conditions at 1 day, 1 week, 1 month, and 1 year
- **Multi-Asset Support**: Stocks, ETFs, commodities, volatility indicators, and sentiment indicators
- **Summary Statistics**: Average returns, median, win rate, best/worst cases, and more
- **Interactive UI**: Modern React-based interface with Material-UI components

## Project Structure

```
trading-probabilities/
├── backend/                 # FastAPI Python backend
│   └── app/
│       ├── api/            # API endpoints
│       ├── core/           # Configuration and settings
│       ├── models/         # Pydantic schemas
│       ├── services/       # Business logic
│       └── utils/          # Utility functions
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API service layer
│   │   ├── theme/         # Material-UI theme
│   │   └── types/         # TypeScript types
│   └── package.json
├── data/                   # Database and cached data
├── logs/                   # Application logs
└── requirements.txt        # Python dependencies
```

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **pandas**: Data manipulation and analysis
- **yfinance**: Fetching historical market data
- **Pydantic**: Data validation and settings management

### Frontend
- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Build tool and dev server
- **Material-UI (MUI)**: React component library
- **React Query**: Data fetching and caching
- **Axios**: HTTP client

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd trading-probabilities
   ```

2. **Set up the backend**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Configure environment variables**
   ```bash
   # Backend (root directory)
   cp .env.example .env

   # Frontend (frontend directory)
   cp frontend/.env.example frontend/.env
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   # Activate virtual environment
   source venv/bin/activate

   # Run FastAPI server
   uvicorn backend.app.main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

2. **Start the frontend development server**
   ```bash
   cd frontend
   npm run dev
   ```

   The application will be available at `http://localhost:5173`

## Usage

### Example Queries

1. **Percentage Change Query**
   - Ticker: NVDA
   - Condition Type: Percentage Change
   - Operator: `<`
   - Threshold: -3
   - Interpretation: "Find all days where NVDA declined more than 3%"

2. **Absolute Threshold Query**
   - Ticker: VIX
   - Condition Type: Absolute Threshold
   - Operator: `>`
   - Threshold: 30
   - Interpretation: "Find all days where VIX exceeded 30"

### Supported Assets

- **Market Indices**: SPY, QQQ, DIA, IWM
- **Sector ETFs**: XLF, XLE, XLK, XLV, XLY, XLP
- **Volatility Indicators**: VIX, VXN, RVX
- **Sentiment Indicators**: Put/Call Ratio
- **Commodities**: GLD, USO, SLV
- **Top 100 Stocks** (coming soon)

## API Endpoints

- `GET /health` - Health check
- `GET /api/tickers` - Get list of available tickers
- `POST /api/query` - Query historical patterns

## Development

### Backend Development
```bash
# Run with auto-reload
uvicorn backend.app.main:app --reload

# Run tests
pytest

# Format code
black backend/
ruff check backend/
```

### Frontend Development
```bash
cd frontend
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Roadmap

- [ ] Add top 100 stocks by market cap
- [ ] Implement confidence scoring algorithm
- [ ] Add visualization charts
- [ ] Support for custom date ranges
- [ ] Export results to CSV/Excel
- [ ] Add more indicators and metrics
- [ ] Implement user authentication
- [ ] Save and share queries
