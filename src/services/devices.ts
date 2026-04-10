import { apiRequest } from './api'

export type ApiDevice = {
  id: number
  device_name: string
  device_serial: string
  user_id: number
  last_seen: string | null
  is_online: boolean
  firmware_version: string | null
  created_at: string
  updated_at: string
}

export type ApiDeviceProvision = ApiDevice & {
  ingest_token: string
}

export type ApiDeviceIngestToken = {
  device_id: number
  device_serial: string
  ingest_token: string
  issued_at: string
}

export type FrontendDevice = {
  id: number
  name: string
  serial: string
  userId: number
  lastSeen: string | null
  isOnline: boolean
  firmwareVersion: string | null
  createdAt: string
  updatedAt: string
}

export type CreateDevicePayload = {
  deviceName: string
  deviceSerial: string
  firmwareVersion?: string
}

function getAccessTokenOrThrow() {
  const token = localStorage.getItem('accessToken')
  if (!token) {
    throw new Error('You must be logged in to manage devices.')
  }

  return token
}

export function toFrontendDevice(device: ApiDevice): FrontendDevice {
  return {
    id: device.id,
    name: device.device_name,
    serial: device.device_serial,
    userId: device.user_id,
    lastSeen: device.last_seen,
    isOnline: device.is_online,
    firmwareVersion: device.firmware_version,
    createdAt: device.created_at,
    updatedAt: device.updated_at
  }
}

export async function fetchMyDevices() {
  const token = getAccessTokenOrThrow()
  return apiRequest<ApiDevice[]>('/devices', { token })
}

export async function createMyDevice(payload: CreateDevicePayload) {
  const token = getAccessTokenOrThrow()
  return apiRequest<ApiDeviceProvision>('/devices', {
    method: 'POST',
    token,
    body: {
      device_name: payload.deviceName,
      device_serial: payload.deviceSerial,
      firmware_version: payload.firmwareVersion || null,
      is_online: false
    }
  })
}

export async function rotateMyDeviceIngestToken(deviceId: number) {
  const token = getAccessTokenOrThrow()
  return apiRequest<ApiDeviceIngestToken>(`/devices/${deviceId}/ingest-token`, {
    method: 'POST',
    token
  })
}
