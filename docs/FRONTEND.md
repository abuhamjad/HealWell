# HealWell Frontend Documentation - v1.0.0

Production-ready React frontend for HealWell v1.0.0. Modern UI with TypeScript, Tailwind CSS, and Framer Motion animations.

## Technology Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Lucide React** - Icon library
- **Axios** - HTTP client

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   ├── client.ts           # Axios HTTP client
│   │   ├── endpoints.ts        # API endpoint paths
│   │   └── types.ts            # Request/response types
│   ├── components/
│   │   ├── Navbar.tsx          # Navigation bar
│   │   ├── RiskBadge.tsx       # Risk level display
│   │   └── Footer.tsx          # Footer section
│   ├── hooks/
│   │   ├── index.ts            # Hook exports
│   │   └── useAnalysis.ts      # Analysis hook
│   ├── pages/
│   │   ├── Home.tsx            # Landing page
│   │   └── Analysis.tsx        # Analysis page
│   ├── sections/
│   │   ├── Automation.tsx      # Workflow diagram
│   │   ├── CTA.tsx             # Call-to-action
│   │   ├── Footer.tsx          # Footer
│   │   ├── Hero.tsx            # Hero section
│   │   ├── HowItWorks.tsx      # Workflow explanation
│   │   └── ProblemStatement.tsx # Problem section
│   ├── services/
│   │   ├── index.ts            # Service exports
│   │   └── analysis.service.ts # Analysis API service
│   ├── types/
│   │   └── index.ts            # TypeScript definitions
│   ├── config/
│   │   └── env.ts              # Environment variables
│   ├── App.tsx                 # Root component
│   ├── main.tsx                # Entry point
│   └── index.css               # Global styles
├── public/                     # Static assets
├── index.html                  # HTML template
├── package.json
├── vite.config.ts              # Vite configuration
├── tsconfig.json               # TypeScript configuration
├── tailwind.config.js          # Tailwind configuration
└── README.md
```

## Pages

### Home Page (`src/pages/Home.tsx`)

Landing page with:
- Hero section with headline and CTA
- Problem statement
- How it works workflow explanation
- Automation/workflow diagram
- Call-to-action button

### Analysis Page (`src/pages/Analysis.tsx`)

Interactive analysis page with:
- Symptom input form (textarea)
- Analysis submission button
- Loading states with animations
- Results display with:
  - Risk badge
  - Risk assessment details
  - Specialist recommendation
  - Health report
  - Emergency alerts

## Components

### Navbar (`src/components/Navbar.tsx`)

Navigation component with:
- Logo/branding
- Navigation links (Home, Analysis)
- Responsive design
- Mobile menu support

### RiskBadge (`src/components/RiskBadge.tsx`)

Risk level display with:
- Color-coded badges (low/moderate/high)
- Confidence percentage
- Visual indicators

### Footer (`src/components/Footer.tsx`)

Footer section with:
- Navigation links
- Branding information
- Copyright notice

## Sections

### Hero Section (`src/sections/Hero.tsx`)

Main headline and CTA:
- Eye-catching headline
- Subheading
- Call-to-action button with animation
- Hero image/background

### Problem Statement (`src/sections/ProblemStatement.tsx`)

Problem and solution context:
- Problem description
- Why HealWell matters
- Key benefits

### How It Works (`src/sections/HowItWorks.tsx`)

Workflow explanation:
- 6-step process visualization
- Icons and descriptions
- Animation on scroll

### Automation Section (`src/sections/Automation.tsx`)

Visual workflow diagram:
- User → Symptoms
- Symptoms → Analysis
- Analysis → Results
- Icons and flow visualization

### Call-to-Action (`src/sections/CTA.tsx`)

Secondary CTA section:
- Encouragement message
- Analysis button
- Responsive layout

## API Layer

### Client (`src/api/client.ts`)

Axios HTTP client configuration:
- Base URL from environment
- Default headers
- Error handling
- Request/response interceptors

### Endpoints (`src/api/endpoints.ts`)

API route constants:
```typescript
const ENDPOINTS = {
  ANALYSIS: '/analysis'
}
```

### Types (`src/api/types.ts`)

Request/response interfaces:

```typescript
interface AnalysisRequest {
  symptoms: string
}

interface RiskAssessment {
  level: 'low' | 'moderate' | 'high'
  confidence: number
  reasoning: string
  factors: string[]
}

interface SpecialistRecommendation {
  specialist: string
  reason: string
  urgency: string
}

interface HealthReport {
  summary: string
  key_findings: string[]
  self_care: string[]
  when_to_seek_care: string
}

interface AnalysisResponse {
  analysis_id: string
  risk_level: 'low' | 'moderate' | 'high'
  confidence: number
  specialist: string
  emergency: boolean
  risk_assessment: RiskAssessment
  specialist_recommendation: SpecialistRecommendation
  health_report: HealthReport
  emergency_message: string | null
}
```

## Services

### Analysis Service (`src/services/analysis.service.ts`)

API communication service:

```typescript
class AnalysisService {
  async analyze(symptoms: string): Promise<AnalysisResponse>
  // Calls POST /api/v1/analysis
}
```

## Hooks

### useAnalysis (`src/hooks/useAnalysis.ts`)

State management hook for analysis:

```typescript
const {
  symptoms,
  setSymptoms,
  result,
  loading,
  error,
  analyze,
  clearResult
} = useAnalysis()
```

Manages:
- Symptoms input state
- Loading state
- Analysis result
- Error handling
- Submission logic

## Configuration

### Environment (`src/config/env.ts`)

Environment variables:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
const ENVIRONMENT = import.meta.env.VITE_ENVIRONMENT
```

### Vite Config (`vite.config.ts`)

- React plugin
- Port 5173 for dev
- Environment variable support
- Build optimization

### Tailwind Config (`tailwind.config.js`)

- Color schemes
- Typography
- Responsive breakpoints
- Custom utilities

## Styling

**Approach:** Utility-first CSS with Tailwind

**Design System:**
- Primary color: Blue (#3B82F6)
- Secondary color: Indigo (#6366F1)
- Risk colors: Green (low), Yellow (moderate), Red (high)
- Typography: Inter font family
- Spacing: Tailwind scale (4px base unit)

**Animations:**
- Framer Motion for complex animations
- Fade-in/out transitions
- Scale animations on hover
- Slide animations on page transitions

## Development

### Environment Setup

```bash
cd frontend

npm install

# Create .env.local
echo "VITE_API_BASE_URL=http://localhost:8000" > .env.local
```

### Running Dev Server

```bash
npm run dev
# Frontend on http://localhost:5173
```

### Building for Production

```bash
npm run build
# Output in dist/
```

### Type Checking

```bash
npm run type-check
```

## Performance

✅ **Optimization:**
- Code splitting with Vite
- Lazy component loading
- Image optimization
- CSS tree-shaking
- Gzip compression

**Bundle Size (Production):**
- JS: 405 KB (130 KB gzipped)
- CSS: 33 KB (7 KB gzipped)
- Total: ~140 KB gzipped

## Deployment

### Static Site Hosting (Vercel)

```bash
# Deploy to Vercel
vercel deploy

# Environment variables
VITE_API_BASE_URL=https://api.healwell.app
VITE_ENVIRONMENT=production
```

### Docker

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Accessibility

- Semantic HTML
- ARIA labels
- Keyboard navigation
- Color contrast compliance
- Screen reader support

## SEO

- Meta tags
- Open Graph tags
- Structured data
- Mobile-friendly
- Performance metrics

## Error Handling

- Try-catch blocks
- User-friendly error messages
- Graceful degradation
- Network error recovery
- Validation feedback
