export type Page = 'home' | 'analysis'
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
  agentOutputs: AgentOutput[]
  warningSigns?: string[]
  references?: string[]
}

export interface AgentOutput {
  agent: string
  icon: string
  status: 'complete' | 'processing' | 'pending'
  output: string
  time: string
}
