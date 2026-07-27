/**
 * Custom hook for finding nearby doctors.
 * Encapsulates API calls, loading state, and error handling.
 */

import { useState, useCallback } from 'react'
import { doctorService } from '../services'
import { Doctor } from '../api'

interface UseDoctorsState {
  doctors: Doctor[]
  loading: boolean
  error: string | null
}

export const useDoctors = () => {
  const [state, setState] = useState<UseDoctorsState>({
    doctors: [],
    loading: false,
    error: null,
  })

  const findNearby = useCallback(
    async (
      latitude?: number,
      longitude?: number,
      specialty?: string,
      radiusKm: number = 5.0
    ) => {
      setState({ doctors: [], loading: true, error: null })
      try {
        const response = await doctorService.findNearby(
          latitude,
          longitude,
          specialty,
          radiusKm
        )
        if (response.success && response.data) {
          setState({
            doctors: response.data.doctors,
            loading: false,
            error: null,
          })
          return response.data.doctors
        } else {
          setState({
            doctors: [],
            loading: false,
            error: response.message || 'Failed to find doctors',
          })
          throw new Error(response.message || 'Failed to find doctors')
        }
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : 'Failed to find doctors'
        setState({ doctors: [], loading: false, error: errorMessage })
        throw err
      }
    },
    []
  )

  const reset = useCallback(() => {
    setState({ doctors: [], loading: false, error: null })
  }, [])

  return {
    doctors: state.doctors,
    loading: state.loading,
    error: state.error,
    findNearby,
    reset,
  }
}

export default useDoctors
