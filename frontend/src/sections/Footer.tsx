import { Activity } from 'lucide-react'
import { Page } from '../types'

export function Footer({ setPage }: { setPage: (p: Page) => void }) {
  return (
    <footer className="border-t border-white/05 py-12 mt-8">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-xl flex items-center justify-center"
              style={{ background: 'linear-gradient(135deg, #3B82F6, #06B6D4)' }}>
              <Activity size={14} className="text-white" />
            </div>
            <span className="font-bold text-white" style={{ fontFamily: 'Manrope, sans-serif' }}>
              Heal<span className="gradient-text">Well</span>
            </span>
            <span className="mx-2" style={{ color: 'rgba(255,255,255,0.18)' }}>·</span>
            <span className="text-sm" style={{ color: 'rgba(255,255,255,0.32)' }}>IBM SkillsBuild · SDG 3</span>
          </div>
          <div className="flex items-center gap-4 text-sm" style={{ color: 'rgba(255,255,255,0.32)' }}>
            {(['home', 'analysis'] as const).map(p => (
              <button key={p} onClick={() => setPage(p)} className="capitalize hover:text-white/65 transition-smooth">{p}</button>
            ))}
          </div>
          <p className="text-xs text-center" style={{ color: 'rgba(255,255,255,0.18)' }}>
            Not a medical diagnosis tool. Always consult a qualified healthcare professional.
          </p>
        </div>
      </div>
    </footer>
  )
}
