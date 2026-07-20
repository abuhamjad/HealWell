import { motion } from 'framer-motion'
import { Sparkles, ChevronDown, Brain, Heart, Activity, Shield } from 'lucide-react'

function HeroIllustration() {
  const floatingCards = [
    { icon: Heart, label: 'Heart Rate', value: '72 BPM', color: '#EF4444', dx: -200, dy: -110 },
    { icon: Activity, label: 'AI Risk Score', value: 'Low Risk', color: '#22C55E', dx: 200, dy: -90 },
    { icon: Brain, label: 'Neural Analysis', value: '98.2%', color: '#3B82F6', dx: -195, dy: 110 },
    { icon: Shield, label: 'Safety Index', value: 'Protected', color: '#06B6D4', dx: 195, dy: 120 },
  ]

  return (
    <div className="relative w-full h-[520px] flex items-center justify-center select-none">
      {[1, 2, 3].map(i => (
        <motion.div key={i} className="absolute rounded-full border border-blue-500/15"
          style={{ width: 80 + i * 100, height: 80 + i * 100 }}
          animate={{ scale: [1, 1.07, 1], opacity: [0.4, 0.1, 0.4] }}
          transition={{ duration: 3.5, delay: i * 0.9, repeat: Infinity }} />
      ))}

      <div className="relative z-10">
        <motion.div className="w-28 h-28 rounded-full flex items-center justify-center"
          style={{ background: 'radial-gradient(circle, rgba(59,130,246,0.25) 0%, transparent 70%)' }}
          animate={{ scale: [1, 1.06, 1] }} transition={{ duration: 2.8, repeat: Infinity }}>
          <div className="w-20 h-20 rounded-full glass-strong border border-blue-400/40 flex items-center justify-center animate-glow-pulse">
            <Brain size={34} className="text-blue-400" />
          </div>
        </motion.div>
        <div className="absolute inset-[-28px] animate-spin-slow pointer-events-none">
          <div className="w-full h-full rounded-full border border-dashed border-blue-400/20" />
        </div>
        <div className="absolute inset-[-48px] animate-spin-reverse pointer-events-none">
          <div className="w-full h-full rounded-full border border-dashed border-cyan-400/12" />
        </div>
      </div>

      {floatingCards.map((card, i) => (
        <motion.div key={i}
          className="absolute glass rounded-xl p-3 flex items-center gap-2.5"
          style={{ left: `calc(50% + ${card.dx}px)`, top: `calc(50% + ${card.dy}px)`, transform: 'translate(-50%,-50%)' }}
          animate={{ y: [0, -7, 0] }} transition={{ duration: 3.5 + i * 0.6, repeat: Infinity, delay: i * 0.8 }}>
          <div className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
            style={{ background: `${card.color}18`, border: `1px solid ${card.color}40` }}>
            <card.icon size={16} style={{ color: card.color }} />
          </div>
          <div>
            <div className="text-[10px] text-white/35">{card.label}</div>
            <div className="text-sm font-semibold text-white">{card.value}</div>
          </div>
        </motion.div>
      ))}

      <div className="absolute right-10 top-6 opacity-25">
        <svg width="36" height="110" viewBox="0 0 36 110">
          {Array.from({ length: 12 }).map((_, i) => (
            <g key={i}>
              <circle cx={18 + Math.sin(i * 0.85) * 14} cy={i * 9 + 5} r="2.5"
                fill={i % 2 === 0 ? '#3B82F6' : '#06B6D4'} opacity="0.9" />
              {i < 11 && (
                <line x1={18 + Math.sin(i * 0.85) * 14} y1={i * 9 + 5}
                  x2={18 + Math.sin((i + 1) * 0.85) * 14} y2={(i + 1) * 9 + 5}
                  stroke="rgba(255,255,255,0.12)" strokeWidth="1" />
              )}
            </g>
          ))}
        </svg>
      </div>

      <div className="absolute bottom-10 left-1/2 -translate-x-1/2 w-56 h-8 opacity-35">
        <svg viewBox="0 0 224 32" className="w-full h-full">
          <motion.polyline points="0,16 28,16 42,3 56,29 70,3 84,29 98,16 224,16"
            fill="none" stroke="#3B82F6" strokeWidth="2" strokeLinecap="round"
            initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
            transition={{ duration: 2.5, repeat: Infinity, ease: 'linear' }} />
        </svg>
      </div>

      {Array.from({ length: 6 }).map((_, i) => (
        <motion.div key={i} className="absolute w-1 h-1 rounded-full bg-blue-400/30"
          style={{ left: 60 + i * 60, top: 200 + (i % 3) * 60 }}
          animate={{ y: [0, -50, 0], opacity: [0, 0.7, 0], scale: [0, 1, 0] }}
          transition={{ duration: 4, delay: i * 0.7, repeat: Infinity }} />
      ))}
    </div>
  )
}

export function Hero({ setPage }: { setPage: (p: 'analysis') => void }) {
  return (
    <section className="min-h-screen flex items-center pt-24 pb-16 relative overflow-hidden">
      <div className="max-w-6xl mx-auto px-4 w-full">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-blue-400/25 text-blue-400 text-sm font-medium mb-8">
              <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
              IBM SkillsBuild · SDG 3 · Good Health &amp; Well-being
            </motion.div>

            <motion.h1 initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
              className="text-5xl lg:text-6xl font-black leading-[1.08] mb-6"
              style={{ fontFamily: 'Manrope, sans-serif', letterSpacing: '-0.02em' }}>
              Navigate Your<br />Health with{' '}
              <span className="gradient-text">AI,</span><br />
              <span style={{ color: 'rgba(255,255,255,0.72)' }}>Not Guesswork.</span>
            </motion.h1>

            <motion.p initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
              className="text-lg leading-relaxed mb-10 max-w-lg" style={{ color: 'rgba(255,255,255,0.52)' }}>
              HealWell is an intelligent health navigator powered by 9 specialized AI agents.
              Describe symptoms naturally — by text or voice — and get a comprehensive health
              assessment with specialist guidance, home-care advice, and nearby doctor locations.
            </motion.p>

            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}
              className="flex flex-col sm:flex-row gap-3">
              <button onClick={() => setPage('analysis')}
                className="btn-primary flex items-center justify-center gap-2 px-7 py-3.5 rounded-2xl text-base font-semibold">
                <Sparkles size={18} /> Start Health Analysis
              </button>
              <a href="#problem-statement" className="btn-ghost flex items-center justify-center gap-2 px-7 py-3.5 rounded-2xl text-base font-medium">
                Learn More <ChevronDown size={16} />
              </a>
            </motion.div>

            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.6 }}
              className="flex items-center gap-8 mt-10 pt-8 border-t border-white/08">
              {[{ val: '9', label: 'AI Agents' }, { val: '99.2%', label: 'Accuracy' }, { val: '<3s', label: 'Analysis Time' }].map(stat => (
                <div key={stat.label}>
                  <div className="text-2xl font-bold gradient-text" style={{ fontFamily: 'Manrope, sans-serif' }}>{stat.val}</div>
                  <div className="text-xs mt-0.5" style={{ color: 'rgba(255,255,255,0.38)' }}>{stat.label}</div>
                </div>
              ))}
            </motion.div>
          </div>

          <motion.div initial={{ opacity: 0, scale: 0.92 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.3, type: 'spring', stiffness: 80 }}>
            <HeroIllustration />
          </motion.div>
        </div>
      </div>
    </section>
  )
}
