# Quick Start Deployment - 10 Minutes to Production

A streamlined guide to get your Trading Probabilities app deployed fast.

## Pre-Deployment Checklist

- [ ] GitHub repository is public or Railway has access
- [ ] You have a Railway account (free)
- [ ] You have a Vercel account (free)

---

## 🚀 Step 1: Deploy Backend to Railway (5 minutes)

### 1.1 Create Railway Project
1. Go to https://railway.app/new
2. Click **"Deploy from GitHub repo"**
3. Select `trading-probabilities`
4. Click **"Deploy Now"**

### 1.2 Add PostgreSQL
1. In Railway project, click **"New Service"**
2. Select **Database** → **PostgreSQL**

### 1.3 Configure Backend
1. Click your backend service (not the database)
2. Go to **Settings** tab
3. Set **Root Directory**: `backend`
4. Go to **Variables** tab and add:

```bash
REQUIRE_AUTH=true
API_KEYS=prod-key-abc123xyz789 (generate your own)
ENABLE_RATE_LIMIT=true
RATE_LIMIT_PER_MINUTE=10
CORS_ORIGINS=https://your-site.vercel.app (we'll update this later)
```

### 1.4 Get Backend URL
After deployment:
- Copy the domain (e.g., `upbeat-name.railway.app`)
- Your API URL: `https://upbeat-name.railway.app`

✅ **Backend deployed!** Test it: `curl https://upbeat-name.railway.app/health`

---

## 🎨 Step 2: Deploy Frontend to Vercel (5 minutes)

### 2.1 Create Vercel Project
1. Go to https://vercel.com/new
2. Import `trading-probabilities` from GitHub
3. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Click Deploy**

### 2.2 Add Environment Variables
After first deploy:
1. Go to **Settings** → **Environment Variables**
2. Add:
   ```bash
   VITE_API_URL=https://upbeat-name.railway.app
   VITE_API_KEY=prod-key-abc123xyz789 (same as backend)
   ```
3. **Redeploy** (Vercel will prompt)

### 2.3 Get Frontend URL
Vercel will give you:
- `https://trading-probabilities-xyz.vercel.app`

✅ **Frontend deployed!** Open the URL and test querying a stock.

---

## 🔗 Step 3: Connect Frontend to Backend (1 minute)

### Update CORS in Railway

1. Go back to Railway → Backend service → **Variables**
2. Update `CORS_ORIGINS`:
   ```bash
   CORS_ORIGINS=https://trading-probabilities-xyz.vercel.app
   ```
3. Railway auto-redeploys

✅ **Done!** Your app is now live and connected.

---

## ✅ Step 4: Test Everything (2 minutes)

### Test 1: Health Check
```bash
curl https://upbeat-name.railway.app/health
# Should return: {"status":"healthy"}
```

### Test 2: API Query
```bash
curl -X POST https://upbeat-name.railway.app/api/query \
  -H "X-API-Key: prod-key-abc123xyz789" \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","condition_type":"percentage_change","threshold":2.0,"operator":"gte","time_horizons":["1d"]}'
```

### Test 3: Frontend UI
1. Open your Vercel URL
2. Search for "AAPL"
3. Submit a query
4. Should see results

---

## 🎉 You're Live!

Your app is now:
- ✅ Hosted on Railway (backend) + Vercel (frontend)
- ✅ Using PostgreSQL database
- � Protected with API authentication
- ✅ Rate limited (10 req/min)
- ✅ Serving over HTTPS
- ✅ Auto-deploying on git push

---

## 📝 Save These URLs

**Backend:**
- API: `https://upbeat-name.railway.app`
- Docs: `https://upbeat-name.railway.app/docs`
- Health: `https://upbeat-name.railway.app/health`

**Frontend:**
- App: `https://trading-probabilities-xyz.vercel.app`

**Admin:**
- Railway: https://railway.app/project/xxx
- Vercel: https://vercel.com/username/project

---

## 🔐 Security Reminders

- Keep your `API_KEYS` secret and secure
- Don't commit keys to GitHub
- Rotate keys periodically
- Monitor logs for suspicious activity

---

## 💰 Cost

- **Free tier**: $0 (with credits)
- **After credits**: ~$5-10/month
- Scale as needed

---

## Need Help?

- Full guide: See [DEPLOYMENT.md](./DEPLOYMENT.md)
- Railway docs: https://docs.railway.app
- Vercel docs: https://vercel.com/docs
- Security: See [backend/SECURITY.md](./backend/SECURITY.md)
