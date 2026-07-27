/**
 * Centralized environment configuration.
 * Never access import.meta.env outside this file.
 */

const getEnvVariable = (key: string, defaultValue?: string): string => {
  const value = import.meta.env[`VITE_${key}`]
  if (!value && !defaultValue) {
    console.warn(`Environment variable VITE_${key} is not set`)
  }
  return value || defaultValue || ''
}

export const env = {
  // API Configuration
  API_BASE_URL: getEnvVariable('API_BASE_URL', 'http://127.0.0.1:8000'),

  // Application Environment
  ENVIRONMENT: getEnvVariable('ENVIRONMENT', 'development'),

  // Feature Flags
  DEBUG: getEnvVariable('DEBUG', 'true') === 'true',
} as const

export default env
