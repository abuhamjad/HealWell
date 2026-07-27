# HealWell Deployment Guide

Complete deployment instructions for local development, staging, and production environments.

---

## Table of Contents

1. [Environment Configuration](#environment-configuration)
2. [Local Development](#local-development)
3. [LAN Testing](#lan-testing)
4. [Staging Deployment (Render)](#staging-deployment-render)
5. [Production Deployment (Render)](#production-deployment-render)
6. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
7. [Verification Checklist](#verification-checklist)
8. [Troubleshooting](#troubleshooting)

---

## Environment Configuration

### Three Deployment Environments

HealWell supports three environments:

| Environment | Purpose | Debug | CORS | Database |
|------------|---------|-------|------|----------|
| **development** | Local development | Enabled | Permissive (localhost, LAN) | Optional (mock) |
| **staging** | Pre-production testing | Enabled | Configured domains | PostgreSQL |
| **production** | Live deployment | Disabled | Strict (frontend only) | PostgreSQL |

### Configuration Hierarchy

Settings are loaded in this order:
1. Environment variables (highest priority)
2. `.env` file
3. Default values in `Settings` class (lowest priority)

### Key Configuration Variables

```
ENVIRONMENT         # development | staging | production
DEBUG               # True | False
FRONTEND_URL        # Development frontend URL
FRONTEND_STAGING_URL    # Staging frontend URL
FRONTEND_PRODUCTION_URL # Production frontend URL (Vercel)
CORS_ORIGINS        # Comma-separated allowed origins
GEMINI_API_KEY      # For v0.7+ (leave empty if not used)
DATABASE_URL        # For v0.9+ (leave empty if not used)
```

---

## Local Development

### Prerequisites

- Node.js 24+ (with npm)
- Python 3.10+
- Virtual environment (`.venv`)
- Git

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment (if needed)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env from example
cp .env.example .env

# Verify .env has:
# ENVIRONMENT=development
# DEBUG=True
# FRONTEND_URL=http://localhost:5173
# CORS_ORIGINS includes localhost and 127.0.0.1

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend starts on: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env (optional - defaults work for local dev)
cp .env.example .env

# Verify .env has:
# VITE_API_BASE_URL=http://127.0.0.1:8000
# VITE_ENVIRONMENT=development
# VITE_DEBUG=true

# Start development server
npm run dev
```

Frontend starts on: `http://localhost:5173`

### Testing Local Development

```bash
# Test homepage
curl http://localhost:5173

# Test API
curl http://localhost:8000/health

# Test analysis endpoint
curl -X POST http://localhost:8000/api/v1/analysis \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "fever and cough"}'

# Test CORS preflight
curl -X OPTIONS http://localhost:8000/api/v1/analysis \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

---

## LAN Testing

### Access Frontend from LAN

To test the application on devices within your local network:

### 1. Update CORS Configuration

Add your LAN IP to `CORS_ORIGINS` in `backend/.env`:

```
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://192.168.1.X:5173
```

Replace `192.168.1.X` with your machine's actual LAN IP.

### 2. Update Frontend URL

In `backend/.env`, set:

```
FRONTEND_URL=http://192.168.1.X:5173
```

### 3. Start Backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Start Frontend

Frontend will automatically bind to all interfaces on port 5173.

```bash
cd frontend
npm run dev
```

### 5. Access from LAN Device

From any device on your network, open:

```
http://192.168.1.X:5173
```

### Verify LAN Connectivity

```bash
# From LAN device, test API
curl http://192.168.1.X:8000/health

# Test CORS
curl -X OPTIONS http://192.168.1.X:8000/api/v1/analysis \
  -H "Origin: http://192.168.1.X:5173" \
  -v
```

---

## Staging Deployment (Render)

### Prerequisites

- Render account (https://render.com)
- Git repository with code
- Environment variables prepared

### 1. Create Backend Service on Render

```bash
# Login to Render dashboard
# Create new Web Service
# Connect your GitHub repository

# Configuration:
# Environment: Python 3.10
# Build Command: pip install -r requirements.txt
# Start Command: uvicorn app.main:app --host 0.0.0.0 --port 8000

# Environment Variables:
ENVIRONMENT=staging
DEBUG=True
FRONTEND_STAGING_URL=https://your-preview-url.vercel.app
CORS_ORIGINS=https://your-preview-url.vercel.app,http://localhost:5173
GEMINI_API_KEY=<your-key-if-ready>
```

### 2. Deploy Frontend Preview on Vercel

```bash
# Vercel handles automatic preview deployments from pull requests
# Each PR gets a preview URL like: https://healwell-pr-123.vercel.app

# Update Render environment:
FRONTEND_STAGING_URL=https://healwell-pr-123.vercel.app
CORS_ORIGINS=https://healwell-pr-123.vercel.app
```

### 3. Update Backend CORS

Render will provide a backend URL like:
```
https://healwell-staging.onrender.com
```

Update frontend `.env`:
```
VITE_API_BASE_URL=https://healwell-staging.onrender.com
```

### 4. Test Staging Deployment

```bash
# Test health check
curl https://healwell-staging.onrender.com/health

# Test CORS from Vercel preview
curl -X OPTIONS https://healwell-staging.onrender.com/api/v1/analysis \
  -H "Origin: https://healwell-pr-123.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Test analysis endpoint
curl -X POST https://healwell-staging.onrender.com/api/v1/analysis \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "test"}'
```

---

## Production Deployment (Render)

### Prerequisites

- Production-ready database (PostgreSQL on Render)
- Vercel production deployment
- Gemini API key (for v0.7+)
- Domain or use Render's subdomain

### 1. Create Production Backend Service

```bash
# On Render Dashboard: Create Production Web Service

# Configuration:
# Environment: Python 3.10
# Build Command: pip install -r requirements.txt
# Start Command: uvicorn app.main:app --host 0.0.0.0 --port 8000
# Health Check: /health

# Critical Environment Variables:
ENVIRONMENT=production
DEBUG=False
FRONTEND_PRODUCTION_URL=https://healwell.vercel.app
CORS_ORIGINS=https://healwell.vercel.app
GEMINI_API_KEY=<your-gemini-key>
DATABASE_URL=postgresql://user:password@db.render.com:5432/healwell
LOG_LEVEL=INFO
AI_TEMPERATURE=0.7
```

### 2. Create Production Database

On Render Dashboard:
- Create PostgreSQL database
- Secure with strong password
- Use private connection
- Enable automated backups
- Copy `DATABASE_URL` to backend environment

### 3. Deploy Frontend to Vercel Production

```bash
# Vercel automatically deploys main branch
# Production domain: https://healwell.vercel.app

# Ensure .env.production in frontend:
VITE_API_BASE_URL=https://healwell-api.onrender.com
VITE_ENVIRONMENT=production
VITE_DEBUG=false
```

### 4. Update Backend CORS

Once Render service is running:

```bash
# Backend URL: https://healwell-api.onrender.com

# Update CORS_ORIGINS to:
CORS_ORIGINS=https://healwell.vercel.app
```

### 5. Production Database Setup

If using v0.9+ with database:

```bash
# After DATABASE_URL is set, run migrations:
cd backend
alembic upgrade head  # (when available)
```

### 6. Verify Production Deployment

```bash
# Test health
curl https://healwell-api.onrender.com/health

# Test CORS
curl -X OPTIONS https://healwell-api.onrender.com/api/v1/analysis \
  -H "Origin: https://healwell.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Test API
curl -X POST https://healwell-api.onrender.com/api/v1/analysis \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "test"}'

# Monitor logs
# Render Dashboard → Logs tab
```

---

## Frontend Deployment (Vercel)

### Prerequisites

- Vercel account (https://vercel.com)
- GitHub repository connected

### 1. Deploy to Vercel

```bash
# Vercel auto-detects Next.js/Vite projects
# Connect GitHub repo to Vercel

# Configuration:
# Framework: Vite
# Build Command: npm run build
# Output Directory: dist
# Root Directory: ./frontend
```

### 2. Environment Variables

On Vercel Dashboard → Project Settings → Environment Variables:

```
# Development
VITE_API_BASE_URL=http://localhost:8000
VITE_ENVIRONMENT=development
VITE_DEBUG=true

# Preview (staging)
VITE_API_BASE_URL=https://healwell-staging.onrender.com
VITE_ENVIRONMENT=staging
VITE_DEBUG=true

# Production
VITE_API_BASE_URL=https://healwell-api.onrender.com
VITE_ENVIRONMENT=production
VITE_DEBUG=false
```

### 3. Custom Domain (Optional)

1. Register domain (e.g., healwell.com)
2. Add to Vercel: Settings → Domains
3. Follow Vercel's DNS configuration

### 4. Preview Deployments

Every pull request automatically creates a preview URL:
```
https://healwell-pr-123.vercel.app
```

Update Render staging backend:
```
CORS_ORIGINS=https://healwell-pr-123.vercel.app
```

---

## Verification Checklist

### Local Development Checklist

- [ ] Backend starts: `uvicorn app.main:app --reload`
- [ ] Frontend starts: `npm run dev`
- [ ] Homepage loads at http://localhost:5173
- [ ] Analyze page loads
- [ ] LangGraph workflow executes
- [ ] Analysis results display
- [ ] Browser console has no errors
- [ ] Backend logs show no exceptions
- [ ] CORS preflight succeeds

### LAN Testing Checklist

- [ ] Update CORS_ORIGINS with LAN IP
- [ ] Update FRONTEND_URL with LAN IP
- [ ] Backend accessible from LAN: `http://192.168.1.X:8000`
- [ ] Frontend accessible from LAN: `http://192.168.1.X:5173`
- [ ] CORS OPTIONS request succeeds
- [ ] Analysis workflow works from LAN device
- [ ] No origin errors in browser console

### Staging Deployment Checklist

- [ ] Render backend service created
- [ ] Vercel preview deployment created
- [ ] ENVIRONMENT=staging in backend
- [ ] CORS_ORIGINS includes Vercel preview URL
- [ ] FRONTEND_STAGING_URL set correctly
- [ ] Health check endpoint returns 200
- [ ] CORS preflight succeeds
- [ ] Analysis endpoint works
- [ ] No CORS errors in browser

### Production Deployment Checklist

- [ ] ENVIRONMENT=production in backend
- [ ] DEBUG=False in backend
- [ ] CORS_ORIGINS only includes production domains
- [ ] DATABASE_URL configured (if v0.9+)
- [ ] GEMINI_API_KEY configured (if v0.7+)
- [ ] Frontend deployed to Vercel production
- [ ] Custom domain configured (optional)
- [ ] Health check passes
- [ ] CORS restricted to production origin only
- [ ] No console errors in production
- [ ] Monitoring/logging configured
- [ ] Backup strategy in place

---

## Troubleshooting

### CORS Errors

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
1. Check browser Origin header matches CORS_ORIGINS
2. Verify OPTIONS preflight returns correct headers
3. In development, check CORS_ORIGINS includes both localhost and 127.0.0.1
4. In production, ensure only production domains are allowed

```bash
# Test CORS
curl -X OPTIONS http://localhost:8000/api/v1/analysis \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

### Backend Won't Start

**Error:** `Pydantic ValidationError: Extra inputs are not permitted`

**Solution:**
1. Ensure all required environment variables are set
2. Remove unknown variables from .env
3. Check .env format (VARIABLE=value, no spaces)

### Frontend API Calls Fail

**Error:** `Failed to create analysis`

**Solution:**
1. Check VITE_API_BASE_URL in frontend .env
2. Verify backend is running on that URL
3. Check browser network tab for actual request URL
4. Ensure CORS is properly configured

### LAN Connectivity Issues

**Problem:** Can't access backend from LAN device

**Solution:**
1. Check LAN IP: `ipconfig` (Windows) or `ifconfig` (Linux)
2. Ensure backend running with `--host 0.0.0.0`
3. Verify firewall allows connections
4. Check CORS_ORIGINS includes LAN IP
5. Test with: `curl http://192.168.1.X:8000/health`

### Production Database Connection Fails

**Error:** `could not connect to server`

**Solution:**
1. Verify DATABASE_URL format (if using v0.9+)
2. Check database credentials
3. Ensure database is accessible from Render
4. Check Render networking/firewall settings
5. Test connection locally before deploying

---

## Next Steps (v0.7+)

When implementing Gemini integration:

1. Set `GEMINI_API_KEY` in production
2. Update `GEMINI_MODEL` if needed
3. Adjust `AI_TEMPERATURE` for response style
4. Set `AI_TIMEOUT` based on expected latency
5. Monitor Gemini API usage and costs

When implementing database (v0.9+):

1. Create PostgreSQL database
2. Set `DATABASE_URL`
3. Run migrations
4. Test data persistence
5. Implement backup strategy

---

## Support

For deployment issues:
- Check logs: Render Dashboard → Logs
- Review configuration: `backend/.env`
- Test endpoints: Use curl commands above
- Check CORS: Use browser DevTools → Network tab
