/**
 * Doctor service for finding nearby healthcare providers.
 */

import { apiClient, API_ENDPOINTS, DoctorsResponse } from '../api'

export const doctorService = {
  /**
   * Find nearby doctors/healthcare providers.
   */
  async findNearby(
    latitude?: number,
    longitude?: number,
    specialty?: string,
    radiusKm: number = 5.0
  ): Promise<DoctorsResponse> {
    const response = await apiClient.get(API_ENDPOINTS.DOCTORS, {
      params: {
        latitude,
        longitude,
        specialty,
        radius_km: radiusKm,
      },
    })
    return response.data
  },
}

export default doctorService
