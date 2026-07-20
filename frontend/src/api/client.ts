/**
 * Axios HTTP client configured for HealWell API.
 */

import axios, { AxiosInstance, AxiosError } from 'axios'
import { env } from '../config'
import { ApiResponse } from './types'

// Create Axios instance
export const apiClient: AxiosInstance = axios.create({
  baseURL: env.API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    if (env.DEBUG) {
      console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
    }
    return config
  },
  (error) => {
    console.error('[API] Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    if (env.DEBUG) {
      console.log(`[API] Response:`, response.data)
    }
    return response
  },
  (error: AxiosError<ApiResponse>) => {
    console.error('[API] Response error:', error)
    return Promise.reject(error)
  }
)

export default apiClient
