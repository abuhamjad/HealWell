import { motion } from 'framer-motion'
import { Brain, ArrowRight, Heart } from 'lucide-react'

export function CTA({ setPage }: { setPage: (p: 'analysis') => void }) {
  return (
    <section className="py-20">
      <div className="max-w-4xl mx-auto px-4">
        <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
          className="glass-strong rounded-3xl p-12 text-center relative overflow-hidden">
          <div className="absolute inset-0 rounded-3xl"
            style={{ background: 'radial-gradient(ellipse at center, rgba(59,130,246,0.12) 0%, transparent 70%)' }} />
          <div className="relative z-10">
            <div className="w-14 h-14 rounded-2xl bg-blue-400/15 border border-blue-400/40 flex items-center justify-center mx-auto mb-6">
              <Heart size={28} className="text-blue-400" />
            </div>
            <h2 className="text-3xl font-bold mb-4" style={{ fontFamily: 'Manrope, sans-serif' }}>
              Your health, understood <span className="gradient-text">by AI</span>
            </h2>
            <p className="mb-8 max-w-md mx-auto text-sm leading-relaxed" style={{ color: 'rgba(255,255,255,0.48)' }}>
              Not a replacement for your doctor — a smarter way to understand your symptoms and find the right care at the right time.
            </p>
            <button onClick={() => setPage('analysis')}
              className="btn-primary inline-flex items-center gap-2.5 px-8 py-4 rounded-2xl text-base font-semibold">
              <Brain size={20} /> Begin Health Analysis <ArrowRight size={18} />
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
