import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Page } from './types'
import { NavBar } from './components/Navbar'
import { Home } from './pages/Home'
import { Analysis } from './pages/Analysis'
import { About } from './pages/About'
import { Footer } from './sections/Footer'
import { BackgroundOrbs } from './utils/BackgroundOrbs'

export default function App() {
  const [page, setPage] = useState<Page>('home')

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, [page])

  return (
    <div className="min-h-screen relative" style={{ background: '#050505' }}>
      <BackgroundOrbs />
      <NavBar page={page} setPage={setPage} />
      <main className="relative z-10">
        <AnimatePresence mode="wait">
          {page === 'home' && (
            <motion.div key="home" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.25 }}>
              <Home setPage={() => setPage('analysis')} />
            </motion.div>
          )}
          {page === 'analysis' && (
            <motion.div key="analysis" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.25 }}>
              <Analysis />
            </motion.div>
          )}
          {page === 'about' && (
            <motion.div key="about" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.25 }}>
              <About />
            </motion.div>
          )}
        </AnimatePresence>
      </main>
      <div className="relative z-10">
        <Footer setPage={setPage} />
      </div>
    </div>
  )
}
