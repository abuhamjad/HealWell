/**
 * Centralized API endpoint definitions.
 */

export const API_ENDPOINTS = {
  // Health & Info
  ROOT: '/',
  HEALTH: '/health',

  // Analysis
  ANALYSIS: '/api/v1/analysis',

  // History
  HISTORY: '/api/v1/history',

  // Doctors
  DOCTORS: '/api/v1/doctors',
} as const

export default API_ENDPOINTS
