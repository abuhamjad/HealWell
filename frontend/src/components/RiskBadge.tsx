import { RiskLevel } from '../types'
import { Star } from 'lucide-react'

export function RiskBadge({ level }: { level: RiskLevel }) {
  const cfg = {
    low: { cls: 'text-emerald-400 border-emerald-400/30 bg-emerald-400/10', label: 'Low Risk', dot: 'bg-emerald-400' },
    moderate: { cls: 'text-yellow-400 border-yellow-400/30 bg-yellow-400/10', label: 'Moderate Risk', dot: 'bg-yellow-400' },
    high: { cls: 'text-red-400 border-red-400/30 bg-red-400/10', label: 'High Risk', dot: 'bg-red-400' },
  }
  const c = cfg[level]
  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border ${c.cls}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${c.dot} animate-pulse`} />
      {c.label}
    </span>
  )
}

export function StarRating({ rating }: { rating: number }) {
  return (
    <div className="flex items-center gap-0.5">
      {[1, 2, 3, 4, 5].map(i => (
        <Star key={i} size={10} className={i <= Math.floor(rating) ? 'text-yellow-400 fill-yellow-400' : 'text-white/20'} />
      ))}
      <span className="text-xs text-white/50 ml-1">{rating}</span>
    </div>
  )
}
