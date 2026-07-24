import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  History as HistoryIcon, Search, X, FileText, AlertTriangle, Clock,
  Stethoscope, Brain, ChevronDown, Eye, Download, Calendar
} from 'lucide-react'
import { AnalysisResult, RiskLevel } from '../types'
import { RiskBadge } from '../components/RiskBadge'

const SAMPLE_HISTORY: AnalysisResult[] = [
  {
    id: '1', date: '2026-07-18',
    symptoms: 'Severe headache on the right side, light sensitivity, nausea lasting 6 hours',
    riskLevel: 'moderate', confidence: 87,
    summary: 'Symptoms consistent with tension or migraine headache. No signs of neurological emergency detected.',
    specialist: 'Neurologist', specialistIcon: '🧠', emergency: false, emergencyNote: '',
    homeCare: ['Rest in a dark room', 'Apply a cold or warm compress', 'Stay well hydrated'],
    lifestyle: ['Maintain a regular sleep schedule', 'Reduce caffeine intake', 'Practice daily stress management'],
    monitor: ['Frequency of headaches', 'Duration and intensity', 'Visual disturbances'],
    nearbyDoctors: [], agentOutputs: []
  },
  {
    id: '2', date: '2026-07-12',
    symptoms: 'Persistent dry cough, mild fever of 99.8°F, fatigue persisting for 3 days',
    riskLevel: 'low', confidence: 92,
    summary: 'Upper respiratory symptoms likely viral in origin. Self-limiting condition with home management appropriate.',
    specialist: 'General Practitioner', specialistIcon: '🩺', emergency: false, emergencyNote: '',
    homeCare: ['Rest and prioritize sleep', 'Honey-lemon tea', 'OTC fever reducers', 'Isolate from household'],
    lifestyle: ['Boost immunity with vitamin C', 'Light exercise once recovered', 'Maintain adequate hydration'],
    monitor: ['Temperature trends', 'Difficulty breathing', 'Symptom duration beyond 7 days'],
    nearbyDoctors: [], agentOutputs: []
  },
  {
    id: '3', date: '2026-07-05',
    symptoms: 'Sharp chest pain on left side, shortness of breath, sweating — sudden onset 1 hour ago',
    riskLevel: 'high', confidence: 95,
    summary: 'High-priority symptoms requiring immediate medical evaluation. Cardiac causes must be ruled out urgently.',
    specialist: 'Cardiologist', specialistIcon: '❤️', emergency: true, emergencyNote: 'Seek emergency care immediately. Call 112 or have someone drive you to the nearest emergency room.',
    homeCare: [], lifestyle: [], monitor: [],
    nearbyDoctors: [], agentOutputs: []
  },
]

export function History() {
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState<'all' | RiskLevel>('all')
  const [expanded, setExpanded] = useState<string | null>(null)

  const filtered = SAMPLE_HISTORY.filter(h => {
    const matchSearch = !search || h.symptoms.toLowerCase().includes(search.toLowerCase()) || h.specialist.toLowerCase().includes(search.toLowerCase())
    const matchFilter = filter === 'all' || h.riskLevel === filter
    return matchSearch && matchFilter
  })

  return (
    <div className="min-h-screen pt-28 pb-20">
      <div className="max-w-4xl mx-auto px-4">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-10">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-white/10 text-sm font-medium mb-6"
            style={{ color: 'rgba(255,255,255,0.55)' }}>
            <HistoryIcon size={14} className="text-blue-400" /> Analysis History
          </div>
          <h1 className="text-4xl font-bold mb-2" style={{ fontFamily: 'Manrope, sans-serif' }}>
            Your Health <span className="gradient-text">Timeline</span>
          </h1>
          <p style={{ color: 'rgba(255,255,255,0.42)' }}>Track patterns and progress across your health analyses</p>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
          className="glass rounded-2xl p-4 mb-6 flex flex-col sm:flex-row gap-3">
          <div className="flex-1 flex items-center gap-2 glass rounded-xl px-3 py-2.5">
            <Search size={14} style={{ color: 'rgba(255,255,255,0.28)' }} />
            <input value={search} onChange={e => setSearch(e.target.value)}
              placeholder="Search symptoms, specialists..."
              className="bg-transparent text-sm text-white placeholder-white/22 outline-none flex-1" />
            {search && <button onClick={() => setSearch('')}><X size={13} style={{ color: 'rgba(255,255,255,0.28)' }} /></button>}
          </div>
          <div className="flex gap-2 flex-wrap">
            {(['all', 'low', 'moderate', 'high'] as const).map(f => (
              <button key={f} onClick={() => setFilter(f)}
                className={`px-3 py-1.5 rounded-xl text-sm font-medium transition-smooth border capitalize ${filter === f ? 'bg-blue-500/18 border-blue-400/48 text-blue-300' : 'border-white/08 text-white/38 hover:border-white/14 hover:text-white/58'}`}>
                {f === 'all' ? 'All' : `${f} risk`}
              </button>
            ))}
          </div>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}
          className="grid grid-cols-3 gap-3 mb-8">
          {[
            { label: 'Total Analyses', value: SAMPLE_HISTORY.length.toString(), icon: FileText, color: '#3B82F6' },
            { label: 'High Risk Events', value: SAMPLE_HISTORY.filter(h => h.riskLevel === 'high').length.toString(), icon: AlertTriangle, color: '#EF4444' },
            { label: 'Last Analysis', value: '2 days ago', icon: Clock, color: '#22C55E' },
          ].map(stat => (
            <div key={stat.label} className="glass rounded-xl p-4 flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                style={{ background: `${stat.color}14`, border: `1px solid ${stat.color}30` }}>
                <stat.icon size={14} style={{ color: stat.color }} />
              </div>
              <div>
                <div className="text-lg font-bold text-white" style={{ fontFamily: 'Manrope, sans-serif' }}>{stat.value}</div>
                <div className="text-[11px]" style={{ color: 'rgba(255,255,255,0.32)' }}>{stat.label}</div>
              </div>
            </div>
          ))}
        </motion.div>

        <div className="relative pl-14">
          <div className="absolute left-5 top-0 bottom-0 w-px"
            style={{ background: 'linear-gradient(180deg, rgba(59,130,246,0.35), rgba(255,255,255,0.06) 80%, transparent)' }} />

          {filtered.length === 0 ? (
            <div className="text-center py-16" style={{ color: 'rgba(255,255,255,0.28)' }}>
              <HistoryIcon size={36} className="mx-auto mb-3 opacity-30" />
              <div className="text-sm">No analyses match your search</div>
            </div>
          ) : (
            <div className="space-y-4">
              {filtered.map((item, i) => (
                <motion.div key={item.id} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.11 }}
                  className="relative">
                  <div className={`absolute flex items-center justify-center w-10 h-10 rounded-xl border-2 ${item.riskLevel === 'high' ? 'bg-red-500/18 border-red-400/55' : item.riskLevel === 'moderate' ? 'bg-yellow-500/14 border-yellow-400/48' : 'bg-emerald-500/14 border-emerald-400/48'}`}
                    style={{ left: -52, top: 14 }}>
                    <span className="text-base">{item.specialistIcon}</span>
                  </div>

                  <div className={`glass rounded-2xl overflow-hidden hover:scale-[1.004] transition-smooth border ${item.riskLevel === 'high' ? 'border-red-500/18' : item.riskLevel === 'moderate' ? 'border-yellow-500/12' : 'border-white/08'}`}>
                    <div className="p-5">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                            <Calendar size={11} style={{ color: 'rgba(255,255,255,0.28)' }} />
                            <span className="text-xs font-mono" style={{ color: 'rgba(255,255,255,0.38)' }}>{item.date}</span>
                            <RiskBadge level={item.riskLevel} />
                            {item.emergency && (
                              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-red-500/18 border border-red-500/38 text-red-400">
                                <AlertTriangle size={8} /> Emergency
                              </span>
                            )}
                          </div>
                          <p className="text-sm font-medium leading-snug max-w-lg" style={{ color: 'rgba(255,255,255,0.75)' }}>{item.symptoms}</p>
                        </div>
                        <button onClick={() => setExpanded(expanded === item.id ? null : item.id)}
                          className="btn-ghost p-1.5 rounded-lg ml-3 flex-shrink-0">
                          <ChevronDown size={14} className={`transition-smooth ${expanded === item.id ? 'rotate-180' : ''}`} style={{ color: 'rgba(255,255,255,0.38)' }} />
                        </button>
                      </div>
                      <div className="flex items-center gap-4 text-xs" style={{ color: 'rgba(255,255,255,0.38)' }}>
                        <div className="flex items-center gap-1.5">
                          <Stethoscope size={11} /><span>{item.specialist}</span>
                        </div>
                        <div className="flex items-center gap-1.5">
                          <Brain size={11} /><span>{(item.confidence * 100).toFixed(0)}% confidence</span>
                        </div>
                      </div>
                    </div>

                    <AnimatePresence>
                      {expanded === item.id && (
                        <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }} className="overflow-hidden">
                          <div className="border-t border-white/06 p-5 space-y-4">
                            <div>
                              <div className="text-xs font-semibold mb-2" style={{ color: 'rgba(255,255,255,0.45)' }}>AI Summary</div>
                              <p className="text-sm leading-relaxed" style={{ color: 'rgba(255,255,255,0.62)' }}>{item.summary}</p>
                            </div>
                            {item.homeCare.length > 0 && (
                              <div>
                                <div className="text-xs font-semibold mb-2" style={{ color: 'rgba(255,255,255,0.45)' }}>Home-Care Suggestions</div>
                                <ul className="space-y-1.5">
                                  {item.homeCare.map((h, hi) => (
                                    <li key={hi} className="text-xs flex items-start gap-2" style={{ color: 'rgba(255,255,255,0.48)' }}>
                                      <span className="w-1 h-1 rounded-full bg-emerald-400/55 mt-1.5 flex-shrink-0" /> {h}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}
                            <div className="flex gap-2 pt-2">
                              <button className="btn-ghost flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs">
                                <Eye size={11} /> View Report
                              </button>
                              <button className="btn-ghost flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs">
                                <Download size={11} /> Download PDF
                              </button>
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
