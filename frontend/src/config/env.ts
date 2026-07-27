/**
 * Centralized environment configuration.
 * Never access import.meta.env outside this file.
 */

const getEnvVariable = (key: string, defaultValue?: string): string => {
  const value = import.meta.env[`VITE_${key}`]
  return value || defaultValue || ''
}

export const env = {
  // API Configuration
  API_BASE_URL: getEnvVariable('API_BASE_URL', 'http://127.0.0.1:8000'),

  // Application Environment
  ENVIRONMENT: getEnvVariable('ENVIRONMENT', 'development'),
} as const

export default env
