/**
 * Centralized API endpoint definitions.
 */

export const API_ENDPOINTS = {
  // Health & Info
  ROOT: '/',
  HEALTH: '/health',

  // Analysis
  ANALYSIS: '/api/v1/analysis',
} as const

export default API_ENDPOINTS
