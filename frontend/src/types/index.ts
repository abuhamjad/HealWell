export type Page = 'home' | 'analysis' | 'history'
export type RiskLevel = 'low' | 'moderate' | 'high'
export type AnalysisPhase = 'idle' | 'processing' | 'complete'

export interface AnalysisResult {
  id: string
  date: string
  symptoms: string
  riskLevel: RiskLevel
  confidence: number
  summary: string
  specialist: string
  specialistIcon: string
  emergency: boolean
  emergencyNote: string
  homeCare: string[]
  lifestyle: string[]
  monitor: string[]
  nearbyDoctors: Doctor[]
  agentOutputs: AgentOutput[]
}

export interface Doctor {
  name: string
  hospital: string
  distance: string
  rating: number
  specialty: string
  available: boolean
}

export interface AgentOutput {
  agent: string
  icon: string
  status: 'complete' | 'processing' | 'pending'
  output: string
  time: string
}
