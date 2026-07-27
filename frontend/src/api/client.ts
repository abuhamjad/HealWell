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
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error: AxiosError<ApiResponse>) => {
    return Promise.reject(error)
  }
)

export default apiClient
