/**
 * API request and response type definitions.
 */

export interface ErrorDetail {
  field: string
  message: string
}

export interface ApiResponse<T = unknown> {
  success: boolean
  message: string
  data: T | null
  errors: ErrorDetail[] | null
}

// Analysis Types
export interface AnalysisRequest {
  symptoms: string
}

// Nested AI output models
export interface RiskAssessment {
  risk_level: string
  confidence: number
  reasoning: string
  warning_signs: string[]
}

export interface SpecialistRecommendation {
  specialist: string
  reasoning: string
  urgency: string
}

export interface HealthReport {
  summary: string
  home_care: string[]
  lifestyle: string[]
  monitoring: string[]
  references: string[]
}

// Analysis response with both flat fields (backward compatibility) and nested AI outputs
export interface AnalysisData {
  analysis_id: string
  risk_level: 'low' | 'moderate' | 'high'
  confidence: number
  specialist: string
  emergency: boolean
  status?: string
  emergency_message?: string
  risk_assessment: RiskAssessment
  specialist_recommendation: SpecialistRecommendation
  health_report: HealthReport
}

export interface AnalysisResponse extends ApiResponse<AnalysisData> {}

// Health Check Types
export interface HealthCheckData {
  api: string
  version: string
  status: string
}

export interface HealthCheckResponse extends ApiResponse<HealthCheckData> {}
