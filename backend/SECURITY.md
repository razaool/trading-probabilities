# Security Guide

This document outlines the security features implemented in the Historical Pattern Analysis Tool.

## Authentication (API Keys)

### Overview
API key authentication can be enabled to restrict access to protected endpoints.

### Configuration
Set the following environment variables in your `.env` file:

```bash
# Enable authentication (set to 'true' for production)
REQUIRE_AUTH=true

# Comma-separated list of valid API keys
API_KEYS=your-secret-key-1,another-secret-key-2
```

### Frontend Configuration
Update your frontend `.env` file to include the API key:

```bash
VITE_API_KEY=your-secret-key-1
```

### Protected Endpoints
The following endpoints require authentication when `REQUIRE_AUTH=true`:
- `POST /api/query` - Execute historical pattern queries
- `GET /api/prices/{ticker}` - Get historical price data
- `GET /api/tickers/etf/{etf_ticker}` - Get ETF constituents

### Public Endpoints
These endpoints remain publicly accessible:
- `GET /` - Root endpoint with API info
- `GET /health` - Health check
- `GET /api/tickers` - List available tickers
- `GET /api/tickers/suggest?q={query}` - Search for tickers

## Rate Limiting

### Overview
Rate limiting protects the API from abuse by limiting the number of requests per IP address.

### Configuration
```bash
# Enable/disable rate limiting
ENABLE_RATE_LIMIT=true

# Maximum requests per minute per IP
RATE_LIMIT_PER_MINUTE=10

# Burst size (temporary allowance)
RATE_LIMIT_BURST=20
```

### Protected Endpoints
Rate limiting is applied to:
- `POST /api/query` - 10 requests per minute
- `GET /api/prices/{ticker}` - 10 requests per minute
- `GET /api/tickers/etf/{etf_ticker}` - 10 requests per minute

### Response
When rate limit is exceeded:
```json
{
  "detail": "Rate limit exceeded: 10 per 1 minute"
}
```

HTTP Status: 429 Too Many Requests

## CORS (Cross-Origin Resource Sharing)

### Configuration
Always set `CORS_ORIGINS` to your actual frontend domain in production:

```bash
# Production example
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Local development
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### ⚠️ WARNING
Never use `CORS_ORIGINS=["*"]` in production. This allows any website to call your API.

## Logging

### Overview
All requests are logged with timing information for monitoring and debugging.

### Log Files
- `logs/app.log` - All application logs
- `logs/errors.log` - Error-level logs only

### Log Format
```
2025-12-28 10:30:45 - INFO - Request: GET /api/query
2025-12-28 10:30:46 - INFO - Response: 200 - GET /api/query - 1.234s
```

### Disabling Logging
To disable logs, comment out the `setup_logging()` call in `app/main.py`.

## Security Best Practices

### For Production Deployment

1. **Enable Authentication**
   ```bash
   REQUIRE_AUTH=true
   API_KEYS=your-strong-random-key-here
   ```

2. **Set Proper CORS Origins**
   ```bash
   CORS_ORIGINS=https://yourdomain.com
   ```

3. **Enable Rate Limiting**
   ```bash
   ENABLE_RATE_LIMIT=true
   RATE_LIMIT_PER_MINUTE=10
   ```

4. **Use HTTPS**
   - Deploy behind a reverse proxy (nginx, Caddy)
   - Enable HTTPS/TLS
   - Redirect HTTP to HTTPS

5. **Secure API Keys**
   - Generate strong, random API keys (32+ characters)
   - Rotate keys periodically
   - Never commit keys to git

6. **Monitor Logs**
   - Review `logs/errors.log` regularly
   - Set up log aggregation for production

7. **Database Security**
   - Switch from SQLite to PostgreSQL for production
   - Use strong database passwords
   - Enable database SSL connections

### Generating Secure API Keys

Using Python:
```python
import secrets
print(secrets.token_urlsafe(32))
```

Using OpenSSL:
```bash
openssl rand -base64 32
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `REQUIRE_AUTH` | `false` | Enable API key authentication |
| `API_KEYS` | (empty) | Comma-separated valid API keys |
| `ENABLE_RATE_LIMIT` | `true` | Enable rate limiting |
| `RATE_LIMIT_PER_MINUTE` | `10` | Max requests per minute per IP |
| `RATE_LIMIT_BURST` | `20` | Burst allowance for rate limiting |
| `CORS_ORIGINS` | localhost URLs | Allowed frontend origins |

## Testing Authentication

### With curl (Authenticated)
```bash
curl -X POST http://localhost:8000/api/query \
  -H "X-API-Key: your-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "condition_type": "percentage_change",
    "threshold": 2.0,
    "operator": "gte",
    "time_horizons": ["1d"]
  }'
```

### Without API Key (Will Fail if Auth Enabled)
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", ...}'
```

Response:
```json
{
  "detail": "API key is missing. Please provide X-API-Key header."
}
```

## Troubleshooting

### "API key is missing" Error
- Ensure `X-API-Key` header is included in requests
- Check frontend `.env` has `VITE_API_KEY` set
- Verify backend `REQUIRE_AUTH` matches your expectations

### "Invalid API key" Error
- Check that the API key matches one in `API_KEYS` list
- Ensure no extra spaces in comma-separated `API_KEYS`
- Regenerate key if compromised

### "Rate limit exceeded" Error
- Wait 1 minute before retrying
- Increase `RATE_LIMIT_PER_MINUTE` if needed
- Implement exponential backoff in frontend

### CORS Errors
- Verify `CORS_ORIGINS` includes your frontend URL
- Check for typos in domain names
- Include protocol (http:// or https://)
