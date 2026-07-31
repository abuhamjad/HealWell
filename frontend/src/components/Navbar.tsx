import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Activity, Menu, X, Sparkles } from 'lucide-react'
import { Page } from '../types'

const smoothScroll = (id: string) => {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

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
          <img
            src="/favicon.png"
            alt="HealWell Logo"
            className="w-8 h-8 rounded-lg object-cover"
            draggable={false}
          />
          <span className="font-bold text-white" style={{ fontFamily: 'Manrope, sans-serif', fontSize: '1.05rem' }}>
            Heal<span className="gradient-text">Well</span>
          </span>
        </button>

        {page === 'home' && (
          <div className="hidden md:flex items-center gap-1">
            {[{ label: 'Problem', id: 'problem-statement' }, { label: 'How It Works', id: 'how-it-works' }, { label: 'Automation', id: 'automation' }].map(item => (
              <button key={item.id} onClick={() => smoothScroll(item.id)}
                className="px-3 py-1.5 text-sm text-white/55 hover:text-white rounded-lg hover:bg-white/05 transition-smooth">
                {item.label}
              </button>
            ))}
          </div>
        )}

        <div className="hidden md:flex items-center gap-2">
          <button onClick={() => setPage('about')}
            className="px-3 py-1.5 text-sm text-white/55 hover:text-white rounded-lg hover:bg-white/05 transition-smooth">
            About
          </button>
        </div>

        <div className="flex items-center gap-2">
          <button onClick={() => setPage('analysis')}
            className="btn-primary flex items-center gap-1.5 px-4 py-1.5 text-sm rounded-xl font-semibold">
            <Sparkles size={14} /> Start Analysis
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
            <button onClick={() => { setPage('about'); setMenuOpen(false) }}
              className="block w-full text-left px-3 py-2 text-sm text-white/55 hover:text-white hover:bg-white/05 rounded-lg">About</button>
            {page === 'home' && (
              <>
                {[{ label: 'Problem', id: 'problem-statement' }, { label: 'How It Works', id: 'how-it-works' }, { label: 'Automation', id: 'automation' }].map(i => (
                  <button key={i.id} onClick={() => { smoothScroll(i.id); setMenuOpen(false) }}
                    className="block w-full text-left px-3 py-2 text-sm text-white/55 hover:text-white hover:bg-white/05 rounded-lg">{i.label}</button>
                ))}
              </>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  )
}
