import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Activity, Brain, Download, FileText,
  Heart, Mic, MicOff, Navigation, Phone, Search,
  Shield, User, AlertTriangle, CheckCircle, Clock,
  Network, Stethoscope, MapPin, X, Menu,
  ArrowRight, Sparkles, Eye, Calendar,
  TrendingUp, MessageSquare, RotateCcw,
  ChevronDown, Info, Loader2, Bot, History,
  Share2, ChevronLeft, Building2, Car
} from 'lucide-react'
import { AnalysisResult, Doctor, RiskLevel, AnalysisPhase } from '../types'
import { RiskBadge, StarRating } from '../components/RiskBadge'
import { useAnalysis } from '../hooks/useAnalysis'

const PROCESSING_STEPS = [
  { label: 'Understanding Symptoms', icon: Brain, color: '#3B82F6' },
  { label: 'Reading Medical History', icon: FileText, color: '#8B5CF6' },
  { label: 'Assessing Risk Level', icon: Activity, color: '#FACC15' },
  { label: 'Detecting Warning Signs', icon: AlertTriangle, color: '#EF4444' },
  { label: 'Selecting Specialist', icon: Stethoscope, color: '#22C55E' },
  { label: 'Finding Nearby Doctors', icon: MapPin, color: '#F97316' },
  { label: 'Generating Health Report', icon: FileText, color: '#A855F7' },
]

export function Analysis() {
  const { createAnalysis, loading: apiLoading, error: apiError } = useAnalysis()
  const [phase, setPhase] = useState<AnalysisPhase>('idle')
  const [currentStep, setCurrentStep] = useState(0)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [symptoms, setSymptoms] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  const [expandedAgent, setExpandedAgent] = useState<number | null>(null)
  const [formData, setFormData] = useState({
    name: '', age: '', gender: 'male', height: '', weight: '',
    diseases: '', medications: '', allergies: '',
    smoking: 'no', alcohol: 'no', exercise: 'moderate', stress: 'moderate',
  })

  const recRef = useRef<any>(null)

  const startRecording = useCallback(() => {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    if (!SR) { alert('Speech recognition not supported. Please use Chrome or Edge.'); return }
    const rec = new SR()
    rec.continuous = true
    rec.interimResults = true
    rec.lang = 'en-US'
    rec.onresult = (e: any) => {
      const text = Array.from(e.results).map((r: any) => r[0].transcript).join('')
      setSymptoms(text)
    }
    rec.start()
    recRef.current = rec
    setIsRecording(true)
  }, [])

  const stopRecording = useCallback(() => {
    recRef.current?.stop()
    setIsRecording(false)
  }, [])

  const runAnalysis = useCallback(async () => {
    if (!symptoms.trim()) return
    setPhase('processing')
    setCurrentStep(0)
    let step = 0
    const iv = setInterval(() => {
      step++
      setCurrentStep(step)
      if (step >= PROCESSING_STEPS.length - 1) {
        clearInterval(iv)
      }
    }, 680)

    try {
      const analysisData = await createAnalysis({ symptoms })

      if (analysisData) {
        const riskLevel = analysisData.risk_level as RiskLevel
        setResult({
          id: analysisData.analysis_id,
          date: new Date().toISOString().split('T')[0],
          symptoms,
          riskLevel,
          confidence: analysisData.confidence,
          summary: analysisData.summary_explanation,
          specialist: analysisData.specialist,
          specialistIcon: riskLevel === 'high' ? '🫀' : riskLevel === 'moderate' ? '⚠️' : '✓',
          emergency: analysisData.emergency,
          emergencyNote: analysisData.emergency_instructions || (analysisData.emergency ? 'Please seek emergency care immediately. Call 112.' : ''),
          homeCare: analysisData.personalized_home_care && analysisData.personalized_home_care.length > 0 ? analysisData.personalized_home_care : ['Care guidance pending'],
          lifestyle: analysisData.personalized_lifestyle && analysisData.personalized_lifestyle.length > 0 ? analysisData.personalized_lifestyle : ['Lifestyle guidance pending'],
          monitor: analysisData.monitoring_guidance && analysisData.monitoring_guidance.length > 0 ? analysisData.monitoring_guidance : ['Monitor your condition'],
          nearbyDoctors: [],
          agentOutputs: [
            { agent: 'API Analysis', icon: '🔬', status: 'complete', output: `Analysis complete. Risk: ${riskLevel}`, time: '1.5s' },
          ],
          confidenceExplanation: analysisData.confidence_explanation,
          riskExplanation: analysisData.risk_explanation,
          specialistExplanation: analysisData.specialist_explanation,
        } as any)
      }

      setPhase('complete')
    } catch (error) {
      console.error('Analysis error:', error)
      alert('Failed to complete analysis. Please try again.')
      setPhase('idle')
    }
  }, [symptoms, createAnalysis])

  const clearAll = () => { setPhase('idle'); setResult(null); setSymptoms(''); setCurrentStep(0) }

  return (
    <div className="min-h-screen pt-28 pb-20">
      <div className="max-w-6xl mx-auto px-4">
        {phase === 'idle' && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <div className="text-center mb-12">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-blue-400/25 text-blue-400 text-sm font-medium mb-6">
                <Brain size={14} /> AI Health Analysis
              </div>
              <h1 className="text-4xl font-bold mb-4" style={{ fontFamily: 'Manrope, sans-serif' }}>
                Tell us how you&apos;re <span className="gradient-text">feeling today</span>
              </h1>
              <p className="max-w-lg mx-auto text-sm leading-relaxed" style={{ color: 'rgba(255,255,255,0.48)' }}>
                Fill in your details and describe your symptoms in natural language.
                Our 9-agent LangGraph system will analyze your health in real time.
              </p>
            </div>

            <div className="grid lg:grid-cols-[360px_1fr] gap-6">
              <div className="space-y-4">
                <div className="glass rounded-2xl p-5">
                  <div className="flex items-center gap-2 mb-4">
                    <User size={15} className="text-blue-400" />
                    <span className="font-semibold text-sm" style={{ color: 'rgba(255,255,255,0.75)' }}>Patient Information</span>
                  </div>
                  <div className="space-y-3">
                    {[
                      { key: 'name', label: 'Full Name', placeholder: 'John Doe', type: 'text' },
                      { key: 'age', label: 'Age', placeholder: '28', type: 'number' },
                      { key: 'height', label: 'Height (cm)', placeholder: '175', type: 'number' },
                      { key: 'weight', label: 'Weight (kg)', placeholder: '72', type: 'number' },
                    ].map(f => (
                      <div key={f.key}>
                        <label className="text-[11px] font-medium mb-1.5 block" style={{ color: 'rgba(255,255,255,0.35)' }}>{f.label}</label>
                        <input type={f.type} placeholder={f.placeholder}
                          value={(formData as any)[f.key]}
                          onChange={e => setFormData(d => ({ ...d, [f.key]: e.target.value }))}
                          className="w-full glass rounded-xl px-3 py-2 text-sm text-white placeholder-white/20 outline-none border border-white/08 focus:border-blue-400/40 bg-transparent transition-smooth" />
                      </div>
                    ))}
                    <div>
                      <label className="text-[11px] font-medium mb-1.5 block" style={{ color: 'rgba(255,255,255,0.35)' }}>Gender</label>
                      <select value={formData.gender} onChange={e => setFormData(d => ({ ...d, gender: e.target.value }))}
                        className="w-full glass rounded-xl px-3 py-2 text-sm text-white bg-[#0B0B0B] outline-none border border-white/08 focus:border-blue-400/40 transition-smooth">
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                      </select>
                    </div>
                  </div>
                </div>

                <div className="glass rounded-2xl p-5">
                  <div className="flex items-center gap-2 mb-4">
                    <FileText size={15} className="text-purple-400" />
                    <span className="font-semibold text-sm" style={{ color: 'rgba(255,255,255,0.75)' }}>Medical History</span>
                  </div>
                  <div className="space-y-3">
                    {[
                      { key: 'diseases', label: 'Existing Conditions', placeholder: 'Diabetes, Hypertension...' },
                      { key: 'medications', label: 'Current Medications', placeholder: 'Metformin 500mg...' },
                      { key: 'allergies', label: 'Known Allergies', placeholder: 'Penicillin, Latex...' },
                    ].map(f => (
                      <div key={f.key}>
                        <label className="text-[11px] font-medium mb-1.5 block" style={{ color: 'rgba(255,255,255,0.35)' }}>{f.label}</label>
                        <input type="text" placeholder={f.placeholder}
                          value={(formData as any)[f.key]}
                          onChange={e => setFormData(d => ({ ...d, [f.key]: e.target.value }))}
                          className="w-full glass rounded-xl px-3 py-2 text-sm text-white placeholder-white/20 outline-none border border-white/08 focus:border-purple-400/40 bg-transparent transition-smooth" />
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex flex-col">
                <div className="glass rounded-2xl p-6 flex-1 flex flex-col">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <MessageSquare size={15} className="text-cyan-400" />
                      <span className="font-semibold text-sm" style={{ color: 'rgba(255,255,255,0.75)' }}>Describe Your Symptoms</span>
                    </div>
                    <span className="text-[11px] font-mono" style={{ color: 'rgba(255,255,255,0.28)' }}>{symptoms.length} chars</span>
                  </div>

                  <textarea value={symptoms} onChange={e => setSymptoms(e.target.value)}
                    placeholder={"Describe your symptoms..."}
                    className="flex-1 bg-transparent text-white/82 placeholder-white/18 resize-none outline-none text-sm leading-relaxed min-h-[300px]"
                    style={{ fontFamily: 'Inter, sans-serif' }} />

                  <div className="flex items-center justify-between mt-5 pt-4 border-t border-white/06">
                    <div className="flex items-center gap-2">
                      <button onClick={isRecording ? stopRecording : startRecording}
                        className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-smooth border ${isRecording ? 'bg-red-500/18 border-red-400/45 text-red-300' : 'btn-ghost'}`}>
                        {isRecording ? <MicOff size={15} /> : <Mic size={15} />}
                        {isRecording ? 'Stop' : 'Voice Input'}
                      </button>
                      <button onClick={clearAll} className="btn-ghost flex items-center gap-1.5 px-3 py-2 rounded-xl text-sm">
                        <RotateCcw size={14} /> Clear
                      </button>
                    </div>
                    <button onClick={runAnalysis} disabled={!symptoms.trim()}
                      className={`btn-primary flex items-center gap-2 px-6 py-2.5 rounded-xl text-sm font-semibold ${!symptoms.trim() ? 'opacity-40 cursor-not-allowed' : ''}`}>
                      <Bot size={16} /> Analyze with AI <ArrowRight size={14} />
                    </button>
                  </div>
                </div>

                <div className="glass rounded-xl p-4 mt-3 flex items-start gap-3">
                  <Info size={14} className="text-yellow-400 mt-0.5 flex-shrink-0" />
                  <p className="text-xs leading-relaxed" style={{ color: 'rgba(255,255,255,0.38)' }}>
                    <span className="text-yellow-400 font-medium">Not a medical diagnosis.</span> HealWell provides general health guidance only.
                    Always consult a qualified healthcare professional for medical decisions.
                    In emergencies, call 112 immediately.
                  </p>
                </div>

                {apiError && (
                  <div className="glass rounded-xl p-4 mt-3 flex items-start gap-3 border border-red-400/30 bg-red-400/08">
                    <AlertTriangle size={14} className="text-red-400 mt-0.5 flex-shrink-0" />
                    <p className="text-xs leading-relaxed text-red-400">{apiError}</p>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}

        {phase === 'processing' && (
          <motion.div initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.96 }} className="max-w-md mx-auto text-center py-16">
            <div className="relative flex items-center justify-center mb-10">
              <div className="relative w-20 h-20 rounded-full glass-strong border border-blue-400/45 flex items-center justify-center animate-glow-pulse z-10">
                <motion.div animate={{ rotate: 360 }} transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}>
                  <Brain size={32} className="text-blue-400" />
                </motion.div>
              </div>
            </div>

            <h2 className="text-2xl font-bold mb-2" style={{ fontFamily: 'Manrope, sans-serif' }}>
              Analyzing your symptoms
            </h2>
            <p className="text-sm mb-10" style={{ color: 'rgba(255,255,255,0.42)' }}>
              LangGraph agents are processing your health data...
            </p>

            <div className="space-y-2.5 text-left">
              {PROCESSING_STEPS.map((step, i) => {
                const state = i < currentStep ? 'done' : i === currentStep ? 'active' : 'pending'
                return (
                  <motion.div key={step.label}
                    initial={{ opacity: 0, x: -16 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }}
                    className={`flex items-center gap-3 p-3 rounded-xl transition-smooth ${state === 'active' ? 'glass border border-blue-400/30' : state === 'done' ? 'opacity-55' : 'opacity-22'}`}>
                    <div className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                      style={{
                        background: state === 'done' ? 'rgba(34,197,94,0.14)' : state === 'active' ? `${step.color}18` : 'rgba(255,255,255,0.04)',
                        border: `1px solid ${state === 'done' ? 'rgba(34,197,94,0.38)' : state === 'active' ? `${step.color}48` : 'rgba(255,255,255,0.08)'}`
                      }}>
                      {state === 'done' ? <CheckCircle size={15} className="text-emerald-400" />
                        : state === 'active'
                          ? <motion.div animate={{ rotate: 360 }} transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}>
                            <Loader2 size={15} style={{ color: step.color }} />
                          </motion.div>
                          : <step.icon size={15} className="text-white/25" />}
                    </div>
                    <span className={`text-sm font-medium ${state === 'active' ? 'text-white' : 'text-white/48'}`}>{step.label}</span>
                  </motion.div>
                )
              })}
            </div>
          </motion.div>
        )}

        {phase === 'complete' && result && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <div className="flex items-center justify-between mb-8">
              <button onClick={clearAll} className="btn-ghost flex items-center gap-2 px-4 py-2 rounded-xl text-sm">
                <ChevronLeft size={16} /> New Analysis
              </button>
              <button className="btn-primary flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold">
                <Download size={14} /> Download PDF
              </button>
            </div>

            {result.emergency && (
              <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
                className="glass rounded-2xl p-5 border border-red-500/48 bg-red-500/08 mb-6 flex items-start gap-4">
                <AlertTriangle size={20} className="text-red-400 flex-shrink-0" />
                <div className="flex-1">
                  <div className="font-bold text-red-400 mb-1">Emergency Warning Detected</div>
                  <div className="text-sm" style={{ color: 'rgba(255,255,255,0.65)' }}>{result.emergencyNote}</div>
                </div>
              </motion.div>
            )}

            <div className="grid md:grid-cols-3 gap-4 mb-6">
              <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
                className="glass rounded-2xl p-5">
                <div className="text-xs font-medium mb-3" style={{ color: 'rgba(255,255,255,0.38)' }}>Risk Level</div>
                <RiskBadge level={result.riskLevel} />
              </motion.div>

              <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}
                className="glass rounded-2xl p-5 flex flex-col">
                <div className="text-xs font-medium mb-2" style={{ color: 'rgba(255,255,255,0.38)' }}>AI Confidence</div>
                <div className="text-xl font-bold gradient-text mb-3" style={{ fontFamily: 'Manrope, sans-serif' }}>{result.confidence}%</div>
                <div className="text-xs leading-relaxed" style={{ color: 'rgba(255,255,255,0.48)' }}>
                  {(result as any).confidenceExplanation || 'Confidence assessment completed.'}
                </div>
              </motion.div>

              <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
                className="glass rounded-2xl p-5">
                <div className="text-xs font-medium mb-3" style={{ color: 'rgba(255,255,255,0.38)' }}>Specialist</div>
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-3xl">{result.specialistIcon}</span>
                  <div className="font-semibold text-white text-sm">{result.specialist}</div>
                </div>
                <div className="text-xs leading-relaxed" style={{ color: 'rgba(255,255,255,0.48)' }}>
                  {(result as any).specialistExplanation || 'Specialist recommendation completed.'}
                </div>
              </motion.div>
            </div>

            <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}
              className="glass rounded-2xl p-6 mb-6">
              <div className="font-semibold text-sm mb-3" style={{ color: 'rgba(255,255,255,0.75)' }}>AI Summary</div>
              <p className="text-sm leading-relaxed" style={{ color: 'rgba(255,255,255,0.65)' }}>{result.summary}</p>
            </motion.div>

            <div className="grid md:grid-cols-3 gap-4 mb-6">
              {[
                { title: 'Home-Care', icon: Heart, color: '#22C55E', items: result.homeCare },
                { title: 'Lifestyle', icon: TrendingUp, color: '#3B82F6', items: result.lifestyle },
                { title: 'Monitor', icon: Eye, color: '#FACC15', items: result.monitor },
              ].map((col, ci) => (
                <motion.div key={col.title} initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 + ci * 0.1 }}
                  className="glass rounded-2xl p-5">
                  <div className="flex items-center gap-2 mb-4">
                    <col.icon size={14} style={{ color: col.color }} />
                    <span className="font-semibold text-sm" style={{ color: 'rgba(255,255,255,0.75)' }}>{col.title}</span>
                  </div>
                  <ul className="space-y-2">
                    {col.items.map((item, ii) => (
                      <li key={ii} className="flex items-start gap-2 text-xs leading-snug" style={{ color: 'rgba(255,255,255,0.55)' }}>
                        <span className="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0" style={{ background: col.color, opacity: 0.65 }} />
                        {item}
                      </li>
                    ))}
                  </ul>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}
