import { apiRequest } from './api'

export type ApiReading = {
  id: number
  device_id: number
  timestamp: string
  temperature: number
  moisture: number
  ambient_temp: number
}

export type SensorReading = {
  entryId: number
  timestamp: string
  temperature: number
  moisture: number
  ambientTemp: number
}

export type SensorSnapshot = {
  temperature: number
  moisture: number
  ambientTemp: number
  lastUpdate: string
}

export type SensorChartSeries = {
  temperature: Array<{ time: string; value: number }>
  moisture: Array<{ time: string; value: number }>
  ambientTemp: Array<{ time: string; value: number }>
}

function getAccessTokenOrThrow() {
  const token = localStorage.getItem('accessToken')
  if (!token) {
    throw new Error('You must be logged in to read sensor data.')
  }

  return token
}

function mapReading(reading: ApiReading): SensorReading {
  return {
    entryId: reading.id,
    timestamp: reading.timestamp,
    temperature: reading.temperature,
    moisture: reading.moisture,
    ambientTemp: reading.ambient_temp
  }
}

export async function fetchLatestDeviceSnapshot(deviceId: number): Promise<SensorSnapshot> {
  const token = getAccessTokenOrThrow()
  const latest = await apiRequest<ApiReading>(`/devices/${deviceId}/readings/latest`, { token })

  return {
    temperature: latest.temperature,
    moisture: latest.moisture,
    ambientTemp: latest.ambient_temp,
    lastUpdate: latest.timestamp
  }
}

export async function fetchDeviceReadings(deviceId: number): Promise<SensorReading[]> {
  const token = getAccessTokenOrThrow()
  const readings = await apiRequest<ApiReading[]>(`/devices/${deviceId}/readings`, { token })
  return readings.map(mapReading)
}

export async function fetchHistoricalDeviceReadings(
  deviceId: number,
  limit = 20
): Promise<SensorReading[]> {
  const readings = await fetchDeviceReadings(deviceId)
  const safeLimit = Math.min(Math.max(limit, 1), 200)
  return readings.slice(0, safeLimit)
}

export const toChartSeries = (readings: SensorReading[]): SensorChartSeries => ({
  temperature: readings.map((reading) => ({
    time: reading.timestamp,
    value: reading.temperature
  })),
  moisture: readings.map((reading) => ({
    time: reading.timestamp,
    value: reading.moisture
  })),
  ambientTemp: readings.map((reading) => ({
    time: reading.timestamp,
    value: reading.ambientTemp
  }))
})
