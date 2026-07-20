/**
 * Custom hook for medical history operations.
 * Encapsulates API calls, loading state, and error handling.
 */

import { useState, useCallback } from 'react'
import { historyService } from '../services'
import { HistoryItem, HistorySaveRequest } from '../api'

interface UseHistoryState {
  analyses: HistoryItem[]
  loading: boolean
  error: string | null
}

export const useHistory = () => {
  const [state, setState] = useState<UseHistoryState>({
    analyses: [],
    loading: false,
    error: null,
  })

  const getHistory = useCallback(async (userId?: string, limit: number = 20) => {
    setState({ analyses: [], loading: true, error: null })
    try {
      const response = await historyService.getHistory(userId, limit)
      if (response.success && response.data) {
        setState({
          analyses: response.data.analyses,
          loading: false,
          error: null,
        })
        return response.data.analyses
      } else {
        setState({
          analyses: [],
          loading: false,
          error: response.message || 'Failed to fetch history',
        })
        throw new Error(response.message || 'Failed to fetch history')
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Failed to fetch history'
      setState({ analyses: [], loading: false, error: errorMessage })
      throw err
    }
  }, [])

  const saveHistory = useCallback(async (data: HistorySaveRequest) => {
    setState(prev => ({ ...prev, loading: true, error: null }))
    try {
      const response = await historyService.saveHistory(data)
      if (response.success) {
        setState(prev => ({ ...prev, loading: false, error: null }))
        return response.data
      } else {
        setState(prev => ({
          ...prev,
          loading: false,
          error: response.message || 'Failed to save history',
        }))
        throw new Error(response.message || 'Failed to save history')
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Failed to save history'
      setState(prev => ({ ...prev, loading: false, error: errorMessage }))
      throw err
    }
  }, [])

  const reset = useCallback(() => {
    setState({ analyses: [], loading: false, error: null })
  }, [])

  return {
    analyses: state.analyses,
    loading: state.loading,
    error: state.error,
    getHistory,
    saveHistory,
    reset,
  }
}

export default useHistory
