#!/bin/bash
# Start backend server accessible from local network
cd /Users/razaool/trading-probabilities/backend
export PYTHONPATH="$PYTHONPATH:/Users/razaool/trading-probabilities/backend"
/Users/razaool/trading-probabilities/venv/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
