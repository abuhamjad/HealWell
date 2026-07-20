/**
 * Analysis service for health analysis operations.
 */

import { apiClient, API_ENDPOINTS, AnalysisRequest, AnalysisResponse } from '../api'

export const analysisService = {
  /**
   * Create a new health analysis.
   */
  async create(data: AnalysisRequest): Promise<AnalysisResponse> {
    const response = await apiClient.post(API_ENDPOINTS.ANALYSIS, data)
    return response.data
  },

  /**
   * Get analysis status/details.
   */
  async getDetails(analysisId: string): Promise<AnalysisResponse> {
    const response = await apiClient.get(`${API_ENDPOINTS.ANALYSIS}/${analysisId}`)
    return response.data
  },
}

export default analysisService
