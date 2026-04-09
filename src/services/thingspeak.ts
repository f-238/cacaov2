export type SensorReading = {
  entryId: number
  timestamp: string
  temperature: number | null
  moisture: number | null
  ambientTemp: number | null
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

type ThingSpeakFeed = {
  created_at: string
  entry_id: number
  field1?: string | null
  field2?: string | null
  field3?: string | null
  field4?: string | null
}

type ThingSpeakFeedsResponse = {
  feeds: ThingSpeakFeed[]
}

const THINGSPEAK_BASE_URL = 'https://api.thingspeak.com'
const THINGSPEAK_CHANNEL_ID = import.meta.env.VITE_THINGSPEAK_CHANNEL_ID?.trim()
const THINGSPEAK_READ_API_KEY = import.meta.env.VITE_THINGSPEAK_READ_API_KEY?.trim()
const FEED_LIMIT = 8000

const parseFieldNumber = (value?: string | null) => {
  if (value == null || value === '') {
    return null
  }

  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : null
}

const getAmbientTemp = (feed: ThingSpeakFeed) => {
  const secondaryTemp = parseFieldNumber(feed.field2)
  const tertiaryTemp = parseFieldNumber(feed.field3)

  if (secondaryTemp !== null && tertiaryTemp !== null) {
    return Number(((secondaryTemp + tertiaryTemp) / 2).toFixed(1))
  }

  return secondaryTemp ?? tertiaryTemp
}

const mapFeedToReading = (feed: ThingSpeakFeed): SensorReading => ({
  entryId: feed.entry_id,
  timestamp: feed.created_at,
  temperature: parseFieldNumber(feed.field1),
  moisture: parseFieldNumber(feed.field4),
  ambientTemp: getAmbientTemp(feed)
})

const fetchFeeds = async (params: Record<string, string>) => {
  const requestUrl = new URL(`${THINGSPEAK_BASE_URL}/channels/${THINGSPEAK_CHANNEL_ID}/feeds.json`)
  requestUrl.searchParams.set('api_key', THINGSPEAK_READ_API_KEY)

  Object.entries(params).forEach(([key, value]) => {
    requestUrl.searchParams.set(key, value)
  })

  const response = await fetch(requestUrl.toString())

  if (!response.ok) {
    throw new Error(`ThingSpeak request failed with status ${response.status}.`)
  }

  const payload = (await response.json()) as ThingSpeakFeedsResponse
  return payload.feeds.map(mapFeedToReading)
}

const coerceSnapshotValue = (value: number | null, fallback: number) => value ?? fallback

export const fetchLatestSensorSnapshot = async (): Promise<SensorSnapshot> => {
  const readings = await fetchFeeds({ results: '1' })
  const latest = readings[0]

  if (!latest) {
    throw new Error('ThingSpeak returned no sensor readings.')
  }

  return {
    temperature: coerceSnapshotValue(latest.temperature, 0),
    moisture: coerceSnapshotValue(latest.moisture, 0),
    ambientTemp: coerceSnapshotValue(latest.ambientTemp, 0),
    lastUpdate: latest.timestamp
  }
}

export const fetchHistoricalSensorReadings = async (limit = 20): Promise<SensorReading[]> => {
  const safeLimit = Math.min(Math.max(limit, 1), 50)
  return fetchFeeds({ results: String(safeLimit) })
}

const formatThingSpeakDate = (value: Date) => value.toISOString().replace('T', ' ').replace('.000Z', '')

const fetchFeedsInRange = async (start: Date, end: Date) =>
  fetchFeeds({
    start: formatThingSpeakDate(start),
    end: formatThingSpeakDate(end),
    results: String(FEED_LIMIT)
  })

const dedupeAndSortReadings = (readings: SensorReading[]) => {
  const uniqueReadings = new Map<number, SensorReading>()

  readings.forEach((reading) => {
    uniqueReadings.set(reading.entryId, reading)
  })

  return Array.from(uniqueReadings.values()).sort(
    (left, right) => new Date(right.timestamp).getTime() - new Date(left.timestamp).getTime()
  )
}

const fetchAllInRange = async (start: Date, end: Date): Promise<SensorReading[]> => {
  const readings = await fetchFeedsInRange(start, end)
  const timeSpanMs = end.getTime() - start.getTime()

  if (readings.length < FEED_LIMIT || timeSpanMs <= 60 * 60 * 1000) {
    return readings
  }

  const midpoint = new Date(start.getTime() + Math.floor(timeSpanMs / 2))
  const left = await fetchAllInRange(start, midpoint)
  const right = await fetchAllInRange(midpoint, end)
  return [...left, ...right]
}

export const fetchAllHistoricalSensorReadings = async (daysBack = 365): Promise<SensorReading[]> => {
  const end = new Date()
  const start = new Date(end.getTime() - daysBack * 24 * 60 * 60 * 1000)
  const readings = await fetchAllInRange(start, end)
  return dedupeAndSortReadings(readings)
}

export const toChartSeries = (readings: SensorReading[]): SensorChartSeries => ({
  temperature: readings
    .filter((reading) => reading.temperature !== null)
    .map((reading) => ({
      time: reading.timestamp,
      value: reading.temperature as number
    })),
  moisture: readings
    .filter((reading) => reading.moisture !== null)
    .map((reading) => ({
      time: reading.timestamp,
      value: reading.moisture as number
    })),
  ambientTemp: readings
    .filter((reading) => reading.ambientTemp !== null)
    .map((reading) => ({
      time: reading.timestamp,
      value: reading.ambientTemp as number
    }))
})
