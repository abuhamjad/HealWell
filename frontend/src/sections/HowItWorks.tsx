import { motion } from 'framer-motion'
import { MessageSquare, Mic, Brain, Activity, Stethoscope, Download } from 'lucide-react'

const steps = [
  { step: '1', title: 'Describe Symptoms', desc: 'Type or speak naturally about how you\'re feeling', icon: MessageSquare },
  { step: '2', title: 'Speech-to-Text', desc: 'Voice converted to data with medical vocabulary support', icon: Mic },
  { step: '3', title: 'Symptom Analysis', desc: 'AI analyzes symptoms contextually and identifies patterns', icon: Brain },
  { step: '4', title: 'Risk Assessment', desc: 'Low, Moderate, or High risk determination with reasoning', icon: Activity },
  { step: '5', title: 'Specialist Recommendation', desc: 'Best-match healthcare provider specialty identified', icon: Stethoscope },
  { step: '6', title: 'Health Report', desc: 'Comprehensive PDF report ready for download', icon: Download },
]

export function HowItWorks() {
  return (
    <section id="how-it-works" className="py-24">
      <div className="max-w-5xl mx-auto px-4">
        <div className="text-center mb-16">
          <motion.h2 initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
            className="text-4xl font-bold" style={{ fontFamily: 'Manrope, sans-serif' }}>
            From symptoms to <span className="gradient-text">insights in seconds</span>
          </motion.h2>
        </div>

        <div className="relative pl-8">
          <div className="absolute left-3.5 top-0 bottom-0 w-px bg-gradient-to-b from-blue-400/40 to-transparent" />

          <div className="space-y-8">
            {steps.map((step, i) => (
              <motion.div key={step.step} initial={{ opacity: 0, x: -20 }} whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }} transition={{ delay: i * 0.08 }} className="relative">
                <div className="absolute -left-6 w-8 h-8 rounded-full glass border border-blue-400/50 flex items-center justify-center bg-blue-400/10">
                  <span className="text-xs font-bold text-blue-400">{step.step}</span>
                </div>

                <motion.div initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }} transition={{ delay: i * 0.08 + 0.1 }}
                  className="glass rounded-2xl p-5 hover:border-blue-400/30 border border-white/08 transition-smooth group">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-smooth"
                      style={{ background: 'rgba(59,130,246,0.14)', border: '1px solid rgba(59,130,246,0.35)' }}>
                      <step.icon size={20} className="text-blue-400" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-white mb-1" style={{ fontFamily: 'Manrope, sans-serif' }}>{step.title}</h3>
                      <p className="text-sm leading-relaxed" style={{ color: 'rgba(255,255,255,0.48)' }}>{step.desc}</p>
                    </div>
                  </div>
                </motion.div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
