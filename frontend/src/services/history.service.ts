/**
 * History service for medical history operations.
 */

import {
  apiClient,
  API_ENDPOINTS,
  HistoryResponse,
  HistorySaveRequest,
  HistorySaveResponse,
} from '../api'

export const historyService = {
  /**
   * Get user's analysis history.
   */
  async getHistory(userId?: string, limit: number = 20): Promise<HistoryResponse> {
    const response = await apiClient.get(API_ENDPOINTS.HISTORY, {
      params: {
        user_id: userId,
        limit,
      },
    })
    return response.data
  },

  /**
   * Save or update user medical history.
   */
  async saveHistory(data: HistorySaveRequest): Promise<HistorySaveResponse> {
    const response = await apiClient.post(API_ENDPOINTS.HISTORY, data)
    return response.data
  },
}

export default historyService
