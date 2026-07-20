import { motion } from 'framer-motion'
import { Network, Brain, Mic, FileText, AlertTriangle, Stethoscope, MapPin, CheckCircle } from 'lucide-react'
import { useState } from 'react'

const LANGGRAPH_NODES = [
  { id: 'user', label: 'User Input', icon: '👤', color: '#3B82F6', x: 50, y: 200 },
  { id: 'stt', label: 'Speech-to-Text', icon: '🎙️', color: '#8B5CF6', x: 185, y: 120 },
  { id: 'symptom', label: 'Symptom Analysis', icon: '🔬', color: '#06B6D4', x: 340, y: 75 },
  { id: 'history', label: 'Medical History', icon: '📋', color: '#3B82F6', x: 340, y: 200 },
  { id: 'risk', label: 'Risk Assessment', icon: '⚡', color: '#FACC15', x: 500, y: 135 },
  { id: 'emergency', label: 'Emergency Detection', icon: '🚨', color: '#EF4444', x: 500, y: 265 },
  { id: 'specialist', label: 'Specialist Rec.', icon: '👨‍⚕️', color: '#22C55E', x: 660, y: 135 },
  { id: 'doctor', label: 'Doctor Finder', icon: '📍', color: '#F97316', x: 660, y: 265 },
  { id: 'report', label: 'Health Report', icon: '📄', color: '#A855F7', x: 820, y: 200 },
]

const LANGGRAPH_EDGES = [
  { from: 'user', to: 'stt' }, { from: 'user', to: 'symptom' },
  { from: 'stt', to: 'symptom' }, { from: 'symptom', to: 'history' },
  { from: 'symptom', to: 'risk' }, { from: 'history', to: 'risk' },
  { from: 'risk', to: 'emergency' }, { from: 'risk', to: 'specialist' },
  { from: 'emergency', to: 'specialist' }, { from: 'specialist', to: 'doctor' },
  { from: 'specialist', to: 'report' }, { from: 'doctor', to: 'report' },
]

export function Automation() {
  const [activeNode, setActiveNode] = useState<string | null>(null)

  const getNode = (id: string) => LANGGRAPH_NODES.find(n => n.id === id)

  return (
    <section id="automation" className="py-24">
      <div className="max-w-6xl mx-auto px-4">
        <div className="text-center mb-16">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-cyan-400/22 text-cyan-400 text-sm font-medium mb-6">
            <Network size={14} /> LangGraph Multi-Agent Automation
          </motion.div>
          <motion.h2 initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.1 }}
            className="text-4xl font-bold mb-4" style={{ fontFamily: 'Manrope, sans-serif' }}>
            <span className="text-white">Intelligent Agents</span>
            <br /><span className="gradient-text">Working in Harmony</span>
          </motion.h2>
          <motion.p initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.2 }}
            className="text-white/45 max-w-xl mx-auto text-sm leading-relaxed">
            Nine specialized AI agents collaborate through LangGraph's orchestration framework,
            each contributing unique medical expertise to your health assessment.
          </motion.p>
        </div>

        <motion.div initial={{ opacity: 0, scale: 0.96 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true }}
          className="glass rounded-3xl p-6 overflow-x-auto">
          <div className="relative" style={{ minWidth: 900, height: 360 }}>
            <svg className="absolute inset-0 w-full h-full" style={{ zIndex: 0 }}>
              <defs>
                <marker id="ah1" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto">
                  <path d="M0,0 L0,6 L7,3 z" fill="rgba(59,130,246,0.55)" />
                </marker>
                <marker id="ah2" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto">
                  <path d="M0,0 L0,6 L7,3 z" fill="rgba(6,182,212,0.55)" />
                </marker>
              </defs>
              {LANGGRAPH_EDGES.map((edge, i) => {
                const f = getNode(edge.from)
                const t = getNode(edge.to)
                if (!f || !t) return null
                const mx = (f.x + t.x) / 2
                const my = Math.min(f.y, t.y) - 28
                return (
                  <motion.path key={i}
                    d={`M ${f.x} ${f.y} Q ${mx} ${my} ${t.x} ${t.y}`}
                    fill="none"
                    stroke={i % 2 === 0 ? 'rgba(59,130,246,0.32)' : 'rgba(6,182,212,0.32)'}
                    strokeWidth="1.5"
                    markerEnd={i % 2 === 0 ? 'url(#ah1)' : 'url(#ah2)'}
                    strokeDasharray="6 4"
                    initial={{ pathLength: 0, opacity: 0 }}
                    animate={{ pathLength: 1, opacity: 1, strokeDashoffset: [0, -20] }}
                    transition={{
                      pathLength: { duration: 1.5, delay: i * 0.1 },
                      opacity: { duration: 0.5, delay: i * 0.1 },
                      strokeDashoffset: { duration: 1.5, repeat: Infinity, ease: 'linear' }
                    }}
                  />
                )
              })}
            </svg>
            {LANGGRAPH_NODES.map((node, i) => (
              <motion.div key={node.id}
                className="absolute flex flex-col items-center cursor-pointer"
                style={{ left: node.x - 40, top: node.y - 44, width: 80, zIndex: 1 }}
                initial={{ opacity: 0, scale: 0 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.09, type: 'spring', stiffness: 220 }}
                onMouseEnter={() => setActiveNode(node.id)}
                onMouseLeave={() => setActiveNode(null)}>
                <motion.div
                  className="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl border-2 transition-smooth"
                  style={{
                    background: `${node.color}14`,
                    borderColor: activeNode === node.id ? node.color : `${node.color}40`,
                  }}
                  animate={{
                    boxShadow: [`0 0 12px ${node.color}22`, `0 0 28px ${node.color}55`, `0 0 12px ${node.color}22`]
                  }}
                  transition={{ duration: 2.5, delay: i * 0.3, repeat: Infinity }}>
                  {node.icon}
                </motion.div>
                <span className="text-[10px] text-white/45 mt-1.5 text-center leading-tight font-medium px-1">{node.label}</span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}
