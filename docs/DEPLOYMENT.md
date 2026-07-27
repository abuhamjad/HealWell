# HealWell Deployment Guide - v1.0.0

Complete deployment instructions for HealWell v1.0.0 across development, staging, and production environments.

## Table of Contents

1. [Overview](#overview)
2. [Local Development](#local-development)
3. [LAN Testing](#lan-testing)
4. [Staging Deployment](#staging-deployment)
5. [Production Deployment](#production-deployment)
6. [Verification Checklist](#verification-checklist)
7. [Troubleshooting](#troubleshooting)

---

## Overview

HealWell v1.0.0 is a stateless health analysis platform:
- No database required
- No user authentication
- Single REST API endpoint
- LangGraph + OpenAI workflow
- Infinite horizontal scalability

### Deployment Architecture

```
Frontend (Vercel)
    ↓
API Gateway (CORS)
    ↓
Backend (Render/Railway)
    ↓
OpenAI API
    ↓
LangGraph Workflow
    ↓
Analysis Result
```

### Environment Support

| Environment | Purpose | Debug | CORS | LLM |
|-----------|---------|-------|------|-----|
| **development** | Local development | Enabled | Permissive | Optional |
| **staging** | Pre-production testing | Enabled | Configured | Required |
| **production** | Live deployment | Disabled | Strict | Required |

---

## Local Development

### Prerequisites

- Node.js 20+ (with npm)
- Python 3.11+
- OpenAI API key (optional for testing)
- Git

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env from example
cp .env.example .env
```

**Edit backend/.env:**

```env
ENVIRONMENT=development
DEBUG=True
API_TITLE=HealWell API
API_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000

FRONTEND_URL=http://localhost:5173
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

API_PREFIX=/api/v1
API_HEALTH_CHECK_PATH=/health

LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-...your-key-or-leave-empty-for-testing...
LLM_MODEL=gpt-4
LLM_TIMEOUT=30

LOG_LEVEL=DEBUG
LOG_FORMAT=text
```

**Start backend:**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs on: `http://localhost:8000`

API docs: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local
cat > .env.local << EOF
VITE_API_BASE_URL=http://localhost:8000
VITE_ENVIRONMENT=development
EOF

# Start dev server
npm run dev
```

Frontend runs on: `http://localhost:5173`

### Testing Local Development

```bash
# Test homepage
curl http://localhost:5173

# Test API health
curl http://localhost:8000/health

# Test analysis endpoint
curl -X POST http://localhost:8000/api/v1/analysis \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "I have a headache and fever"}'

# Test CORS preflight
curl -X OPTIONS http://localhost:8000/api/v1/analysis \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

---

## LAN Testing

Testing the application on devices within your local network:

### 1. Find Your LAN IP

```bash
# Windows
ipconfig

# Linux/macOS
ifconfig
```

Look for your local IP (e.g., 192.168.1.10)

### 2. Update Backend Configuration

Edit **backend/.env:**

```env
FRONTEND_URL=http://192.168.1.10:5173
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://192.168.1.10:5173
```

### 3. Start Services

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 4. Access from LAN Device

From any device on your network:

```
http://192.168.1.10:5173
```

### Verify LAN Connectivity

```bash
# Test backend health
curl http://192.168.1.10:8000/health

# Test CORS
curl -X OPTIONS http://192.168.1.10:8000/api/v1/analysis \
  -H "Origin: http://192.168.1.10:5173" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

---

## Staging Deployment

### Prerequisites

- Render account (https://render.com)
- GitHub repository connected
- OpenAI API key

### 1. Create Backend Service on Render

1. Go to Render Dashboard
2. Create new Web Service
3. Connect your GitHub repository

**Configuration:**

```
Environment: Python 3.11
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port 8000
Root Directory: ./backend
Health Check: /health
```

**Environment Variables:**

```env
ENVIRONMENT=staging
DEBUG=True
FRONTEND_STAGING_URL=https://healwell-staging.vercel.app
CORS_ORIGINS=https://healwell-staging.vercel.app,http://localhost:5173

LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-...your-staging-key...
LLM_MODEL=gpt-4
LLM_TIMEOUT=30

LOG_LEVEL=INFO
LOG_FORMAT=json
```

### 2. Deploy Frontend Preview on Vercel

```bash
vercel deploy --prod
```

Or enable automatic deployments from GitHub.

**Environment Variables (Vercel Settings → Environment Variables):**

For Preview environment:
```
VITE_API_BASE_URL=https://healwell-staging.onrender.com
VITE_ENVIRONMENT=staging
```

### 3. Update Backend CORS

Once Render service is running, update environment:

```env
CORS_ORIGINS=https://healwell-staging.vercel.app
```

### 4. Test Staging Deployment

```bash
# Test health check
curl https://healwell-staging.onrender.com/health

# Test CORS
curl -X OPTIONS https://healwell-staging.onrender.com/api/v1/analysis \
  -H "Origin: https://healwell-staging.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Test analysis
curl -X POST https://healwell-staging.onrender.com/api/v1/analysis \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "I have a headache"}'
```

---

## Production Deployment

### Prerequisites

- Render account (or Railway, Heroku, etc.)
- Vercel production domain
- OpenAI API key (production)
- Custom domain (optional)

### 1. Create Production Backend Service

**On Render Dashboard:**

1. Create new Web Service
2. Connect GitHub repository
3. Select `main` branch for production

**Configuration:**

```
Environment: Python 3.11
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port 8000
Root Directory: ./backend
Health Check: /health
Region: Choose closest to users
```

**Environment Variables:**

```env
ENVIRONMENT=production
DEBUG=False
FRONTEND_PRODUCTION_URL=https://healwell.vercel.app
CORS_ORIGINS=https://healwell.vercel.app

LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-...your-production-key...
LLM_MODEL=gpt-4
LLM_TIMEOUT=30

LOG_LEVEL=WARNING
LOG_FORMAT=json
```

### 2. Deploy Frontend to Vercel Production

```bash
vercel deploy --prod --token $VERCEL_TOKEN
```

Or push to `main` branch for automatic deployment.

**Environment Variables (Vercel Production):**

```
VITE_API_BASE_URL=https://healwell-api.onrender.com
VITE_ENVIRONMENT=production
```

### 3. Update Backend CORS

Once Render backend is running, update:

```env
CORS_ORIGINS=https://healwell.vercel.app
```

### 4. Verify Production Deployment

```bash
# Test health
curl https://healwell-api.onrender.com/health

# Test CORS
curl -X OPTIONS https://healwell-api.onrender.com/api/v1/analysis \
  -H "Origin: https://healwell.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Test analysis
curl -X POST https://healwell-api.onrender.com/api/v1/analysis \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "I have a headache and fever"}'

# Check logs
# Render Dashboard → Logs tab
```

### 5. Custom Domain (Optional)

1. Register domain (e.g., healwell.com)
2. On Render: Settings → Custom Domain
3. Follow DNS configuration instructions
4. Update Vercel CORS_ORIGINS if needed

---

## Frontend Deployment (Vercel)

### Quick Start

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from frontend directory
cd frontend
vercel --prod
```

### Configuration

Vercel auto-detects Vite projects.

**Build Settings:**
- Framework: Vite
- Build Command: `npm run build`
- Output Directory: `dist`
- Root Directory: `./frontend`

### Environment Variables

**Development:**
```
VITE_API_BASE_URL=http://localhost:8000
VITE_ENVIRONMENT=development
```

**Preview (Staging):**
```
VITE_API_BASE_URL=https://healwell-staging.onrender.com
VITE_ENVIRONMENT=staging
```

**Production:**
```
VITE_API_BASE_URL=https://healwell-api.onrender.com
VITE_ENVIRONMENT=production
```

### Preview Deployments

Every push to non-main branches creates a preview URL:
```
https://healwell-pr-123.vercel.app
```

Update Render staging CORS if testing:
```env
CORS_ORIGINS=https://healwell-pr-123.vercel.app
```

---

## Verification Checklist

### Local Development

- [ ] Backend starts: `uvicorn app.main:app --reload`
- [ ] Frontend starts: `npm run dev`
- [ ] Homepage loads: http://localhost:5173
- [ ] Analysis page loads
- [ ] Submit analysis works
- [ ] Results display correctly
- [ ] No console errors
- [ ] No backend exceptions
- [ ] CORS preflight succeeds

### LAN Testing

- [ ] CORS_ORIGINS includes LAN IP
- [ ] Backend accessible: `http://192.168.1.X:8000`
- [ ] Frontend accessible: `http://192.168.1.X:5173`
- [ ] CORS OPTIONS succeeds
- [ ] Analysis works from LAN device
- [ ] No origin errors

### Staging Deployment

- [ ] Render service created
- [ ] Vercel preview deployed
- [ ] ENVIRONMENT=staging
- [ ] CORS_ORIGINS includes Vercel URL
- [ ] Health endpoint returns 200
- [ ] CORS preflight succeeds
- [ ] Analysis endpoint works
- [ ] No CORS errors in console

### Production Deployment

- [ ] ENVIRONMENT=production
- [ ] DEBUG=False
- [ ] CORS_ORIGINS only includes production domains
- [ ] LLM_API_KEY configured
- [ ] Frontend deployed to Vercel
- [ ] Health check passes
- [ ] CORS restricted correctly
- [ ] No console errors
- [ ] Logs monitored
- [ ] Uptime tracked

---

## Troubleshooting

### CORS Errors

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
```bash
# Check CORS configuration
curl -X OPTIONS http://localhost:8000/api/v1/analysis \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Verify frontend domain in CORS_ORIGINS
# Check exact match (no trailing slashes)
```

### Backend Won't Start

**Error:** `Pydantic ValidationError: Extra inputs are not permitted`

**Solution:**
1. Check `.env` for unknown variables
2. Remove any extra lines
3. Verify format: `VARIABLE=value` (no spaces)

### Frontend API Calls Fail

**Error:** `Failed to create analysis`

**Solution:**
1. Check `VITE_API_BASE_URL` matches backend URL
2. Verify backend is running
3. Check browser Network tab
4. Verify CORS is configured

### LLM API Errors

**Error:** `401 Unauthorized`

**Solution:**
1. Verify `LLM_API_KEY` is set
2. Check key hasn't expired
3. Verify at https://platform.openai.com/account/api-keys
4. Try test request with curl

### Analysis Takes Too Long

**Error:** `Request timeout after 30 seconds`

**Solution:**
1. Increase `LLM_TIMEOUT` if needed
2. Check OpenAI API status
3. Monitor backend logs
4. Consider rate limiting

### Render Service Crashes

**Solution:**
1. Check Render logs for errors
2. Verify environment variables
3. Ensure `LLM_API_KEY` is set
4. Check Python version compatibility
5. Review memory usage

---

## Performance Optimization

### Frontend

```bash
# Optimize build
npm run build

# Check bundle size
npm run build -- --analyze
```

### Backend

- Enable Gunicorn workers for production
- Use async execution
- Implement caching if needed
- Monitor memory usage

### Monitoring

- Set up error tracking (Sentry)
- Monitor API latency
- Track LLM API costs
- Log analysis patterns

---

## Security Checklist

- [ ] `DEBUG=False` in production
- [ ] `ENVIRONMENT=production` set
- [ ] API keys in environment variables (not in git)
- [ ] CORS restricts to frontend domain only
- [ ] HTTPS enforced
- [ ] No sensitive data in logs
- [ ] Regular dependency updates
- [ ] Input validation enabled

---

## Support

For deployment issues:
- Check Render/Vercel logs
- Review configuration in `.env`
- Test endpoints with curl
- Check browser DevTools Network tab
- Consult documentation at [docs/](../docs/)

---

**HealWell v1.0.0 is production-ready. Deploy with confidence.**
