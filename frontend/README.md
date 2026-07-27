# HealWell Frontend - v1.0.0

React-based frontend for HealWell health analysis platform.

Modern UI built with React 19, TypeScript, Tailwind CSS, and Framer Motion.

## Quick Start

### 1. Install Dependencies

```bash
cd frontend

npm install
```

### 2. Configure Environment

```bash
cat > .env.local << EOF
VITE_API_BASE_URL=http://localhost:8000
VITE_ENVIRONMENT=development
EOF
```

### 3. Run Development Server

```bash
npm run dev
```

Frontend runs on: `http://localhost:5173`

## Available Scripts

```bash
# Development
npm run dev              # Start dev server

# Production
npm run build            # Build for production
npm run preview          # Preview production build

# Quality
npm run type-check       # TypeScript type checking
npm run lint             # ESLint checks
```

## Technology Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool (5x faster than Create React App)
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Lucide React** - Icon library
- **Axios** - HTTP client

## Project Structure

```
src/
├── api/                 # API communication
│   ├── client.ts       # Axios HTTP client
│   ├── endpoints.ts    # API paths
│   └── types.ts        # Request/response types
├── components/         # React components
│   ├── Navbar.tsx
│   ├── RiskBadge.tsx
│   └── Footer.tsx
├── hooks/              # Custom React hooks
│   └── useAnalysis.ts
├── pages/              # Page components
│   ├── Home.tsx
│   └── Analysis.tsx
├── sections/           # Section components
│   ├── Automation.tsx
│   ├── CTA.tsx
│   ├── Footer.tsx
│   ├── Hero.tsx
│   ├── HowItWorks.tsx
│   └── ProblemStatement.tsx
├── services/           # Business logic
│   └── analysis.service.ts
├── types/              # TypeScript definitions
│   └── index.ts
├── config/             # Configuration
│   └── env.ts
├── App.tsx             # Root component
├── main.tsx            # Entry point
└── index.css           # Global styles
```

## Pages

### Home (`/`)

Landing page featuring:
- Hero section with CTA
- Problem statement
- How it works explanation
- Automation workflow diagram
- Call-to-action buttons

### Analysis (`/analysis`)

Analysis page with:
- Symptom input form
- Submit button
- Loading animations
- Results display
- Risk assessment
- Specialist recommendation
- Health report

## Components

### Navbar
Navigation with links to Home and Analysis pages.

### RiskBadge
Displays risk level (low/moderate/high) with color coding and confidence percentage.

### Footer
Footer with navigation links and copyright information.

## Hooks

### useAnalysis
Manages analysis state and API calls:
- `symptoms` - Input symptoms
- `result` - Analysis results
- `loading` - Loading state
- `error` - Error messages
- `analyze()` - Submit for analysis
- `clearResult()` - Reset state

## Services

### analysisService
API communication:
- `analyze(symptoms)` - POST /api/v1/analysis

## Styling

**Design System:**
- Primary: Blue (#3B82F6)
- Secondary: Indigo (#6366F1)
- Risk colors: Green/Yellow/Red
- Font: Inter
- Responsive mobile-first

**Animations:**
- Framer Motion for complex transitions
- Smooth page transitions
- Loading spinners
- Result fade-in

## Configuration

Environment variables in `.env.local`:

```env
VITE_API_BASE_URL=http://localhost:8000  # Backend URL
VITE_ENVIRONMENT=development             # Environment
```

See [docs/ENVIRONMENT.md](../docs/ENVIRONMENT.md) for all options.

## Performance

**Production Build:**
- JavaScript: 405 KB (130 KB gzipped)
- CSS: 33 KB (7 KB gzipped)
- Total: ~140 KB gzipped

**Optimizations:**
- Code splitting
- Tree-shaking
- Image optimization
- CSS minification
- Gzip compression

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Accessibility

- Semantic HTML
- ARIA labels
- Keyboard navigation
- Screen reader support
- Color contrast compliance

## Development

### Type Checking

```bash
npm run type-check
```

All TypeScript types enforced at compile time.

### Code Style

- ESLint for code quality
- Prettier for formatting (if configured)
- TypeScript for type safety

### Adding Components

1. Create component in `src/components/`
2. Export from `src/components/index.ts`
3. Use in pages/sections
4. Add TypeScript interfaces

### Adding API Endpoints

1. Add endpoint to `src/api/endpoints.ts`
2. Add types to `src/api/types.ts`
3. Create service method in `src/services/`
4. Use in component via hook

## Testing

```bash
# Coming soon
npm run test
npm run test:coverage
```

## Deployment

### Development

```bash
npm run dev
```

### Production Build

```bash
npm run build
```

Output in `dist/` directory.

### Deploy to Vercel

```bash
npm i -g vercel
vercel --prod
```

Environment variables configured in Vercel dashboard.

## Troubleshooting

### CORS Errors

**Problem:** API calls blocked by CORS policy

**Solution:**
1. Check backend `CORS_ORIGINS` includes frontend URL
2. Verify `VITE_API_BASE_URL` matches backend URL
3. Test with browser DevTools Network tab

### API Calls Fail

**Problem:** 404 or connection refused

**Solution:**
1. Verify backend is running
2. Check `VITE_API_BASE_URL` in `.env.local`
3. Check browser Network tab for actual request URL

### Build Fails

**Problem:** TypeScript errors or build errors

**Solution:**
1. Run `npm run type-check` to find issues
2. Ensure all dependencies installed: `npm install`
3. Clear cache: `rm -rf node_modules dist`

## Medical Disclaimer

HealWell provides AI-generated health information for **educational purposes only**.

It is **not** a replacement for professional medical advice. Always consult qualified healthcare professionals.

In case of emergency, contact local emergency services immediately.

## Support

- 📖 Documentation: [docs/](../docs/)
- 🐛 Issues: GitHub Issues
- 📧 Contact: See main README

## Version

**v1.0.0** - Production Ready

---

**Made with React, TypeScript, Vite, and Tailwind CSS.**
