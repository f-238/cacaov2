<template>
  <section class="analytics-shell">
    <div class="analytics-header">
      <div>
        <p class="eyebrow">Trend Analysis</p>
        <h1>Temperature and Moisture Analytics</h1>
        <p class="subtitle">
          ThingSpeak history is visualized here, with local fallback data before chart-library integration.
        </p>
      </div>

      <div class="summary-pill">
        {{ totalPoints }} total points
      </div>
    </div>

    <div class="chart-grid">
      <article class="chart-card">
        <div class="chart-card-head">
          <div class="chart-title-wrap">
            <span class="chart-icon temperature" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false">
                <path
                  d="M14 14.76V5a2 2 0 1 0-4 0v9.76a4 4 0 1 0 4 0ZM12 20a2 2 0 0 1-1-3.73V6a1 1 0 0 1 2 0v10.27A2 2 0 0 1 12 20Z"
                />
              </svg>
            </span>
            <div>
              <h2>Temperature Trend</h2>
              <p>Preview using ThingSpeak readings</p>
            </div>
          </div>
        </div>

        <div class="mini-chart temperature-chart" aria-label="Temperature trend preview">
          <div
            v-for="point in tempData"
            :key="`temp-${point.time}`"
            class="bar-group"
          >
            <div class="bar temperature-bar" :style="{ height: `${normalizeHeight(point.value, tempRange)}%` }"></div>
            <span class="bar-value">{{ point.value.toFixed(1) }} °C</span>
            <span class="bar-label">{{ formatShortTime(point.time) }}</span>
          </div>
        </div>
      </article>

      <article class="chart-card">
        <div class="chart-card-head">
          <div class="chart-title-wrap">
            <span class="chart-icon moisture" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false">
                <path
                  d="M12 3.25C12 3.25 6 10 6 14a6 6 0 0 0 12 0c0-4-6-10.75-6-10.75Zm0 14.75a4 4 0 0 1-4-4c0-2.13 2.46-5.77 4-7.7 1.54 1.93 4 5.57 4 7.7a4 4 0 0 1-4 4Z"
                />
              </svg>
            </span>
            <div>
              <h2>Moisture Trend</h2>
              <p>Preview using ThingSpeak readings</p>
            </div>
          </div>
        </div>

        <div class="mini-chart moisture-chart" aria-label="Moisture trend preview">
          <div
            v-for="point in moistureData"
            :key="`moisture-${point.time}`"
            class="bar-group"
          >
            <div class="bar moisture-bar" :style="{ height: `${normalizeHeight(point.value, moistureRange)}%` }"></div>
            <span class="bar-value">{{ point.value.toFixed(1) }}%</span>
            <span class="bar-label">{{ formatShortTime(point.time) }}</span>
          </div>
        </div>
      </article>
    </div>

    <section class="integration-card">
      <div class="integration-copy">
        <p class="eyebrow">Future Integration</p>
        <h2>Chart.js / ApexCharts placeholder</h2>
        <p>
          This section is reserved for the real charting library. The current layout keeps spacing and hierarchy ready for a future swap.
        </p>
      </div>

      <div class="integration-preview" aria-label="Chart library placeholder">
        <div class="preview-grid"></div>
        <div class="preview-line line-one"></div>
        <div class="preview-line line-two"></div>
      </div>
    </section>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { fetchHistoricalSensorReadings, toChartSeries, type SensorChartSeries } from '../services/thingspeak'

type DataPoint = {
  time: string
  value: number
}

type AnalyticsData = {
  temperature: DataPoint[]
  moisture: DataPoint[]
}

const seededAnalytics: AnalyticsData = {
  temperature: [
    { time: '2026-04-09T08:00:00.000Z', value: 29.8 },
    { time: '2026-04-09T09:30:00.000Z', value: 30.5 },
    { time: '2026-04-09T11:00:00.000Z', value: 31.1 },
    { time: '2026-04-09T12:30:00.000Z', value: 32.0 },
    { time: '2026-04-09T14:00:00.000Z', value: 31.4 }
  ],
  moisture: [
    { time: '2026-04-09T08:00:00.000Z', value: 13.5 },
    { time: '2026-04-09T09:30:00.000Z', value: 12.9 },
    { time: '2026-04-09T11:00:00.000Z', value: 12.2 },
    { time: '2026-04-09T12:30:00.000Z', value: 11.7 },
    { time: '2026-04-09T14:00:00.000Z', value: 11.3 }
  ]
}

const tempData = ref<DataPoint[]>([])
const moistureData = ref<DataPoint[]>([])

const totalPoints = computed(() => tempData.value.length + moistureData.value.length)

const getRange = (points: DataPoint[]) => {
  const values = points.map((point) => point.value)
  const min = Math.min(...values)
  const max = Math.max(...values)

  return {
    min,
    max
  }
}

const tempRange = computed(() => getRange(tempData.value))
const moistureRange = computed(() => getRange(moistureData.value))

const normalizeHeight = (value: number, range: { min: number; max: number }) => {
  if (range.max === range.min) {
    return 60
  }

  const scaled = ((value - range.min) / (range.max - range.min)) * 55 + 25
  return Number(scaled.toFixed(2))
}

const loadAnalyticsData = () => {
  const storedAnalytics = localStorage.getItem('analyticsData')

  if (!storedAnalytics) {
    localStorage.setItem('analyticsData', JSON.stringify(seededAnalytics))
    tempData.value = seededAnalytics.temperature
    moistureData.value = seededAnalytics.moisture
    return
  }

  try {
    const parsed = JSON.parse(storedAnalytics) as Partial<AnalyticsData>
    const hasTemperature = Array.isArray(parsed.temperature)
    const hasMoisture = Array.isArray(parsed.moisture)

    tempData.value = hasTemperature ? (parsed.temperature as DataPoint[]) : seededAnalytics.temperature
    moistureData.value = hasMoisture ? (parsed.moisture as DataPoint[]) : seededAnalytics.moisture

    if (!hasTemperature || !hasMoisture) {
      localStorage.setItem('analyticsData', JSON.stringify(seededAnalytics))
    }
  } catch {
    localStorage.setItem('analyticsData', JSON.stringify(seededAnalytics))
    tempData.value = seededAnalytics.temperature
    moistureData.value = seededAnalytics.moisture
  }
}

const formatShortTime = (value: string) =>
  new Date(value).toLocaleTimeString(undefined, {
    hour: 'numeric',
    minute: '2-digit'
  })

onMounted(() => {
  fetchHistoricalSensorReadings(20)
    .then((readings) => {
      const series: SensorChartSeries = toChartSeries(readings)
      tempData.value = series.temperature
      moistureData.value = series.moisture

      localStorage.setItem(
        'analyticsData',
        JSON.stringify({
          temperature: series.temperature,
          moisture: series.moisture
        })
      )
    })
    .catch(() => {
      loadAnalyticsData()
    })
})
</script>

<style scoped>
:global(body) {
  font-family: 'Inter', 'Poppins', 'Roboto', sans-serif;
}

.analytics-shell {
  min-height: calc(100vh - 72px);
  padding: 32px 20px 48px;
  background:
    radial-gradient(circle at top left, rgba(255, 229, 235, 0.92), transparent 24%),
    radial-gradient(circle at bottom right, rgba(223, 246, 240, 0.92), transparent 28%),
    #fcfcfd;
}

.analytics-header {
  max-width: 1120px;
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

h1,
h2 {
  margin: 0;
  color: #243042;
}

h1 {
  font-size: clamp(2rem, 4vw, 3rem);
}

h2 {
  font-size: clamp(1.2rem, 2.6vw, 1.6rem);
}

.subtitle,
.integration-copy p,
.chart-title-wrap p {
  margin: 12px 0 0;
  color: #5f6d81;
  line-height: 1.6;
}

.summary-pill {
  display: inline-flex;
  align-items: center;
  padding: 12px 16px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid #eadfe5;
  color: #526075;
  box-shadow: 0 16px 30px rgba(36, 48, 66, 0.08);
  font-weight: 700;
}

.chart-grid {
  max-width: 1120px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}

.chart-card,
.integration-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #efe3e7;
  border-radius: 24px;
  box-shadow: 0 22px 50px rgba(36, 48, 66, 0.08);
}

.chart-card {
  padding: 22px;
}

.chart-card-head {
  margin-bottom: 18px;
}

.chart-title-wrap {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.chart-icon {
  width: 46px;
  height: 46px;
  display: grid;
  place-items: center;
  border-radius: 16px;
  flex-shrink: 0;
}

.chart-icon svg {
  width: 22px;
  height: 22px;
  fill: currentColor;
}

.chart-icon.temperature {
  background: #fff0ea;
  color: #d87e5f;
}

.chart-icon.moisture {
  background: #eefaf5;
  color: #49a483;
}

.mini-chart {
  min-height: 300px;
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
  align-items: end;
  padding: 22px 18px 18px;
  border-radius: 22px;
  position: relative;
  overflow: hidden;
}

.mini-chart::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(to right, rgba(120, 134, 156, 0.08) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(120, 134, 156, 0.08) 1px, transparent 1px);
  background-size: 52px 52px;
  pointer-events: none;
}

.temperature-chart {
  background: linear-gradient(180deg, rgba(255, 240, 234, 0.65), rgba(255, 255, 255, 0.92));
}

.moisture-chart {
  background: linear-gradient(180deg, rgba(238, 250, 245, 0.7), rgba(255, 255, 255, 0.92));
}

.bar-group {
  position: relative;
  z-index: 1;
  display: grid;
  justify-items: center;
  align-items: end;
  gap: 10px;
}

.bar {
  width: 100%;
  max-width: 44px;
  min-height: 48px;
  border-radius: 16px 16px 10px 10px;
  box-shadow: inset 0 -8px 16px rgba(255, 255, 255, 0.18);
}

.temperature-bar {
  background: linear-gradient(180deg, #f6b39d, #de7f67);
}

.moisture-bar {
  background: linear-gradient(180deg, #9ad8c5, #49a483);
}

.bar-value,
.bar-label {
  text-align: center;
}

.bar-value {
  font-size: 0.82rem;
  font-weight: 700;
  color: #334155;
}

.bar-label {
  font-size: 0.8rem;
  color: #7a8799;
}

.integration-card {
  max-width: 1120px;
  margin: 28px auto 0;
  padding: 26px;
  display: grid;
  grid-template-columns: minmax(260px, 340px) 1fr;
  gap: 24px;
}

.integration-preview {
  position: relative;
  min-height: 280px;
  border-radius: 22px;
  overflow: hidden;
  background:
    linear-gradient(180deg, rgba(252, 226, 234, 0.55), rgba(223, 247, 242, 0.55)),
    #fff;
  border: 1px dashed #d9c8d1;
}

.preview-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(to right, rgba(120, 134, 156, 0.12) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(120, 134, 156, 0.12) 1px, transparent 1px);
  background-size: 52px 52px;
}

.preview-line {
  position: absolute;
  left: 7%;
  right: 7%;
  height: 3px;
  border-radius: 999px;
}

.line-one {
  top: 38%;
  background: linear-gradient(90deg, #f0a7ba, #d889a0, #9fd9cc);
  transform: rotate(-4deg);
}

.line-two {
  top: 58%;
  background: linear-gradient(90deg, #8cc7ea, #9fd9cc, #f8c79b);
  transform: rotate(5deg);
}

@media (max-width: 900px) {
  .chart-grid,
  .integration-card {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .analytics-shell {
    padding: 22px 14px 36px;
  }

  .analytics-header {
    flex-direction: column;
  }

  .chart-card,
  .integration-card {
    border-radius: 20px;
  }

  .mini-chart {
    min-height: 260px;
    gap: 10px;
    padding: 18px 12px 14px;
  }

  .bar {
    max-width: 100%;
  }
}
</style>
