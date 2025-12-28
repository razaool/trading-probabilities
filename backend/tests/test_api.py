"""
Integration tests for the Trading Probabilities API.
"""

def test_read_root(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_get_ticker_suggestions(client, sample_ticker):
    """Test ticker suggestions endpoint."""
    response = client.get("/api/tickers/suggest?q=A")
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)
    # Should find AAPL
    assert any(ticker["ticker"] == "AAPL" for ticker in data["suggestions"])


def test_get_ticker_suggestions_no_results(client):
    """Test ticker suggestions with no matches."""
    response = client.get("/api/tickers/suggest?q=XYZ123NOTFOUND")
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)
    assert len(data["suggestions"]) == 0


def test_get_historical_prices(client, db_session, sample_stock_data):
    """Test historical prices endpoint."""
    response = client.get("/api/prices/AAPL")
    assert response.status_code == 200
    data = response.json()

    assert "ticker" in data
    assert data["ticker"] == "AAPL"
    assert "prices" in data
    assert isinstance(data["prices"], list)
    assert len(data["prices"]) > 0

    # Verify price data structure
    price = data["prices"][0]
    assert "date" in price
    assert "close" in price


def test_get_historical_prices_invalid_ticker(client):
    """Test historical prices with invalid ticker."""
    response = client.get("/api/prices/INVALIDTICKER123")
    # Should return 500 or 404 depending on implementation
    assert response.status_code in [404, 500]


def test_query_historical_patterns_basic(client, db_session, sample_stock_data):
    """Test basic historical pattern query."""
    query = {
        "ticker": "AAPL",
        "condition_type": "percentage_change",
        "threshold": 2.0,
        "operator": "gte",
        "time_horizons": ["1d"]
    }

    response = client.post("/api/query", json=query)
    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "ticker" in data
    assert data["ticker"] == "AAPL"
    assert "total_occurrences" in data
    assert "instances" in data
    assert "summary_statistics" in data


def test_query_validation_error(client):
    """Test query with missing required fields."""
    query = {
        "ticker": "AAPL",
        # Missing threshold
        "operator": "gte",
        "time_horizons": ["1d"]
    }

    response = client.post("/api/query", json=query)
    assert response.status_code == 422  # Validation error


def test_query_different_time_horizons(client, db_session, sample_stock_data):
    """Test querying with multiple time horizons."""
    query = {
        "ticker": "AAPL",
        "condition_type": "percentage_change",
        "threshold": 2.0,
        "operator": "gte",
        "time_horizons": ["1d", "1w", "1m"]
    }

    response = client.post("/api/query", json=query)
    assert response.status_code == 200

    data = response.json()

    # Verify all requested time horizons are returned
    stats = data["summary_statistics"]
    assert "1d" in stats
    assert "1w" in stats
    assert "1m" in stats
