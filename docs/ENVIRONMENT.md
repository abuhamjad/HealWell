# Environment Variables Reference - v1.0.0

Complete reference for all HealWell environment configuration across development, staging, and production.

## Overview

Environment variables control HealWell's behavior across:
- **Development:** Local development with full debugging and permissive CORS
- **Staging:** Pre-production testing with production-like settings
- **Production:** Live deployment with strict security

## Core Configuration

### ENVIRONMENT

**Type:** `string`  
**Values:** `development` | `staging` | `production`  
**Default:** `development`

Controls which environment's configuration is active. Affects CORS, debugging, and URL selection.

```env
# Development (most permissive CORS, debug enabled)
ENVIRONMENT=development

# Staging (configured CORS, debug enabled for troubleshooting)
ENVIRONMENT=staging

# Production (strict CORS, debug disabled)
ENVIRONMENT=production
```

### DEBUG

**Type:** `boolean`  
**Values:** `True` | `False`  
**Default:** `True`

Enables FastAPI debug mode and verbose logging.

```env
DEBUG=True    # Development/Staging: Full error details
DEBUG=False   # Production: Hide implementation details
```

### API_TITLE

**Type:** `string`  
**Default:** `HealWell API`

API title displayed in Swagger documentation.

```env
API_TITLE=HealWell API
```

### API_VERSION

**Type:** `string`  
**Default:** `1.0.0`

API version. Must match production release version.

```env
API_VERSION=1.0.0
```

---

## Deployment Configuration

### HOST

**Type:** `string`  
**Default:** `0.0.0.0`

Server bind address.

```env
HOST=0.0.0.0      # Listen on all interfaces (production)
HOST=127.0.0.1    # Listen on localhost only (development)
```

### PORT

**Type:** `integer`  
**Default:** `8000`

Server port.

```env
PORT=8000         # Development and production
```

---

## Frontend URLs

### FRONTEND_URL

**Type:** `string`  
**Default:** `http://localhost:5173`

Frontend URL for development environment. Used when `ENVIRONMENT=development`.

```env
# Local development
FRONTEND_URL=http://localhost:5173

# LAN testing
FRONTEND_URL=http://192.168.1.10:5173
```

### FRONTEND_STAGING_URL

**Type:** `string`  
**Default:** `http://localhost:5173`

Frontend URL for staging environment. Used when `ENVIRONMENT=staging`.

```env
# Vercel preview deployment
FRONTEND_STAGING_URL=https://healwell-staging.vercel.app
```

### FRONTEND_PRODUCTION_URL

**Type:** `string`  
**Default:** `https://healwell.vercel.app`

Frontend URL for production environment. Used when `ENVIRONMENT=production`.

```env
# Vercel production deployment
FRONTEND_PRODUCTION_URL=https://healwell.vercel.app

# Custom domain (example)
FRONTEND_PRODUCTION_URL=https://app.healwell.com
```

---

## CORS Configuration

### CORS_ORIGINS

**Type:** `string` (comma-separated)  
**Default:** `http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000,http://192.168.1.6:5173`

Allowed origins for CORS requests.

```env
# Development (permissive)
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://192.168.1.10:5173

# Staging
CORS_ORIGINS=https://healwell-staging.vercel.app

# Production (strict)
CORS_ORIGINS=https://healwell.vercel.app
```

### CORS_ALLOW_CREDENTIALS

**Type:** `boolean`  
**Default:** `True`

Allow credentials (cookies, authorization headers) in CORS requests.

```env
CORS_ALLOW_CREDENTIALS=True
```

### CORS_ALLOW_METHODS

**Type:** `string` (comma-separated or wildcard)  
**Default:** `*`

HTTP methods allowed by CORS.

```env
CORS_ALLOW_METHODS=*          # All methods
CORS_ALLOW_METHODS=GET,POST,OPTIONS
```

### CORS_ALLOW_HEADERS

**Type:** `string` (comma-separated or wildcard)  
**Default:** `*`

HTTP headers allowed by CORS.

```env
CORS_ALLOW_HEADERS=*          # All headers
CORS_ALLOW_HEADERS=Content-Type
```

---

## API Configuration

### API_PREFIX

**Type:** `string`  
**Default:** `/api/v1`

Base path for all API routes.

```env
API_PREFIX=/api/v1
# Routes: POST /api/v1/analysis
```

### API_HEALTH_CHECK_PATH

**Type:** `string`  
**Default:** `/health`

Health check endpoint path.

```env
API_HEALTH_CHECK_PATH=/health
```

---

## LLM Provider Configuration

### LLM_BASE_URL

**Type:** `string`  
**Default:** `https://api.openai.com/v1`

OpenAI-compatible API endpoint.

Supports:
- OpenAI: `https://api.openai.com/v1`
- OpenRouter: `https://openrouter.ai/api/v1`
- Azure OpenAI: `https://{resource-name}.openai.azure.com/v1`
- Ollama (local): `http://localhost:11434/v1`

```env
# OpenAI (default)
LLM_BASE_URL=https://api.openai.com/v1

# OpenRouter
LLM_BASE_URL=https://openrouter.ai/api/v1

# Ollama local
LLM_BASE_URL=http://localhost:11434/v1
```

### LLM_API_KEY

**Type:** `string`  
**Default:** `` (empty)

API key for the LLM provider. Required for production.

Get keys from:
- OpenAI: https://platform.openai.com/api-keys
- OpenRouter: https://openrouter.ai/account/api-keys

```env
# Development (can be empty for testing)
LLM_API_KEY=

# Production (required)
LLM_API_KEY=sk-...your-key-here...
```

### LLM_MODEL

**Type:** `string`  
**Default:** `gpt-4`

Model name for the LLM provider.

Common models:
- `gpt-4` - Most capable (expensive)
- `gpt-4-turbo` - Turbo version
- `gpt-3.5-turbo` - Budget option
- `claude-opus-4-1` - Via OpenRouter

```env
# Production
LLM_MODEL=gpt-4

# Budget
LLM_MODEL=gpt-3.5-turbo

# Via OpenRouter
LLM_MODEL=meta-llama/llama-2-70b
```

### LLM_TIMEOUT

**Type:** `integer` (seconds)  
**Default:** `30`

Maximum time to wait for LLM response.

```env
LLM_TIMEOUT=30    # 30 seconds per analysis
```

---

## Logging Configuration

### LOG_LEVEL

**Type:** `string`  
**Values:** `DEBUG` | `INFO` | `WARNING` | `ERROR` | `CRITICAL`  
**Default:** `INFO`

Minimum logging level to capture.

```env
LOG_LEVEL=DEBUG      # Development: Show everything
LOG_LEVEL=INFO       # Production: Normal level
LOG_LEVEL=WARNING    # Only warnings and errors
```

### LOG_FORMAT

**Type:** `string`  
**Values:** `json` | `text`  
**Default:** `json`

Log output format. JSON recommended for production (easier parsing).

```env
LOG_FORMAT=json      # Structured logs (production)
LOG_FORMAT=text      # Human-readable logs (development)
```

---

## Frontend Environment Variables

### VITE_API_BASE_URL

**Type:** `string`  
**Frontend config file:** `frontend/src/config/env.ts`

Backend API base URL.

```env
# Development
VITE_API_BASE_URL=http://localhost:8000

# Production
VITE_API_BASE_URL=https://api.healwell.com
```

### VITE_ENVIRONMENT

**Type:** `string`  
**Values:** `development` | `staging` | `production`  
**Frontend config file:** `frontend/src/config/env.ts`

Frontend environment.

```env
VITE_ENVIRONMENT=development
VITE_ENVIRONMENT=production
```

---

## Environment Presets

### Development Preset

```env
# Backend
ENVIRONMENT=development
DEBUG=True
API_TITLE=HealWell API
API_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000

# Frontend URLs
FRONTEND_URL=http://localhost:5173
FRONTEND_STAGING_URL=http://localhost:5173
FRONTEND_PRODUCTION_URL=https://healwell.vercel.app

# CORS
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_METHODS=*
CORS_ALLOW_HEADERS=*

# API
API_PREFIX=/api/v1
API_HEALTH_CHECK_PATH=/health

# LLM (optional for development)
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=
LLM_MODEL=gpt-4
LLM_TIMEOUT=30

# Logging
LOG_LEVEL=DEBUG
LOG_FORMAT=text

# Frontend (.env.local)
VITE_API_BASE_URL=http://localhost:8000
VITE_ENVIRONMENT=development
```

### Staging Preset

```env
# Backend
ENVIRONMENT=staging
DEBUG=True
API_TITLE=HealWell API
API_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000

# Frontend URLs
FRONTEND_URL=https://healwell-staging.vercel.app
FRONTEND_STAGING_URL=https://healwell-staging.vercel.app
FRONTEND_PRODUCTION_URL=https://healwell.vercel.app

# CORS
CORS_ORIGINS=https://healwell-staging.vercel.app
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_METHODS=*
CORS_ALLOW_HEADERS=*

# API
API_PREFIX=/api/v1
API_HEALTH_CHECK_PATH=/health

# LLM
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-...your-staging-key...
LLM_MODEL=gpt-4
LLM_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### Production Preset

```env
# Backend
ENVIRONMENT=production
DEBUG=False
API_TITLE=HealWell API
API_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000

# Frontend URLs
FRONTEND_URL=https://healwell.vercel.app
FRONTEND_STAGING_URL=https://healwell-staging.vercel.app
FRONTEND_PRODUCTION_URL=https://healwell.vercel.app

# CORS
CORS_ORIGINS=https://healwell.vercel.app
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_METHODS=GET,POST,OPTIONS
CORS_ALLOW_HEADERS=Content-Type

# API
API_PREFIX=/api/v1
API_HEALTH_CHECK_PATH=/health

# LLM (required)
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-...your-production-key...
LLM_MODEL=gpt-4
LLM_TIMEOUT=30

# Logging
LOG_LEVEL=WARNING
LOG_FORMAT=json
```

---

## Security Guidelines

### Production Security Checklist

- [ ] `ENVIRONMENT=production`
- [ ] `DEBUG=False`
- [ ] `CORS_ORIGINS` contains only frontend domain (no localhost)
- [ ] `LLM_API_KEY` stored in Render/Vercel secrets (not in git)
- [ ] No API keys or credentials in version control
- [ ] Environment variables set via deployment platform secrets
- [ ] HTTPS used for all frontend/backend URLs

### Never Commit to Git

- [ ] LLM API keys (`LLM_API_KEY`)
- [ ] Any sensitive configuration
- [ ] Production `.env` file

Use `.env` only for local development. In production, use platform secrets:
- **Render:** Environment Variables in dashboard
- **Vercel:** Environment Variables in project settings

---

## Deployment Platform Setup

### Render Environment Variables

1. Go to Service Settings
2. Environment Variables section
3. Add each variable individually
4. Select appropriate environment (Production)
5. Redeploy service

### Vercel Environment Variables

1. Project Settings → Environment Variables
2. Add variable name and value
3. Select environments: Production
4. Save (automatically redeployed)

---

## Troubleshooting

**Q: CORS blocked from frontend**

A: Check that frontend domain is in `CORS_ORIGINS` for active environment. Test with curl:
```bash
curl -i -X OPTIONS http://localhost:8000/api/v1/analysis
```

**Q: Wrong environment settings applied**

A: Verify `ENVIRONMENT` variable matches active environment. Settings are selected based on this value.

**Q: LLM API calls failing with 401**

A: Check `LLM_API_KEY` is set correctly and not expired. Verify with provider dashboard.

**Q: Analysis taking too long**

A: Increase `LLM_TIMEOUT` if consistently hitting timeout. Default 30s is usually sufficient.

**Q: CORS errors in production**

A: Ensure `CORS_ORIGINS` is exact match to frontend domain (no trailing slashes). Use exact domain: `https://example.com` not `https://example.com/`.
