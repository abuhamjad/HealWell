/**
 * Custom hook for health analysis operations.
 * Encapsulates API calls, loading state, and error handling.
 */

import { useState, useCallback } from 'react'
import { analysisService } from '../services'
import { AnalysisRequest, AnalysisData, ApiResponse } from '../api'

interface UseAnalysisState {
  data: AnalysisData | null
  loading: boolean
  error: string | null
}

export const useAnalysis = () => {
  const [state, setState] = useState<UseAnalysisState>({
    data: null,
    loading: false,
    error: null,
  })

  const createAnalysis = useCallback(async (request: AnalysisRequest) => {
    setState({ data: null, loading: true, error: null })
    try {
      const response = await analysisService.create(request)
      if (response.success && response.data) {
        setState({ data: response.data, loading: false, error: null })
        return response.data
      } else {
        setState({
          data: null,
          loading: false,
          error: response.message || 'Analysis failed',
        })
        throw new Error(response.message || 'Analysis failed')
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Failed to create analysis'
      setState({ data: null, loading: false, error: errorMessage })
      throw err
    }
  }, [])

  const reset = useCallback(() => {
    setState({ data: null, loading: false, error: null })
  }, [])

  return {
    data: state.data,
    loading: state.loading,
    error: state.error,
    createAnalysis,
    reset,
  }
}

export default useAnalysis
