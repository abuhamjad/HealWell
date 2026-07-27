import { useState, useCallback, useRef } from 'react'
import { motion } from 'framer-motion'
import {
  Activity, Brain, Download, FileText,
  Heart, Mic, MicOff, AlertTriangle, CheckCircle,
  Stethoscope, ArrowRight, Eye,
  TrendingUp, MessageSquare, RotateCcw,
  Info, Loader2, Bot, ChevronLeft
} from 'lucide-react'
import { AnalysisResult, RiskLevel, AnalysisPhase } from '../types'
import { RiskBadge } from '../components/RiskBadge'
import { useAnalysis } from '../hooks/useAnalysis'

interface SpeechRecognitionInstance {
  continuous: boolean
  interimResults: boolean
  lang: string
  onresult: (event: Event) => void
  start(): void
  stop(): void
}

const PROCESSING_STEPS = [
  { label: 'Understanding Symptoms', icon: Brain, color: '#3B82F6' },
  { label: 'Assessing Risk Level', icon: Activity, color: '#FACC15' },
  { label: 'Detecting Warning Signs', icon: AlertTriangle, color: '#EF4444' },
  { label: 'Selecting Specialist', icon: Stethoscope, color: '#22C55E' },
  { label: 'Generating Health Report', icon: FileText, color: '#A855F7' },
]

export function Analysis() {
  const { createAnalysis, error: apiError } = useAnalysis()
  const [phase, setPhase] = useState<AnalysisPhase>('idle')
  const [currentStep, setCurrentStep] = useState(0)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [symptoms, setSymptoms] = useState('')
  const [isRecording, setIsRecording] = useState(false)

  const recRef = useRef<SpeechRecognitionInstance | null>(null)

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
          summary: analysisData?.health_report?.summary ?? `Analysis received: Risk level is ${riskLevel}. Specialist recommended: ${analysisData.specialist}`,
          specialist: analysisData.specialist,
          specialistIcon: riskLevel === 'high' ? '🫀' : riskLevel === 'moderate' ? '⚠️' : '✓',
          emergency: analysisData.emergency,
          emergencyNote: analysisData?.emergency_message ?? (analysisData.emergency ? 'Please seek emergency care immediately. Call 112.' : ''),
          homeCare: (analysisData?.health_report?.home_care?.length) ? analysisData.health_report.home_care : ['Rest adequately', 'Stay well-hydrated', 'Monitor symptoms', 'Follow specialist recommendations'],
          lifestyle: (analysisData?.health_report?.lifestyle?.length) ? analysisData.health_report.lifestyle : ['Maintain healthy habits', 'Manage stress', 'Regular exercise', 'Adequate sleep'],
          monitor: (analysisData?.health_report?.monitoring?.length) ? analysisData.health_report.monitoring : ['Symptom progression', 'Any new symptoms', 'Severity changes', 'Follow-up care'],
          agentOutputs: [
            {
              agent: 'Risk Assessment',
              icon: '⚠️',
              status: 'complete',
              output: analysisData?.risk_assessment?.reasoning ?? 'Risk assessment completed',
              time: 'Completed',
            },
            {
              agent: 'Specialist Recommendation',
              icon: '👨‍⚕️',
              status: 'complete',
              output: analysisData?.specialist_recommendation?.reasoning
                ? analysisData.specialist_recommendation.urgency
                  ? `${analysisData.specialist_recommendation.reasoning}\n\nUrgency: ${analysisData.specialist_recommendation.urgency}`
                  : analysisData.specialist_recommendation.reasoning
                : 'Specialist recommendation completed',
              time: 'Completed',
            },
            {
              agent: 'Health Report',
              icon: '📋',
              status: 'complete',
              output: analysisData?.health_report?.summary ?? 'Health report generated',
              time: 'Completed',
            },
          ],
          warningSigns: analysisData?.risk_assessment?.warning_signs ?? [],
          references: analysisData?.health_report?.references ?? [],
        })
      }

      setPhase('complete')
    } catch (error) {
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
            <div className="text-center mb-16">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-blue-400/25 text-blue-400 text-sm font-medium mb-6">
                <Brain size={14} /> AI Health Analysis
              </div>
              <h1 className="text-4xl font-bold mb-4" style={{ fontFamily: 'Manrope, sans-serif' }}>
                Tell us how you&apos;re <span className="gradient-text">feeling today</span>
              </h1>
              <p className="max-w-lg mx-auto text-sm leading-relaxed" style={{ color: 'rgba(255,255,255,0.48)' }}>
                Fill in your details and describe your symptoms in natural language.
                Our AI health analysis system will assess your condition in real time.
              </p>
            </div>

            <div className="flex flex-col lg:max-w-2xl mx-auto">
                <div className="glass rounded-2xl p-6 flex-1 flex flex-col">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <MessageSquare size={15} className="text-cyan-400" />
                      <span className="font-semibold text-sm" style={{ color: 'rgba(255,255,255,0.75)' }}>Describe Your Symptoms</span>
                    </div>
                    <span className="text-[11px] font-mono" style={{ color: 'rgba(255,255,255,0.28)' }}>{symptoms.length} chars</span>
                  </div>

                  <textarea value={symptoms} onChange={e => setSymptoms(e.target.value)}
                    placeholder={"Describe your symptoms...\n\nExamples:\n• Fever with sore throat for 3 days\n• Persistent headache and dizziness\n• Chest pain after exercise\n• Dry cough and fatigue\n• Stomach pain after meals"}
                    className="flex-1 bg-transparent text-white/82 placeholder-white/18 resize-none outline-none text-sm leading-relaxed min-h-[300px] border border-white/08 rounded-xl p-3 focus:border-cyan-400/40 transition-smooth"
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
                  <Info size={14} className="text-yellow-400 mt-0.5 shrink-0" />
                  <p className="text-xs leading-relaxed" style={{ color: 'rgba(255,255,255,0.38)' }}>
                    <span className="text-yellow-400 font-medium">Not a medical diagnosis.</span> HealWell provides general health guidance only.
                    Always consult a qualified healthcare professional for medical decisions.
                    In emergencies, call 112 immediately.
                  </p>
                </div>

                {apiError && (
                  <div className="glass rounded-xl p-4 mt-3 flex items-start gap-3 border border-red-400/30 bg-red-400/08">
                    <AlertTriangle size={14} className="text-red-400 mt-0.5 shrink-0" />
                    <p className="text-xs leading-relaxed text-red-400">{apiError}</p>
                  </div>
                )}
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
                    <div className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0"
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
                <AlertTriangle size={20} className="text-red-400 shrink-0" />
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
                className="glass rounded-2xl p-5 flex flex-col items-center justify-center">
                <div className="text-xs font-medium mb-3" style={{ color: 'rgba(255,255,255,0.38)' }}>AI Confidence</div>
                <div className="text-xl font-bold gradient-text" style={{ fontFamily: 'Manrope, sans-serif' }}>{result.confidence}%</div>
              </motion.div>

              <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
                className="glass rounded-2xl p-5">
                <div className="text-xs font-medium mb-3" style={{ color: 'rgba(255,255,255,0.38)' }}>Specialist</div>
                <div className="flex items-center gap-3">
                  <span className="text-3xl">{result.specialistIcon}</span>
                  <div className="font-semibold text-white text-sm">{result.specialist}</div>
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
                        <span className="w-1.5 h-1.5 rounded-full mt-1.5 shrink-0" style={{ background: col.color, opacity: 0.65 }} />
                        {item}
                      </li>
                    ))}
                  </ul>
                </motion.div>
              ))}
            </div>

            {result.warningSigns?.length > 0 && (
              <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.65 }}
                className="glass rounded-2xl p-5 mb-6">
                <div className="flex items-center gap-2 mb-4">
                  <AlertTriangle size={14} style={{ color: '#EF4444' }} />
                  <span className="font-semibold text-sm" style={{ color: 'rgba(255,255,255,0.75)' }}>Warning Signs</span>
                </div>
                <ul className="space-y-2">
                  {result.warningSigns.map((sign, i) => (
                    <li key={i} className="flex items-start gap-2 text-xs leading-snug" style={{ color: 'rgba(255,255,255,0.55)' }}>
                      <span className="w-1.5 h-1.5 rounded-full mt-1.5 shrink-0" style={{ background: '#EF4444', opacity: 0.65 }} />
                      {sign}
                    </li>
                  ))}
                </ul>
              </motion.div>
            )}

            {result.references?.length > 0 && (
              <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.75 }}
                className="glass rounded-2xl p-5">
                <div className="flex items-center gap-2 mb-4">
                  <FileText size={14} style={{ color: '#8B5CF6' }} />
                  <span className="font-semibold text-sm" style={{ color: 'rgba(255,255,255,0.75)' }}>Medical References</span>
                </div>
                <ul className="space-y-2">
                  {result.references.map((ref, i) => (
                    <li key={i} className="flex items-start gap-2 text-xs leading-snug" style={{ color: 'rgba(255,255,255,0.55)' }}>
                      <span className="w-1.5 h-1.5 rounded-full mt-1.5 shrink-0" style={{ background: '#8B5CF6', opacity: 0.65 }} />
                      {ref}
                    </li>
                  ))}
                </ul>
              </motion.div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  )
}
