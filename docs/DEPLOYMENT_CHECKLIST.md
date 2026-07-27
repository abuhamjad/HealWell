# Deployment Checklist

Step-by-step verification checklist for deploying HealWell across all environments.

---

## Local Development Setup

### Prerequisites
- [ ] Node.js 24+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Python 3.10+ installed (`python --version`)
- [ ] Git installed and configured
- [ ] Project cloned locally

### Backend Setup

- [ ] Navigate to `backend/` directory
- [ ] Create virtual environment: `python -m venv .venv`
- [ ] Activate venv: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env`: `cp .env.example .env`
- [ ] Verify `.env` contains:
  - `ENVIRONMENT=development`
  - `DEBUG=True`
  - `FRONTEND_URL=http://localhost:5173`
  - `CORS_ORIGINS=...includes localhost...`

### Frontend Setup

- [ ] Navigate to `frontend/` directory
- [ ] Install dependencies: `npm install`
- [ ] Verify `.env.example` exists with VITE_API_BASE_URL
- [ ] Optional: Create `.env` with:
  - `VITE_API_BASE_URL=http://127.0.0.1:8000`
  - `VITE_ENVIRONMENT=development`
  - `VITE_DEBUG=true`

### Local Verification

- [ ] Start backend: `uvicorn app.main:app --reload`
  - [ ] Backend starts successfully
  - [ ] No errors in console
  - [ ] Swagger UI accessible: http://localhost:8000/docs

- [ ] Start frontend: `npm run dev`
  - [ ] Frontend compiles successfully
  - [ ] Dev server running on port 5173
  - [ ] No build errors

- [ ] Open http://localhost:5173 in browser
  - [ ] Homepage loads
  - [ ] No console errors
  - [ ] Navbar renders correctly
  - [ ] Analyze page is accessible

- [ ] Test analysis workflow
  - [ ] Enter symptoms and submit
  - [ ] LangGraph executes without errors
  - [ ] Analysis results display
  - [ ] Risk badge shows
  - [ ] Specialist recommendation displays
  - [ ] Health report shows

- [ ] Check backend logs
  - [ ] POST /api/v1/analysis returns 200
  - [ ] LangGraph agents execute (symptom → risk → specialist → report)
  - [ ] Mock data returned correctly

- [ ] Test CORS
  ```bash
  curl -X OPTIONS http://localhost:8000/api/v1/analysis \
    -H "Origin: http://localhost:5173" \
    -H "Access-Control-Request-Method: POST" \
    -v
  ```
  - [ ] Response includes `access-control-allow-origin`
  - [ ] Status 200

---

## LAN Testing

### Setup

- [ ] Note your machine's LAN IP: `ipconfig` (Windows) or `ifconfig` (Linux)
- [ ] Update `backend/.env`:
  - `CORS_ORIGINS=...add your-lan-ip:5173...`
  - `FRONTEND_URL=http://your-lan-ip:5173`

- [ ] Restart backend with: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

### LAN Device Access

- [ ] Access frontend from LAN device: `http://192.168.1.X:5173`
- [ ] Homepage loads on LAN device
- [ ] Test analysis workflow on LAN device
  - [ ] Submit symptoms
  - [ ] Results display
  - [ ] No CORS errors

- [ ] Test from different LAN device if possible

### CORS Verification

- [ ] From LAN device, test CORS:
  ```bash
  curl -X OPTIONS http://192.168.1.X:8000/api/v1/analysis \
    -H "Origin: http://192.168.1.X:5173" \
    -v
  ```
  - [ ] Includes `access-control-allow-origin` header
  - [ ] Status 200

---

## Staging Deployment (Render + Vercel)

### Create Render Backend Service

- [ ] Login to Render.com
- [ ] Create new Web Service
- [ ] Connect GitHub repository
- [ ] Configure:
  - [ ] Environment: Python 3.10
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
  - [ ] Root Directory: `./backend` (if monorepo)

- [ ] Add Environment Variables:
  - `ENVIRONMENT=staging`
  - `DEBUG=True`
  - `FRONTEND_STAGING_URL=https://healwell-pr-xxx.vercel.app` (update with actual URL)
  - `CORS_ORIGINS=https://healwell-pr-xxx.vercel.app`
  - `API_PREFIX=/api/v1`
  - `LOG_LEVEL=INFO`

- [ ] Deploy service
- [ ] Wait for deployment to complete
- [ ] Note Render URL: `https://healwell-staging.onrender.com`

### Create Vercel Preview Deployment

- [ ] Push changes to GitHub branch (creates PR)
- [ ] Vercel automatically creates preview deployment
- [ ] Note preview URL: `https://healwell-pr-xxx.vercel.app`

### Connect Render and Vercel

- [ ] Update Render environment variables with correct Vercel preview URL
- [ ] Restart Render backend service

### Staging Verification

- [ ] Test health endpoint:
  ```bash
  curl https://healwell-staging.onrender.com/health
  ```
  - [ ] Returns 200
  - [ ] Includes environment info

- [ ] Test CORS preflight:
  ```bash
  curl -X OPTIONS https://healwell-staging.onrender.com/api/v1/analysis \
    -H "Origin: https://healwell-pr-xxx.vercel.app" \
    -H "Access-Control-Request-Method: POST" \
    -v
  ```
  - [ ] Includes CORS headers
  - [ ] Status 200

- [ ] Test analysis endpoint:
  ```bash
  curl -X POST https://healwell-staging.onrender.com/api/v1/analysis \
    -H "Content-Type: application/json" \
    -H "Origin: https://healwell-pr-xxx.vercel.app" \
    -d '{"symptoms": "test"}'
  ```
  - [ ] Returns 200
  - [ ] Returns valid analysis

- [ ] Access frontend from Vercel URL: `https://healwell-pr-xxx.vercel.app`
  - [ ] Homepage loads
  - [ ] No console CORS errors
  - [ ] Analyze page works
  - [ ] Analysis workflow completes

---

## Production Deployment (Render + Vercel)

### Production Database (Render)

- [ ] Create PostgreSQL database on Render
- [ ] Configure:
  - [ ] Region: Same as backend
  - [ ] PostgreSQL version: 14+
  - [ ] Enable backups
- [ ] Note connection string: `postgresql://...`
- [ ] Create strong password (32+ characters)

### Create Production Backend Service

- [ ] Create new Render Web Service
- [ ] Connect GitHub repository (main branch)
- [ ] Configure:
  - [ ] Environment: Python 3.10
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

- [ ] Add Environment Variables:
  - [ ] `ENVIRONMENT=production`
  - [ ] `DEBUG=False`
  - [ ] `FRONTEND_PRODUCTION_URL=https://healwell.vercel.app`
  - [ ] `CORS_ORIGINS=https://healwell.vercel.app`
  - [ ] `DATABASE_URL=postgresql://...` (if v0.9+)
  - [ ] `GEMINI_API_KEY=sk-...` (if v0.7+)
  - [ ] `LOG_LEVEL=WARNING`
  - [ ] `AI_TEMPERATURE=0.3` (more consistent)

- [ ] Deploy backend
- [ ] Wait for deployment
- [ ] Note Production URL: `https://healwell-api.onrender.com`

### Production Frontend (Vercel)

- [ ] Deploy main branch to Vercel production
- [ ] Configure environment variables:
  - [ ] `VITE_API_BASE_URL=https://healwell-api.onrender.com`
  - [ ] `VITE_ENVIRONMENT=production`
  - [ ] `VITE_DEBUG=false`

- [ ] Set up custom domain (if applicable)
- [ ] Enable auto-SSL
- [ ] Wait for production deployment

### Update Backend CORS

- [ ] Confirm Render backend is running at: `https://healwell-api.onrender.com`
- [ ] Update Render environment variable:
  - `CORS_ORIGINS=https://healwell.vercel.app`
  - Restart backend service

### Production Verification

- [ ] Test health endpoint:
  ```bash
  curl https://healwell-api.onrender.com/health
  ```
  - [ ] Returns 200
  - [ ] No debug info leaked

- [ ] Test CORS:
  ```bash
  curl -X OPTIONS https://healwell-api.onrender.com/api/v1/analysis \
    -H "Origin: https://healwell.vercel.app" \
    -v
  ```
  - [ ] Includes `access-control-allow-origin: https://healwell.vercel.app`
  - [ ] No wildcards in production

- [ ] Test from production frontend: `https://healwell.vercel.app`
  - [ ] Homepage loads
  - [ ] No console errors
  - [ ] Analyze workflow works
  - [ ] Results display

- [ ] Verify production-only settings:
  - [ ] DEBUG=False in backend
  - [ ] ENVIRONMENT=production
  - [ ] VITE_DEBUG=false in frontend
  - [ ] CORS does NOT include localhost
  - [ ] API keys stored in Render secrets (not .env)

- [ ] Test from different networks/browsers
- [ ] Monitor Render logs for errors
- [ ] Set up alerts/monitoring (optional)

---

## v0.7 Gemini Integration

### Prerequisites
- [ ] Google Gemini API key obtained from https://aistudio.google.com/apikey
- [ ] API key is valid and has quota

### Configuration

- [ ] Render production environment variable:
  - [ ] `GEMINI_API_KEY=sk-...your-key...`
- [ ] Restart backend service
- [ ] Verify backend starts without errors

### Testing

- [ ] Submit analysis from production frontend
- [ ] Verify response comes from Gemini (not mock data)
- [ ] Check response quality
- [ ] Monitor Gemini API usage/costs
- [ ] Set API usage alerts if needed

---

## v0.9 Database Integration

### Prerequisites
- [ ] PostgreSQL database created on Render
- [ ] Strong credentials set
- [ ] Database accessible from Render backend

### Configuration

- [ ] Set `DATABASE_URL` in production
- [ ] Restart backend
- [ ] Verify connection successful

### Database Setup

- [ ] Run migrations (when available): `alembic upgrade head`
- [ ] Verify database schema created
- [ ] Test data persistence

### Testing

- [ ] Create analysis (saves to database)
- [ ] Retrieve analysis history
- [ ] Verify data persisted correctly
- [ ] Test database backups

---

## Post-Deployment Tasks

### Monitoring

- [ ] Set up error tracking (e.g., Sentry)
- [ ] Configure Render logs retention
- [ ] Set up alerts for:
  - [ ] High error rates
  - [ ] API timeouts
  - [ ] Database connection issues

### Documentation

- [ ] Update deployment documentation with actual URLs
- [ ] Document any custom configurations
- [ ] Create runbook for common issues
- [ ] Document rollback procedures

### Backup & Recovery

- [ ] Verify database backups enabled
- [ ] Test backup restoration
- [ ] Document recovery procedures
- [ ] Set backup retention policies

### Security

- [ ] Enable HTTPS (automatic on Render/Vercel)
- [ ] Review security headers
- [ ] Verify no secrets in logs
- [ ] Set up CORS properly (no wildcards in prod)
- [ ] Enable rate limiting (future)

### Performance

- [ ] Monitor response times
- [ ] Check backend CPU/memory usage
- [ ] Monitor API latency
- [ ] Optimize slow endpoints

---

## Rollback Procedures

### If Backend Breaks

1. Check Render logs for errors
2. Review latest environment variable changes
3. Revert problematic environment variable
4. Restart backend service
5. Verify health endpoint works

### If Frontend Breaks

1. Check Vercel deployment logs
2. Revert to previous commit if needed
3. Verify environment variables are set correctly
4. Redeploy

### If Database Issues

1. Check database connection string
2. Verify database is running
3. Check database logs for issues
4. Restore from backup if necessary

---

## Success Criteria

- [ ] Both frontend and backend deployed
- [ ] All environment variables correctly configured
- [ ] CORS working for production domains only
- [ ] API responses working
- [ ] LangGraph workflow executing
- [ ] Mock AI data returned (v0.6)
- [ ] No console errors in production
- [ ] No sensitive data in logs
- [ ] Monitoring/alerts configured
- [ ] Backup strategy in place

---

## Support & Troubleshooting

See `DEPLOYMENT.md` for common issues and solutions:
- CORS errors
- Backend won't start
- API connection failures
- LAN connectivity issues
- Database problems
