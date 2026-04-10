import { apiRequest } from './api'

export type ApiAlertSeverity = 'info' | 'warning' | 'critical'

export type ApiAlert = {
  id: number
  device_id: number
  user_id: number
  type: string
  severity: ApiAlertSeverity
  message: string
  resolved: boolean
  created_at: string
  resolved_at: string | null
}

function getAccessTokenOrThrow() {
  const token = localStorage.getItem('accessToken')
  if (!token) {
    throw new Error('You must be logged in to read alerts.')
  }

  return token
}

export async function fetchDeviceAlerts(deviceId: number, resolved?: boolean) {
  const token = getAccessTokenOrThrow()
  const query = typeof resolved === 'boolean' ? `?resolved=${resolved}` : ''
  return apiRequest<ApiAlert[]>(`/devices/${deviceId}/alerts${query}`, { token })
}
