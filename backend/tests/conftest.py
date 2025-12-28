import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.models import Base
from app.database import get_db

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Create a test client with a test database session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_ticker(db_session):
    """Create a sample ticker in the database."""
    from app.database.models import Ticker

    ticker = Ticker(
        symbol="AAPL",
        name="Apple Inc.",
        type="stock"
    )
    db_session.add(ticker)
    db_session.commit()
    db_session.refresh(ticker)
    return ticker


@pytest.fixture
def sample_stock_data(db_session):
    """Create sample stock price data."""
    from app.database.models import HistoricalPrice
    from datetime import datetime, timedelta
    import random

    base_date = datetime(2024, 1, 1)
    prices = []

    # Generate 100 days of sample data
    for i in range(100):
        date = base_date + timedelta(days=i)
        # Skip weekends
        if date.weekday() >= 5:
            continue

        price = 150 + random.uniform(-10, 10)  # Random price around $150

        stock_data = HistoricalPrice(
            ticker="AAPL",
            date=date,
            open=price,
            high=price * 1.02,
            low=price * 0.98,
            close=price,
            volume=1000000
        )
        db_session.add(stock_data)

    db_session.commit()
    return "AAPL"
