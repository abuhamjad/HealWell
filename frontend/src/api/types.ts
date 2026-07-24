/**
 * API request and response type definitions.
 */

export interface ErrorDetail {
  field: string
  message: string
}

export interface ApiResponse<T = any> {
  success: boolean
  message: string
  data: T | null
  errors: ErrorDetail[] | null
}

// Analysis Types
export interface AnalysisRequest {
  symptoms: string
  user_id?: string
}

export interface AnalysisData {
  analysis_id: string
  risk_level: 'low' | 'moderate' | 'high'
  confidence: number
  confidence_explanation: string
  risk_explanation: string
  specialist: string
  specialist_explanation: string
  emergency: boolean
  emergency_instructions?: string | null
  summary_explanation: string
  personalized_home_care: string[]
  personalized_lifestyle: string[]
  monitoring_guidance: string[]
  status?: string
}

export interface AnalysisResponse extends ApiResponse<AnalysisData> {}

// History Types
export interface HistoryItem {
  id: string
  user_id: string
  date: string
  symptoms: string
  risk_level: string
  specialist: string
}

export interface HistoryData {
  analyses: HistoryItem[]
  count: number
}

export interface HistoryResponse extends ApiResponse<HistoryData> {}

export interface HistorySaveRequest {
  user_id: string
  conditions?: string[]
  medications?: string[]
  allergies?: string[]
}

export interface HistorySaveData {
  history_id: string
  user_id: string
  saved_at: string
}

export interface HistorySaveResponse extends ApiResponse<HistorySaveData> {}

// Doctor Types
export interface Doctor {
  id: string
  name: string
  specialty: string
  hospital: string
  distance: string
  rating: number
  available: boolean
}

export interface DoctorsData {
  doctors: Doctor[]
  count: number
}

export interface DoctorsResponse extends ApiResponse<DoctorsData> {}

// Health Check Types
export interface HealthCheckData {
  api: string
  version: string
  status: string
}

export interface HealthCheckResponse extends ApiResponse<HealthCheckData> {}
