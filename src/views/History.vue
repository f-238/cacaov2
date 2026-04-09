<template>
  <section class="history-shell">
    <div class="history-header">
      <div>
        <p class="eyebrow">Reading History</p>
        <h1>All ThingSpeak Past Readings</h1>
        <p class="subtitle">
          Complete historical feed sorted by newest date and time first.
        </p>
      </div>

      <div class="summary-pill">
        <span class="summary-count">{{ filteredHistory.length }}</span>
        visible records
      </div>
    </div>

    <div class="table-card">
      <div class="table-toolbar">
        <div class="toolbar-copy">
          <p class="toolbar-note">
            Filter by date range or export the complete ThingSpeak history as CSV.
          </p>
        </div>

        <div class="toolbar-controls">
          <label class="filter-field">
            <span>From</span>
            <input v-model="startDate" type="date">
          </label>

          <label class="filter-field">
            <span>To</span>
            <input v-model="endDate" type="date">
          </label>

          <button class="secondary-button" type="button" @click="clearFilters">
            Clear
          </button>

          <button class="export-button" type="button" @click="exportCsv" :disabled="history.length === 0">
            Export CSV
          </button>
        </div>
      </div>

      <div class="table-scroll">
        <table v-if="filteredHistory.length > 0">
          <thead>
            <tr>
              <th>Entry ID</th>
              <th>Date</th>
              <th>Time</th>
              <th>Temperature</th>
              <th>Ambient Temp</th>
              <th>Moisture</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="reading in filteredHistory" :key="reading.entryId">
              <td>{{ reading.entryId }}</td>
              <td>{{ formatDate(reading.timestamp) }}</td>
              <td>{{ formatClock(reading.timestamp) }}</td>
              <td>
                <span class="metric-chip chip-temperature">
                  {{ formatMetric(reading.temperature, '°C') }}
                </span>
              </td>
              <td>
                <span class="metric-chip chip-ambient">
                  {{ formatMetric(reading.ambientTemp, '°C') }}
                </span>
              </td>
              <td>
                <span class="metric-chip chip-moisture">
                  {{ formatMetric(reading.moisture, '%') }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="history.length > 0 && filteredHistory.length === 0" class="empty-state">
        No readings match the selected date range.
      </div>

      <div v-if="history.length === 0" class="empty-state">
        No history data available yet.
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { fetchAllHistoricalSensorReadings, type SensorReading } from '../services/thingspeak'

const history = ref<SensorReading[]>([])
const startDate = ref('')
const endDate = ref('')

const sampleHistory: SensorReading[] = [
  {
    entryId: 1,
    timestamp: '2026-04-09T08:00:00.000Z',
    temperature: 29.8,
    ambientTemp: 27.9,
    moisture: 13.4
  },
  {
    entryId: 2,
    timestamp: '2026-04-09T09:30:00.000Z',
    temperature: 30.6,
    ambientTemp: 28.4,
    moisture: 12.8
  },
  {
    entryId: 3,
    timestamp: '2026-04-09T11:00:00.000Z',
    temperature: 31.2,
    ambientTemp: 29.1,
    moisture: 12.1
  }
]

const loadHistoryFallback = () => {
  const storedHistory = localStorage.getItem('sensorHistory')

  if (!storedHistory) {
    localStorage.setItem('sensorHistory', JSON.stringify(sampleHistory))
    history.value = sampleHistory
    return
  }

  try {
    const parsed = JSON.parse(storedHistory) as SensorReading[]
    history.value = Array.isArray(parsed) ? parsed : sampleHistory

    if (!Array.isArray(parsed)) {
      localStorage.setItem('sensorHistory', JSON.stringify(sampleHistory))
    }
  } catch {
    localStorage.setItem('sensorHistory', JSON.stringify(sampleHistory))
    history.value = sampleHistory
  }
}

const filteredHistory = computed(() => {
  const startBoundary = startDate.value ? new Date(`${startDate.value}T00:00:00`) : null
  const endBoundary = endDate.value ? new Date(`${endDate.value}T23:59:59.999`) : null

  return history.value.filter((reading) => {
    const readingTime = new Date(reading.timestamp).getTime()

    if (startBoundary && readingTime < startBoundary.getTime()) {
      return false
    }

    if (endBoundary && readingTime > endBoundary.getTime()) {
      return false
    }

    return true
  })
})

const formatDate = (value: string) =>
  new Date(value).toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })

const formatClock = (value: string) =>
  new Date(value).toLocaleTimeString(undefined, {
    hour: 'numeric',
    minute: '2-digit',
    second: '2-digit'
  })

const formatMetric = (value: number | null, unit: string) =>
  value === null ? 'N/A' : `${value.toFixed(1)} ${unit}`

const clearFilters = () => {
  startDate.value = ''
  endDate.value = ''
}

const exportCsv = () => {
  const csvRows = [
    ['entry_id', 'timestamp', 'date', 'time', 'temperature_c', 'ambient_temp_c', 'moisture_percent'],
    ...history.value.map((reading) => [
      String(reading.entryId),
      reading.timestamp,
      formatDate(reading.timestamp),
      formatClock(reading.timestamp),
      reading.temperature === null ? '' : reading.temperature.toFixed(1),
      reading.ambientTemp === null ? '' : reading.ambientTemp.toFixed(1),
      reading.moisture === null ? '' : reading.moisture.toFixed(1)
    ])
  ]

  const csvContent = csvRows
    .map((row) =>
      row
        .map((cell) => `"${String(cell).replaceAll('"', '""')}"`)
        .join(',')
    )
    .join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const downloadUrl = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = downloadUrl
  link.download = 'thingspeak-history.csv'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(downloadUrl)
}

onMounted(() => {
  fetchAllHistoricalSensorReadings()
    .then((readings) => {
      history.value = readings
      localStorage.setItem('sensorHistory', JSON.stringify(readings))
    })
    .catch(() => {
      loadHistoryFallback()
    })
})
</script>

<style scoped>
:global(body) {
  font-family: 'Inter', 'Poppins', 'Roboto', sans-serif;
}

.history-shell {
  min-height: calc(100vh - 72px);
  padding: 32px 20px 48px;
  background:
    radial-gradient(circle at top left, rgba(255, 229, 235, 0.9), transparent 24%),
    radial-gradient(circle at bottom right, rgba(222, 245, 239, 0.9), transparent 28%),
    #fcfcfd;
}

.history-header {
  max-width: 1200px;
  margin: 0 auto 24px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.eyebrow {
  margin: 0 0 10px;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #d17890;
}

h1 {
  margin: 0;
  font-size: clamp(2rem, 4vw, 3rem);
  color: #243042;
}

.subtitle,
.toolbar-note {
  margin: 12px 0 0;
  color: #5f6d81;
  line-height: 1.6;
}

.summary-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid #eadfe5;
  color: #526075;
  box-shadow: 0 16px 30px rgba(36, 48, 66, 0.08);
}

.summary-count {
  display: inline-grid;
  place-items: center;
  min-width: 32px;
  height: 32px;
  padding: 0 8px;
  border-radius: 999px;
  background: #eef8f4;
  color: #2f8669;
  font-weight: 700;
}

.table-card {
  max-width: 1200px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #efe3e7;
  border-radius: 24px;
  box-shadow: 0 22px 50px rgba(36, 48, 66, 0.08);
  overflow: hidden;
}

.table-toolbar {
  padding: 18px 22px 0;
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 20px;
  flex-wrap: wrap;
}

.toolbar-copy {
  max-width: 420px;
}

.toolbar-controls {
  display: flex;
  align-items: end;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-field {
  display: grid;
  gap: 6px;
  color: #526075;
  font-size: 0.92rem;
  font-weight: 600;
}

.filter-field input {
  min-height: 42px;
  padding: 0 12px;
  border: 1px solid #e6dce2;
  border-radius: 14px;
  background: #fff;
  color: #243042;
}

.filter-field input:focus {
  outline: none;
  border-color: #d9a6b8;
  box-shadow: 0 0 0 4px rgba(233, 189, 204, 0.25);
}

.secondary-button,
.export-button {
  min-height: 42px;
  padding: 0 14px;
  border-radius: 14px;
  cursor: pointer;
  font-weight: 700;
}

.secondary-button {
  border: 1px solid #eadfe5;
  background: rgba(255, 255, 255, 0.88);
  color: #526075;
}

.export-button {
  border: 0;
  background: linear-gradient(135deg, #f3a6ba, #9fd9cc);
  color: #1f2937;
}

.export-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.table-scroll {
  overflow-x: auto;
}

table {
  width: 100%;
  min-width: 900px;
  border-collapse: collapse;
  margin-top: 18px;
}

thead th {
  padding: 18px 22px;
  text-align: left;
  font-size: 0.95rem;
  font-weight: 700;
  color: #334155;
  background: #fff8fa;
  border-bottom: 1px solid #f0e3e8;
}

tbody td {
  padding: 18px 22px;
  border-bottom: 1px solid #f4edf0;
  color: #334155;
}

tbody tr:last-child td {
  border-bottom: 0;
}

tbody tr:hover {
  background: #fffdfd;
}

.metric-chip {
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 999px;
  font-weight: 700;
}

.chip-temperature {
  background: #fff2ed;
  color: #ca6e4f;
}

.chip-ambient {
  background: #eef6ff;
  color: #4d7bb5;
}

.chip-moisture {
  background: #effaf5;
  color: #3b9274;
}

.empty-state {
  padding: 28px;
  text-align: center;
  color: #7a8799;
}

@media (max-width: 720px) {
  .history-shell {
    padding: 22px 14px 36px;
  }

  .history-header {
    flex-direction: column;
  }

  .table-card {
    border-radius: 20px;
  }

  .table-toolbar {
    padding: 16px 14px 0;
  }

  .toolbar-controls {
    width: 100%;
  }

  .filter-field {
    width: 100%;
  }

  .filter-field input,
  .secondary-button,
  .export-button {
    width: 100%;
  }

  thead th,
  tbody td {
    padding: 16px 14px;
  }
}
</style>
