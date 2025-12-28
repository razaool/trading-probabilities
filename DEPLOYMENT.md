# Deployment Guide - Railway + Vercel

This guide walks you through deploying the Trading Probabilities application using Railway (backend) and Vercel (frontend).

## Architecture Overview

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Vercel App    │ ───> │  Railway API    │ ───> │  Railway DB     │
│  (Frontend)     │      │   (Backend)     │      │  (PostgreSQL)   │
│  React + Vite   │      │   FastAPI       │      │                 │
└─────────────────┘      └─────────────────┘      └─────────────────┘
     https://              https://                   Internal
your-site.vercel.app   your-api.railway.app      (railway internal)
```

## Prerequisites

- GitHub account with repository access
- Railway account ([railway.app](https://railway.app))
- Vercel account ([vercel.com](https://vercel.com))
- Railway free tier ($5 credit one-time)
- Vercel free tier (hobby plan)

---

## Part 1: Deploy Backend to Railway

### Step 1: Create New Project on Railway

1. Go to [railway.app](https://railway.app) and log in
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your `trading-probabilities` repository
4. Click **"Deploy Now"**

### Step 2: Configure Backend Service

Railway will auto-detect your Python project. Configure it:

1. Click on your backend service
2. Go to **Settings** tab
3. Set **Root Directory**: `backend`
4. Set **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Add PostgreSQL Database

1. In your Railway project, click **"New Service"**
2. Select **Database** → **PostgreSQL**
3. Railway will provision a PostgreSQL database

### Step 4: Set Environment Variables

Go to your backend service → **Variables** tab, and add:

```bash
# Authentication (generate a secure key)
REQUIRE_AUTH=true
API_KEYS=your-super-secure-random-key-here-32-chars-min

# Rate Limiting
ENABLE_RATE_LIMIT=true
RATE_LIMIT_PER_MINUTE=10

# CORS (replace with your Vercel URL)
CORS_ORIGINS=https://your-site.vercel.app

# Database (Railway sets this automatically)
# DATABASE_URL is set by Railway's PostgreSQL service

# Data Cache
DATA_CACHE_ENABLED=true
DATA_CACHE_TTL=86400
```

**Generating a Secure API Key:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

Or use: https://www.uuidgenerator.net/api/guid

### Step 5: Get Your API URL

After deployment completes:
1. Go to your backend service
2. Copy the **Public Domain** (e.g., `your-api.railway.app`)
3. Your API URL will be: `https://your-api.railway.app`

### Step 6: Test the Backend

```bash
# Test health endpoint
curl https://your-api.railway.app/health

# Should return: {"status":"healthy"}
```

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Create New Project on Vercel

1. Go to [vercel.com](https://vercel.com) and log in
2. Click **"Add New"** → **"Project"**
3. Import your `trading-probabilities` GitHub repository

### Step 2: Configure Project Settings

Set these configuration options:

**Framework Preset:** Vite

**Root Directory:** `frontend`

**Build Command:** `npm run build`

**Output Directory:** `dist`

**Install Command:** `npm install`

### Step 3: Set Environment Variables

Go to **Settings** → **Environment Variables**, and add:

```bash
# Backend API URL (from Railway)
VITE_API_URL=https://your-api.railway.app

# API Key (same as Railway backend)
VITE_API_KEY=your-super-secure-random-key-here-32-chars-min
```

**Important:** Select all environments (Production, Preview, Development)

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait for build to complete (~1-2 minutes)
3. Vercel will provide a URL: `https://your-site.vercel.app`

---

## Part 3: Update CORS Configuration

After you have your Vercel URL, go back to Railway:

1. Open your backend service → **Variables** tab
2. Update `CORS_ORIGINS`:
   ```bash
   CORS_ORIGINS=https://your-site.vercel.app
   ```
3. Railway will automatically redeploy

---

## Part 4: Database Setup (One Time)

Your Railway PostgreSQL database needs to be initialized. Railway will handle the schema automatically on first deployment, but you may want to seed it with initial data.

### Option 1: Automatic (Recommended)

The app will auto-create tables on first run via SQLAlchemy.

### Option 2: Manual Seed

If you want to pre-populate data:

1. Go to Railway → PostgreSQL service
2. Click **"Query"** tab
3. Run seed queries or use the Python script in `scripts/seed_db.py`

---

## Part 5: Verify Deployment

### Test Frontend → Backend Connection

1. Open your Vercel URL: `https://your-site.vercel.app`
2. Try querying a stock (e.g., AAPL)
3. Check the Railway logs to see requests coming through

### Test with curl

```bash
# Test health check
curl https://your-api.railway.app/health

# Test query (with API key)
curl -X POST https://your-api.railway.app/api/query \
  -H "X-API-Key: your-super-secure-random-key-here-32-chars-min" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "condition_type": "percentage_change",
    "threshold": 2.0,
    "operator": "gte",
    "time_horizons": ["1d"]
  }'
```

---

## Part 6: Custom Domain (Optional)

### Frontend (Vercel)

1. Go to Vercel project → **Settings** → **Domains**
2. Add your custom domain
3. Configure DNS records as instructed by Vercel

### Backend (Railway)

1. Go to Railway project → **Settings** → **Domains**
2. Add your custom domain (e.g., `api.yourdomain.com`)
3. Configure DNS records
4. Update CORS origins in Railway variables

---

## Monitoring & Logs

### Railway (Backend)

- **Logs**: Click service → **Metrics** tab → **Logs**
- **Database**: PostgreSQL service → **Metrics** tab
- **Uptime**: Built-in health checks at `/health`

### Vercel (Frontend)

- **Logs**: Project → **Deployments** → Click deployment → **Function Logs**
- **Analytics**: Project → **Analytics** tab
- **Uptime**: Vercel handles automatically

---

## Troubleshooting

### Issue: CORS Errors

**Symptoms**: Browser console shows CORS policy errors

**Solution**:
1. Check Railway `CORS_ORIGINS` variable includes your Vercel URL
2. Ensure URL starts with `https://` (not `http://`)
3. Redeploy Railway service

### Issue: 502 Bad Gateway

**Symptoms**: Frontend can't reach backend

**Solution**:
1. Check Railway service is running (not paused)
2. Verify `VITE_API_URL` in Vercel env vars
3. Test backend health endpoint directly

### Issue: Database Connection Errors

**Symptoms**: Backend logs show database connection failures

**Solution**:
1. Verify PostgreSQL service is running in Railway
2. Check `DATABASE_URL` is set (Railway sets this automatically)
3. Ensure both services are in the same Railway project

### Issue: Rate Limiting Too Aggressive

**Symptoms**: Legitimate requests are blocked

**Solution**:
1. Increase `RATE_LIMIT_PER_MINUTE` in Railway variables
2. Or disable entirely: `ENABLE_RATE_LIMIT=false` (not recommended)

### Issue: API Key Not Working

**Symptoms**: 401 Unauthorized errors

**Solution**:
1. Verify `VITE_API_KEY` in Vercel matches `API_KEYS` in Railway
2. Check `REQUIRE_AUTH=true` in Railway
3. Regenerate keys if compromised

---

## Cost Estimates

### Railway (Free Tier)
- **Free**: $5 one-time credit
- **After credit**: ~$5-10/month depending on usage
- Includes: Backend container + PostgreSQL database

### Vercel (Hobby Plan)
- **Free**: Personal projects
- **Pro**: $20/month (if needed for commercial use)
- Includes: Frontend hosting + CDN + SSL certificates

**Total Estimated Cost**: $0-10/month after free credits

---

## Security Checklist

Before going live, ensure you've:

- [ ] Generated strong API keys (32+ characters)
- [ ] Set `REQUIRE_AUTH=true` in Railway
- [ ] Configured `CORS_ORIGINS` to your Vercel domain only
- [ ] Enabled rate limiting (`ENABLE_RATE_LIMIT=true`)
- [ ] Set up HTTPS (automatic on both platforms)
- [ ] Added custom domain (optional but recommended)
- [ ] Tested authentication is working
- [ ] Verified rate limiting is active
- [ ] Checked logs are being captured
- [ ] Set up monitoring/alerts (Railway does this automatically)

---

## Scaling Considerations

Your setup can handle:

### Current Setup (Free Tier)
- **Concurrent Users**: 10-50
- **Requests/Day**: ~1,000-5,000
- **Database Size**: Up to 1GB

### When to Upgrade

Upgrade Railway plan when:
- Database exceeds 1GB
- Need more than 5 concurrent connections
- CPU/Memory usage is consistently high

Upgrade Vercel plan when:
- Need production analytics
- Want team collaboration features
- Deploying for commercial use

---

## Updates & Maintenance

### Deploying Updates

**Backend (Railway):**
1. Push changes to GitHub `main` branch
2. Railway auto-deploys within 1-2 minutes
3. Zero-downtime deployment

**Frontend (Vercel):**
1. Push changes to GitHub
2. Vercel auto-deploys
3. Preview URLs for every PR

### Database Migrations

When changing database schema:
1. Use Alembic for migrations
2. Run migrations via Railway console or deploy script
3. Always test on staging first

---

## Backup Strategy

Railway provides:
- **Automated daily backups** (Pro plan)
- **Point-in-time recovery** (Pro plan)
- **Manual exports**: Use `pg_dump` via Railway console

For free tier:
- Export data regularly via Railway console
- Save to GitHub or external storage

---

## Support Resources

### Railway Documentation
- [Railway Docs](https://docs.railway.app)
- [Python Guide](https://docs.railway.app/deploy/python)
- [PostgreSQL Guide](https://docs.railway.app/deploy/postgresql)

### Vercel Documentation
- [Vercel Docs](https://vercel.com/docs)
- [Vite Guide](https://vercel.com/docs/frameworks/vite)
- [Environment Variables](https://vercel.com/docs/projects/environment-variables)

### Your Project
- Backend `SECURITY.md` - Security configuration guide
- Backend `.env.example` - Environment variable reference
- Frontend `.env.example` - Frontend configuration

---

## Next Steps

1. **Deploy to Railway** (Part 1)
2. **Deploy to Vercel** (Part 2)
3. **Test end-to-end** (Part 5)
4. **Set up custom domain** (Part 6 - optional)
5. **Monitor for 24 hours** before promoting to users
6. **Gather feedback** and iterate

---

## Quick Reference URLs

After deployment, save these URLs:

- **Frontend**: `https://your-site.vercel.app`
- **Backend API**: `https://your-api.railway.app`
- **API Docs**: `https://your-api.railway.app/docs`
- **Health Check**: `https://your-api.railway.app/health`
- **Railway Dashboard**: `https://railway.app/project/xxx`
- **Vercel Dashboard**: `https://vercel.com/username/project`
