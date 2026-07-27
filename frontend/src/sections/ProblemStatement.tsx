import { motion } from 'framer-motion'

export function ProblemStatement() {
  return (
    <section id="problem-statement" className="py-24">
      <div className="max-w-3xl mx-auto px-4">
        <div className="text-center">
          <motion.h2 initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
            className="text-4xl font-bold mb-8" style={{ fontFamily: 'Manrope, sans-serif' }}>
            The Problem We're <span className="gradient-text">Solving</span>
          </motion.h2>

          <motion.p initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.1 }}
            className="text-lg leading-relaxed mb-8" style={{ color: 'rgba(255,255,255,0.65)' }}>
            People often experience symptoms but are unsure whether they require immediate medical attention or simple home care. This uncertainty can lead to delayed treatment, unnecessary hospital visits, increased healthcare costs, and difficulty identifying the appropriate medical specialist. HealWell provides AI-powered health navigation using LangGraph multi-agent automation to help users make informed healthcare decisions.
          </motion.p>

          <motion.div initial={{ opacity: 0, scale: 0.95 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true }} transition={{ delay: 0.2 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-emerald-400/30 text-emerald-400 text-sm font-semibold">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
            SDG 3: Good Health &amp; Well-Being
          </motion.div>
        </div>
      </div>
    </section>
  )
}
