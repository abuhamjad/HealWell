# Environment Variables Reference

Complete reference for all HealWell configuration variables across all environments.

---

## Overview

Environment variables control HealWell's behavior across:
- **Development**: Local development with full debugging
- **Staging**: Pre-production testing with production-like settings
- **Production**: Live deployment with strict security

---

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

### API_TITLE & API_VERSION

**Type:** `string`  
**Default:** `HealWell API` | `0.6.0`

API metadata displayed in Swagger UI and health endpoints.

```env
API_TITLE=HealWell API
API_VERSION=0.6.0
```

---

## Deployment Configuration

### HOST

**Type:** `string`  
**Default:** `0.0.0.0`

Server bind address.

```env
HOST=0.0.0.0      # Listen on all interfaces (development, Render)
HOST=127.0.0.1    # Listen on localhost only (not recommended)
```

### PORT

**Type:** `integer`  
**Default:** `8000`

Server port.

```env
PORT=8000         # Development
PORT=8000         # Render (automatically assigned)
```

---

## Frontend URLs

### FRONTEND_URL

**Type:** `string`  
**Default:** `http://localhost:5173`

Frontend URL used in CORS for development environment. Used when `ENVIRONMENT=development`.

```env
# Local development
FRONTEND_URL=http://localhost:5173

# LAN testing
FRONTEND_URL=http://192.168.1.10:5173
```

### FRONTEND_STAGING_URL

**Type:** `string`  
**Default:** `http://localhost:5173`

Frontend URL used in CORS for staging environment. Used when `ENVIRONMENT=staging`.

```env
# Vercel preview deployment
FRONTEND_STAGING_URL=https://healwell-pr-123.vercel.app
```

### FRONTEND_PRODUCTION_URL

**Type:** `string`  
**Default:** `https://healwell.vercel.app`

Frontend URL used in CORS for production environment. Used when `ENVIRONMENT=production`.

```env
# Production Vercel deployment
FRONTEND_PRODUCTION_URL=https://healwell.vercel.app

# Custom domain (future)
FRONTEND_PRODUCTION_URL=https://app.healwell.health
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
CORS_ORIGINS=https://healwell-pr-123.vercel.app

# Production (strict)
CORS_ORIGINS=https://healwell.vercel.app
```

### CORS_ALLOW_CREDENTIALS

**Type:** `boolean`  
**Default:** `True`

Allow credentials (cookies, authorization headers) in CORS requests.

```env
CORS_ALLOW_CREDENTIALS=True   # Always True for APIs
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
CORS_ALLOW_HEADERS=Content-Type,Authorization
```

---

## API Configuration

### API_PREFIX

**Type:** `string`  
**Default:** `/api/v1`

Base path for all API routes.

```env
API_PREFIX=/api/v1            # Routes: POST /api/v1/analysis
```

### API_HEALTH_CHECK_PATH

**Type:** `string`  
**Default:** `/health`

Health check endpoint path.

```env
API_HEALTH_CHECK_PATH=/health  # GET /health
```

---

## AI/Gemini Configuration (v0.7+)

**Note:** These variables are required for v0.7 Gemini integration but are optional for v0.6.

### GEMINI_API_KEY

**Type:** `string`  
**Default:** `` (empty)

Google Gemini API key. Get from: https://aistudio.google.com/apikey

```env
# Leave empty for v0.6 (uses mock AI)
GEMINI_API_KEY=

# Set for v0.7 production
GEMINI_API_KEY=sk-...your-key-here...
```

### GEMINI_MODEL

**Type:** `string`  
**Default:** `gemini-2.5-flash`

Gemini model to use for AI analysis.

```env
GEMINI_MODEL=gemini-2.5-flash     # Fast, low-cost
GEMINI_MODEL=gemini-2.0-pro       # More capable, higher-cost
```

### AI_TIMEOUT

**Type:** `integer` (seconds)  
**Default:** `30`

Maximum time to wait for AI response.

```env
AI_TIMEOUT=30    # 30 seconds for analysis
```

### AI_MAX_RETRIES

**Type:** `integer`  
**Default:** `3`

Number of retries for failed AI requests.

```env
AI_MAX_RETRIES=3   # Retry up to 3 times on failure
```

### AI_TEMPERATURE

**Type:** `float` (0.0-1.0)  
**Default:** `0.7`

Controls randomness of AI responses.
- `0.0` = Deterministic (same input → same output)
- `1.0` = Creative (varied outputs)

```env
AI_TEMPERATURE=0.7   # Balanced (default)
AI_TEMPERATURE=0.3   # More consistent medical advice
AI_TEMPERATURE=0.9   # More varied responses
```

---

## Database Configuration (v0.9+)

**Note:** These variables are required for v0.9 database integration but are optional for v0.6.

### DATABASE_URL

**Type:** `string`  
**Default:** `` (empty)

PostgreSQL connection string. Format:

```
postgresql://[user[:password]@][host][:port][/dbname][?param=value]
```

```env
# Leave empty for v0.6 (no database)
DATABASE_URL=

# Local development
DATABASE_URL=postgresql://healwell:password@localhost:5432/healwell

# Render PostgreSQL
DATABASE_URL=postgresql://user:password@dpg-xxx.regional.postgres.render.com:5432/healwell_db

# With SSL (production)
DATABASE_URL=postgresql://user:password@host:5432/db?sslmode=require
```

### DATABASE_POOL_SIZE

**Type:** `integer`  
**Default:** `5`

Database connection pool size.

```env
DATABASE_POOL_SIZE=5      # 5 concurrent connections
```

### DATABASE_MAX_OVERFLOW

**Type:** `integer`  
**Default:** `10`

Maximum overflow connections beyond pool size.

```env
DATABASE_MAX_OVERFLOW=10   # Allow 10 extra connections if needed
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

## Environment Presets

### Development Preset

```env
ENVIRONMENT=development
DEBUG=True
FRONTEND_URL=http://localhost:5173
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://192.168.1.10:5173
LOG_LEVEL=DEBUG
LOG_FORMAT=text

# v0.7+ (optional)
GEMINI_API_KEY=
AI_TEMPERATURE=0.7

# v0.9+ (optional)
DATABASE_URL=
```

### Staging Preset

```env
ENVIRONMENT=staging
DEBUG=True
FRONTEND_STAGING_URL=https://healwell-pr-123.vercel.app
CORS_ORIGINS=https://healwell-pr-123.vercel.app
LOG_LEVEL=INFO
LOG_FORMAT=json
PORT=8000
HOST=0.0.0.0

# v0.7+
GEMINI_API_KEY=sk-...your-staging-key...
AI_TEMPERATURE=0.7

# v0.9+
DATABASE_URL=postgresql://user:pass@staging-db:5432/healwell
```

### Production Preset

```env
ENVIRONMENT=production
DEBUG=False
FRONTEND_PRODUCTION_URL=https://healwell.vercel.app
CORS_ORIGINS=https://healwell.vercel.app
LOG_LEVEL=WARNING
LOG_FORMAT=json
PORT=8000
HOST=0.0.0.0

# v0.7+ (required)
GEMINI_API_KEY=sk-...your-production-key...
AI_TEMPERATURE=0.3  # More consistent for production

# v0.9+ (required)
DATABASE_URL=postgresql://user:secure_password@prod-db:5432/healwell_db?sslmode=require
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=50
```

---

## Security Guidelines

### Production Security Checklist

- [ ] `ENVIRONMENT=production`
- [ ] `DEBUG=False`
- [ ] `CORS_ORIGINS` contains only frontend domain (no localhost)
- [ ] `GEMINI_API_KEY` stored in Render/Vercel secrets (not in git)
- [ ] `DATABASE_URL` uses strong password
- [ ] `DATABASE_URL` uses SSL (`sslmode=require`)
- [ ] No API keys or credentials in version control
- [ ] Environment variables set via deployment platform (not .env file)

### Never Commit to Git

- [ ] API keys (GEMINI_API_KEY)
- [ ] Database passwords
- [ ] Production .env file
- [ ] Any sensitive configuration

Use `.env` only for local development. In production, use:
- **Render**: Environment Variables in dashboard
- **Vercel**: Environment Variables in project settings

---

## Deployment Platform Setup

### Render Environment Variables

1. Go to Service Settings
2. Environment Variables section
3. Add each variable individually
4. Select appropriate environment (Preview/Staging/Production)

### Vercel Environment Variables

1. Project Settings → Environment Variables
2. Add variable name and value
3. Select environments: Production/Preview/Development
4. Save (automatically redeployed)

---

## Troubleshooting

**Q: ValidationError: Extra inputs are not permitted**

A: Unknown variables in .env. Only set variables defined in `Settings` class or remove unknown variables.

**Q: CORS blocked from frontend**

A: Check that current domain is in `CORS_ORIGINS` for active environment. Use `curl` to test CORS preflight.

**Q: Wrong environment settings applied**

A: Check `ENVIRONMENT` variable. Settings are selected based on this value, not the deployment platform.

**Q: Database connection refused**

A: Verify `DATABASE_URL` format, credentials, and that database is running and accessible.
