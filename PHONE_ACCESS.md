# Phone Access Setup

This application can be accessed from your phone when both devices are on the same WiFi network.

## Current Configuration

- **Your local IP**: `192.168.1.66`
- **Frontend URL**: `http://192.168.1.66:5173`
- **Backend API**: `http://192.168.1.66:8000`

## Steps to Access from Phone

### 1. Stop Current Servers

Stop any running frontend and backend servers.

### 2. Start Backend (Network Accessible)

```bash
./run-backend-network.sh
```

Or manually:
```bash
cd backend
export PYTHONPATH="$PYTHONPATH:/Users/razaool/trading-probabilities/backend"
../venv/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be accessible at `http://192.168.1.66:8000`

### 3. Start Frontend (Network Accessible)

```bash
./run-frontend-network.sh
```

Or manually:
```bash
cd frontend
npm run dev
```

The frontend will be accessible at `http://192.168.1.66:5173`

### 4. Access from Phone

1. Make sure your phone is connected to the **same WiFi network** as your computer
2. Open your phone's browser
3. Navigate to: `http://192.168.1.66:5173`

## Important Notes

- **Both devices must be on the same WiFi network**
- **Your computer's firewall must allow connections on ports 5173 and 8000**
- **The IP address may change if you reconnect to WiFi** - check with:
  ```bash
  ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null
  ```
- If the IP changes, update:
  - `frontend/.env` (VITE_API_URL)
  - `backend/app/core/config.py` (CORS_ORIGINS)

## Troubleshooting

### Can't access from phone

1. **Check firewall settings**:
   ```bash
   # Allow incoming connections on macOS
   # System Settings → Network → Firewall
   ```

2. **Verify both servers are running**:
   ```bash
   curl http://192.168.1.66:8000/health
   curl http://192.168.1.66:5173
   ```

3. **Check IP address**:
   ```bash
   ipconfig getifaddr en0
   ```

4. **Ensure phone is on same WiFi**:
   - Check WiFi network name on both devices

### CORS Errors

If you see CORS errors in the browser console:
- Verify `backend/app/core/config.py` includes your phone's potential IP in CORS_ORIGINS
- Restart the backend after updating CORS settings

### Connection Refused

- Make sure both servers are started with `--host 0.0.0.0` (backend) or `host: '0.0.0.0'` (frontend)
- Check that ports 5173 and 8000 are not blocked by firewall
