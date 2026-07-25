import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Activity, Menu, X, History, Sparkles, LogIn } from 'lucide-react'
import { Page } from '../types'

export function NavBar({ page, setPage }: { page: Page; setPage: (p: Page) => void }) {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    const h = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', h)
    return () => window.removeEventListener('scroll', h)
  }, [])

  return (
    <motion.nav
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
      className={`fixed top-4 left-1/2 -translate-x-1/2 z-50 w-[calc(100%-2rem)] max-w-6xl rounded-2xl transition-all duration-300 ${scrolled ? 'glass-strong shadow-2xl' : 'glass'}`}>
      <div className="flex items-center justify-between px-5 py-3">
        <button onClick={() => setPage('home')} className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl flex items-center justify-center animate-glow-pulse"
            style={{ background: 'linear-gradient(135deg, #3B82F6, #06B6D4)' }}>
            <Activity size={16} className="text-white" />
          </div>
          <span className="font-bold text-white" style={{ fontFamily: 'Manrope, sans-serif', fontSize: '1.05rem' }}>
            Heal<span className="gradient-text">Well</span>
          </span>
        </button>

        <div className="hidden md:flex items-center gap-1">
          {['Problem', 'How It Works', 'Automation'].map(item => (
            <a key={item} href={`#${item.toLowerCase().replace(/\s+/g, '-')}`}
              className="px-3 py-1.5 text-sm text-white/55 hover:text-white rounded-lg hover:bg-white/05 transition-smooth">
              {item}
            </a>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <button onClick={() => setPage('history')}
            className={`hidden sm:flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-xl btn-ghost ${page === 'history' ? 'text-blue-400 border-blue-400/30 bg-blue-400/10' : ''}`}>
            <History size={14} /> History
          </button>
          <button onClick={() => setPage('analysis')}
            className="btn-primary flex items-center gap-1.5 px-4 py-1.5 text-sm rounded-xl font-semibold">
            <Sparkles size={14} /> Start Analysis
          </button>
          <button onClick={() => setPage('profile')}
            className="hidden sm:flex items-center gap-1.5 px-4 py-1.5 text-sm rounded-xl btn-ghost hover:bg-white/05">
            <LogIn size={14} /> Login
          </button>
          <button className="md:hidden btn-ghost p-2 rounded-xl" onClick={() => setMenuOpen(o => !o)}>
            {menuOpen ? <X size={18} /> : <Menu size={18} />}
          </button>
        </div>
      </div>
      <AnimatePresence>
        {menuOpen && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }} className="md:hidden px-4 pb-4 pt-2 border-t border-white/06">
            {['Problem', 'How It Works', 'Automation'].map(i => (
              <a key={i} href={`#${i.toLowerCase().replace(/\s+/g, '-')}`}
                className="block px-3 py-2 text-sm text-white/55 hover:text-white hover:bg-white/05 rounded-lg"
                onClick={() => setMenuOpen(false)}>{i}</a>
            ))}
            <button onClick={() => { setPage('history'); setMenuOpen(false) }}
              className="w-full text-left px-3 py-2 text-sm text-white/55 hover:text-white hover:bg-white/05 rounded-lg">
              History
            </button>
            <button onClick={() => { setPage('profile'); setMenuOpen(false) }}
              className="w-full text-left px-3 py-2 text-sm text-white/55 hover:text-white hover:bg-white/05 rounded-lg">
              Login
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  )
}
