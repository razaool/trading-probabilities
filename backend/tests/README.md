# Integration Tests for Trading Probabilities API

This directory contains integration tests for the Trading Probabilities backend API.

## Running Tests

From the backend directory:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py -v

# Run specific test
pytest tests/test_api.py::test_read_root -v
```

## Test Coverage

Current tests cover:

- ✅ Root endpoint
- ✅ Ticker suggestions API
- ✅ Historical prices API
- ✅ Query historical patterns API
- ✅ Input validation
- ✅ Multiple time horizons
- ✅ Error handling (404, 422)

## Test Structure

- `conftest.py` - Pytest fixtures and test configuration
- `test_api.py` - API endpoint integration tests

## Fixtures

- `client` - FastAPI test client with test database
- `db_session` - In-memory SQLite database session
- `sample_ticker` - Creates a sample ticker (AAPL) in the database
- `sample_stock_data` - Creates 100 days of sample price data

## Notes

- Tests use an in-memory SQLite database for isolation
- Each test gets a fresh database
- Tests are independent and can run in parallel
