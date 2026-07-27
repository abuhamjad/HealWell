# Deployment Checklist - v1.0.0

Step-by-step verification checklist for deploying HealWell v1.0.0 across all environments.

---

## Local Development Setup

### Prerequisites

- [ ] Node.js 20+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Python 3.11+ installed (`python --version`)
- [ ] Git installed and configured
- [ ] Project cloned locally
- [ ] OpenAI API key obtained (https://platform.openai.com/api-keys)

### Backend Setup

- [ ] Navigate to `backend/` directory
- [ ] Create virtual environment: `python -m venv .venv`
- [ ] Activate venv:
  - Windows: `.venv\Scripts\activate`
  - Linux/macOS: `source .venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env`: `cp .env.example .env`
- [ ] Configure `.env`:
  - [ ] `ENVIRONMENT=development`
  - [ ] `DEBUG=True`
  - [ ] `FRONTEND_URL=http://localhost:5173`
  - [ ] `CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173`
  - [ ] `LLM_API_KEY=sk-...your-openai-key...` (optional for testing)
  - [ ] `LLM_MODEL=gpt-4`

### Frontend Setup

- [ ] Navigate to `frontend/` directory
- [ ] Install dependencies: `npm install`
- [ ] Create `.env.local`:
  ```
  VITE_API_BASE_URL=http://localhost:8000
  VITE_ENVIRONMENT=development
  ```

### Local Verification

**Backend:**
- [ ] Start backend: `uvicorn app.main:app --reload`
  - [ ] Backend starts successfully
  - [ ] No errors in console
  - [ ] Swagger UI accessible: http://localhost:8000/docs
  - [ ] ReDoc accessible: http://localhost:8000/redoc

**Frontend:**
- [ ] Start frontend: `npm run dev`
  - [ ] Frontend compiles successfully
  - [ ] Dev server running on port 5173
  - [ ] No TypeScript errors
  - [ ] No build warnings

**API Testing:**
- [ ] Open http://localhost:5173 in browser
  - [ ] Homepage loads
  - [ ] No console errors
  - [ ] Navbar renders
  - [ ] Analysis page accessible

**Workflow Testing:**
- [ ] Test analysis submission
  - [ ] Enter symptoms: "I have a headache and fever"
  - [ ] Click Analyze
  - [ ] Results display within 10 seconds
  - [ ] Risk badge shows
  - [ ] Specialist recommendation displays
  - [ ] Health report shows
  - [ ] No error messages

**Health Endpoints:**
- [ ] `curl http://localhost:8000/` - Returns version info
- [ ] `curl http://localhost:8000/health` - Returns healthy status
- [ ] `curl -X POST http://localhost:8000/api/v1/analysis -H "Content-Type: application/json" -d '{"symptoms": "test"}'` - Returns analysis

**CORS Verification:**
```bash
curl -X OPTIONS http://localhost:8000/api/v1/analysis \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -v
```
- [ ] Response includes `access-control-allow-origin: http://localhost:5173`
- [ ] Status 200

---

## LAN Testing

### Setup

- [ ] Find LAN IP:
  - Windows: `ipconfig` (look for "IPv4 Address")
  - Linux/macOS: `ifconfig` (look for "inet addr")
  
- [ ] Update `backend/.env`:
  ```
  FRONTEND_URL=http://192.168.1.X:5173
  CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://192.168.1.X:5173
  ```

- [ ] Restart backend: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

### LAN Device Access

- [ ] Access frontend from LAN device: `http://192.168.1.X:5173`
  - [ ] Homepage loads
  - [ ] No CORS errors in console
  - [ ] Analyze page accessible

- [ ] Test analysis workflow on LAN device
  - [ ] Submit symptoms
  - [ ] Results display correctly
  - [ ] No errors in browser console

### CORS Testing on LAN

```bash
curl -X OPTIONS http://192.168.1.X:8000/api/v1/analysis \
  -H "Origin: http://192.168.1.X:5173" \
  -H "Access-Control-Request-Method: POST" \
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
  - [ ] Environment: Python 3.11
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
  - [ ] Root Directory: `./backend`

- [ ] Add Environment Variables:
  ```
  ENVIRONMENT=staging
  DEBUG=True
  FRONTEND_STAGING_URL=https://healwell-staging.vercel.app
  CORS_ORIGINS=https://healwell-staging.vercel.app,http://localhost:5173
  
  LLM_BASE_URL=https://api.openai.com/v1
  LLM_API_KEY=sk-...your-staging-openai-key...
  LLM_MODEL=gpt-4
  LLM_TIMEOUT=30
  
  LOG_LEVEL=INFO
  LOG_FORMAT=json
  ```

- [ ] Deploy service
- [ ] Wait for deployment to complete
- [ ] Note Render URL: `https://healwell-staging.onrender.com`

### Create Vercel Preview Deployment

- [ ] Push changes to GitHub non-main branch
- [ ] Vercel automatically creates preview deployment
- [ ] Note preview URL: `https://healwell-staging.vercel.app`

### Connect Render and Vercel

- [ ] Update Render `FRONTEND_STAGING_URL` with actual Vercel preview URL
- [ ] Update Render `CORS_ORIGINS` with Vercel preview URL
- [ ] Restart Render backend service

### Staging Verification

**Health Check:**
```bash
curl https://healwell-staging.onrender.com/health
```
- [ ] Returns 200
- [ ] Includes environment info

**CORS Preflight:**
```bash
curl -X OPTIONS https://healwell-staging.onrender.com/api/v1/analysis \
  -H "Origin: https://healwell-staging.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -v
```
- [ ] Includes CORS headers
- [ ] Status 200

**Analysis Endpoint:**
```bash
curl -X POST https://healwell-staging.onrender.com/api/v1/analysis \
  -H "Content-Type: application/json" \
  -H "Origin: https://healwell-staging.vercel.app" \
  -d '{"symptoms": "I have a headache"}'
```
- [ ] Returns 200
- [ ] Returns valid analysis with risk_level, specialist, etc.

**Frontend Access:**
- [ ] Open Vercel staging URL: `https://healwell-staging.vercel.app`
  - [ ] Homepage loads
  - [ ] No console CORS errors
  - [ ] Analyze page works
  - [ ] Analysis workflow completes
  - [ ] Results display

---

## Production Deployment (Render + Vercel)

### Create Production Backend Service

- [ ] Create new Render Web Service
- [ ] Connect GitHub repository (main branch only)
- [ ] Configure:
  - [ ] Environment: Python 3.11
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
  - [ ] Region: Select closest to users

- [ ] Add Environment Variables:
  ```
  ENVIRONMENT=production
  DEBUG=False
  FRONTEND_PRODUCTION_URL=https://healwell.vercel.app
  CORS_ORIGINS=https://healwell.vercel.app
  
  LLM_BASE_URL=https://api.openai.com/v1
  LLM_API_KEY=sk-...your-production-openai-key...
  LLM_MODEL=gpt-4
  LLM_TIMEOUT=30
  
  LOG_LEVEL=WARNING
  LOG_FORMAT=json
  ```

- [ ] Deploy backend
- [ ] Wait for deployment complete
- [ ] Note Production URL: `https://healwell-api.onrender.com`

### Deploy Frontend to Vercel Production

- [ ] Push to main branch or deploy from Vercel dashboard
- [ ] Configure environment variables:
  ```
  VITE_API_BASE_URL=https://healwell-api.onrender.com
  VITE_ENVIRONMENT=production
  VITE_DEBUG=false
  ```

- [ ] Set up custom domain (optional)
- [ ] Enable auto-SSL
- [ ] Wait for production deployment complete

### Production Verification

**Backend Health:**
```bash
curl https://healwell-api.onrender.com/health
```
- [ ] Returns 200
- [ ] Status is "healthy"
- [ ] No debug info leaked

**CORS Verification:**
```bash
curl -X OPTIONS https://healwell-api.onrender.com/api/v1/analysis \
  -H "Origin: https://healwell.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -v
```
- [ ] Includes `access-control-allow-origin: https://healwell.vercel.app`
- [ ] No wildcards
- [ ] Status 200

**API Test:**
```bash
curl -X POST https://healwell-api.onrender.com/api/v1/analysis \
  -H "Content-Type: application/json" \
  -H "Origin: https://healwell.vercel.app" \
  -d '{"symptoms": "I have chest pain and shortness of breath"}'
```
- [ ] Returns 200
- [ ] Includes complete analysis
- [ ] Emergency detection works if applicable
- [ ] Response time < 30 seconds

**Frontend Access:**
- [ ] Open production URL: `https://healwell.vercel.app`
  - [ ] Homepage loads
  - [ ] No console errors
  - [ ] Analyze page works
  - [ ] Analysis workflow executes
  - [ ] Results display correctly

**Production Settings Verification:**
- [ ] Backend: `DEBUG=False`
- [ ] Backend: `ENVIRONMENT=production`
- [ ] Frontend: `VITE_DEBUG=false`
- [ ] CORS does NOT include localhost
- [ ] API keys in Render secrets (not .env)
- [ ] No test data in production

---

## Post-Deployment Tasks

### Monitoring Setup

- [ ] Render error tracking enabled
- [ ] Render logs configured with retention
- [ ] Set up alerts for:
  - [ ] API errors (5xx responses)
  - [ ] High response times (> 10s)
  - [ ] Service restarts

### Documentation

- [ ] Update deployment doc with actual URLs
- [ ] Document any custom configurations
- [ ] Create incident response runbook
- [ ] Document rollback procedures

### Performance Monitoring

- [ ] Monitor response times at: Render dashboard
- [ ] Check API latency trends
- [ ] Monitor OpenAI API usage/costs
- [ ] Optimize if response times > 5s

### Security Verification

- [ ] HTTPS enforced on all URLs
- [ ] CORS properly restricted to production domains
- [ ] No API keys in logs
- [ ] No sensitive data exposed
- [ ] Security headers present

---

## Rollback Procedures

### If Backend Breaks

1. Check Render logs: `Render Dashboard → Logs`
2. Review recent environment variable changes
3. Revert problematic configuration
4. Restart backend service
5. Verify health endpoint: `curl https://healwell-api.onrender.com/health`
6. Test analysis endpoint

### If Frontend Breaks

1. Check Vercel deployment logs
2. Verify environment variables are correct
3. Rollback to previous working commit if needed
4. Redeploy
5. Verify homepage loads

### If LLM API Fails

1. Verify `LLM_API_KEY` is valid
2. Check OpenAI account status and quota
3. Monitor OpenAI service status
4. Verify API calls are succeeding in logs
5. Switch to alternative provider if needed

---

## Success Criteria

- [ ] Frontend and backend deployed and running
- [ ] All environment variables correctly configured
- [ ] Health endpoints return 200
- [ ] CORS working for production domains only
- [ ] Analysis workflow executes end-to-end
- [ ] Results display correctly on frontend
- [ ] No errors in production browser console
- [ ] No sensitive data in logs
- [ ] Response times consistently < 10s
- [ ] OpenAI API calls successful
- [ ] Monitoring and alerts configured

---

## Testing Scenarios

### Happy Path

1. User navigates to app
2. Clicks "Get Analysis"
3. Enters symptoms: "I have a mild headache and sore throat"
4. Clicks Submit
5. Receives analysis with low risk, cold/flu recommendation
6. Reads health report and recommendations

### Emergency Scenario

1. User enters: "severe chest pain and difficulty breathing"
2. Analysis marks as emergency
3. Emergency message displays: "🚨 EMERGENCY: Call 911..."
4. User can copy message or call emergency services

### Error Handling

1. Submit empty symptoms → Validation error
2. Backend timeout → User sees error message
3. CORS failure → Console error, no results
4. Invalid API response → Handled gracefully

---

## Support & Troubleshooting

See [docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md) for:
- CORS errors and solutions
- Backend startup issues
- API connection failures
- LLM API errors
- Performance optimization
- Common debugging techniques

---

**HealWell v1.0.0 Deployment Checklist**

Last Updated: July 27, 2026
