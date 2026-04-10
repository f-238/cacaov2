<template>
  <section class="analytics-shell">
    <div class="analytics-header">
      <div>
        <p class="eyebrow">Trend Analysis</p>
        <h1>Temperature and Moisture Analytics</h1>
        <p class="subtitle">
          Backend device history is visualized here for your registered device.
        </p>
      </div>

      <div class="summary-pill">
        {{ summaryText }}
      </div>
    </div>

    <div v-if="isLoading" class="empty-state">
      Loading analytics...
    </div>

    <div v-else-if="noDevice" class="empty-state">
      No device is registered to your account yet.
    </div>

    <div v-else-if="loadError" class="empty-state error-state">
      {{ loadError }}
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
              <p>Preview using backend readings</p>
            </div>
          </div>
        </div>

        <div v-if="tempData.length > 0" class="mini-chart temperature-chart" aria-label="Temperature trend preview">
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
        <div v-else class="chart-empty">
          No temperature readings yet.
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
              <p>Preview using backend readings</p>
            </div>
          </div>
        </div>

        <div v-if="moistureData.length > 0" class="mini-chart moisture-chart" aria-label="Moisture trend preview">
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
        <div v-else class="chart-empty">
          No moisture readings yet.
        </div>
      </article>
    </div>

    <section class="integration-card">
      <div class="integration-copy">
        <p class="eyebrow">Chart Library</p>
        <h2>Interactive Trends</h2>
        <p>
          Real chart rendering is now enabled with Chart.js using backend readings.
        </p>
        <div class="library-switch">
          <button
            type="button"
            class="library-chip"
            :class="{ active: selectedLibrary === 'Chart.js' }"
            @click="selectedLibrary = 'Chart.js'"
          >
            Chart.js
          </button>
          <button
            type="button"
            class="library-chip"
            :class="{ active: selectedLibrary === 'ApexCharts' }"
            @click="selectedLibrary = 'ApexCharts'"
          >
            ApexCharts (Soon)
          </button>
        </div>
      </div>

      <div class="integration-preview" aria-label="Chart library panel">
        <template v-if="selectedLibrary === 'Chart.js'">
          <div v-if="hasChartData" class="real-charts">
            <article class="real-chart-card">
              <p class="real-chart-title">Temperature and Ambient (Line)</p>
              <div class="chart-canvas-wrap">
                <canvas ref="trendCanvas"></canvas>
              </div>
            </article>

            <article class="real-chart-card">
              <p class="real-chart-title">Moisture (Bar)</p>
              <div class="chart-canvas-wrap">
                <canvas ref="moistureCanvas"></canvas>
              </div>
            </article>
          </div>

          <div v-else class="chart-empty">
            No data available yet to render Chart.js charts.
          </div>
        </template>

        <div v-else class="apex-placeholder">
          ApexCharts mode is reserved for the next iteration.
        </div>
      </div>
    </section>
  </section>
</template>

<script setup lang="ts">
import {
  BarController,
  BarElement,
  CategoryScale,
  Chart,
  type ChartConfiguration,
  Filler,
  Legend,
  LineController,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip
} from 'chart.js'
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { fetchMyDevices } from '../services/devices'
import { fetchHistoricalDeviceReadings, toChartSeries, type SensorChartSeries } from '../services/readings'

type DataPoint = {
  time: string
  value: number
}

const tempData = ref<DataPoint[]>([])
const moistureData = ref<DataPoint[]>([])
const ambientData = ref<DataPoint[]>([])
const isLoading = ref(true)
const noDevice = ref(false)
const loadError = ref('')
const selectedLibrary = ref<'Chart.js' | 'ApexCharts'>('Chart.js')
const trendCanvas = ref<HTMLCanvasElement | null>(null)
const moistureCanvas = ref<HTMLCanvasElement | null>(null)
let trendChart: Chart | null = null
let moistureChart: Chart | null = null

Chart.register(
  LineController,
  LineElement,
  PointElement,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Filler
)

const totalPoints = computed(() => tempData.value.length + moistureData.value.length)
const hasChartData = computed(() => tempData.value.length > 0 && moistureData.value.length > 0)
const summaryText = computed(() => {
  if (isLoading.value) {
    return 'Loading analytics...'
  }

  return `${totalPoints.value} total points`
})

const getRange = (points: DataPoint[]) => {
  if (points.length === 0) {
    return {
      min: 0,
      max: 1
    }
  }

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

const formatShortTime = (value: string) =>
  new Date(value).toLocaleTimeString(undefined, {
    hour: 'numeric',
    minute: '2-digit'
  })

const toChartTimeLabel = (value: string) =>
  new Date(value).toLocaleTimeString(undefined, {
    hour: '2-digit',
    minute: '2-digit'
  })

const destroyCharts = () => {
  trendChart?.destroy()
  moistureChart?.destroy()
  trendChart = null
  moistureChart = null
}

const readCssVariable = (name: string, fallback: string) => {
  const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim()
  return value || fallback
}

const renderChartJs = () => {
  if (selectedLibrary.value !== 'Chart.js') {
    destroyCharts()
    return
  }

  if (!hasChartData.value || !trendCanvas.value || !moistureCanvas.value) {
    destroyCharts()
    return
  }

  destroyCharts()

  const labels = tempData.value.map((point) => toChartTimeLabel(point.time))
  const textColor = readCssVariable('--app-text-secondary', '#526075')
  const gridColor = readCssVariable('--app-border-color', 'rgba(199, 208, 218, 0.6)')

  const trendContext = trendCanvas.value.getContext('2d')
  const moistureContext = moistureCanvas.value.getContext('2d')
  if (!trendContext || !moistureContext) {
    return
  }

  const trendConfig: ChartConfiguration<'line'> = {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Temperature (°C)',
          data: tempData.value.map((point) => point.value),
          borderColor: '#de7f67',
          backgroundColor: 'rgba(222, 127, 103, 0.18)',
          pointRadius: 2,
          tension: 0.32,
          fill: true
        },
        {
          label: 'Ambient (°C)',
          data: ambientData.value.map((point) => point.value),
          borderColor: '#4d7bb5',
          backgroundColor: 'rgba(77, 123, 181, 0.12)',
          pointRadius: 2,
          tension: 0.3,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: textColor,
            boxWidth: 12,
            usePointStyle: true,
            pointStyle: 'circle'
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: textColor,
            maxRotation: 0
          },
          grid: {
            color: gridColor
          }
        },
        y: {
          ticks: {
            color: textColor
          },
          grid: {
            color: gridColor
          }
        }
      }
    }
  }

  const moistureConfig: ChartConfiguration<'bar'> = {
    type: 'bar',
    data: {
      labels: moistureData.value.map((point) => toChartTimeLabel(point.time)),
      datasets: [
        {
          label: 'Moisture (%)',
          data: moistureData.value.map((point) => point.value),
          backgroundColor: 'rgba(73, 164, 131, 0.75)',
          borderColor: '#49a483',
          borderWidth: 1,
          borderRadius: 8,
          barPercentage: 0.72,
          categoryPercentage: 0.72
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: textColor,
            boxWidth: 12,
            usePointStyle: true,
            pointStyle: 'circle'
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: textColor,
            maxRotation: 0
          },
          grid: {
            color: gridColor
          }
        },
        y: {
          ticks: {
            color: textColor
          },
          grid: {
            color: gridColor
          }
        }
      }
    }
  }

  trendChart = new Chart(trendContext, trendConfig)
  moistureChart = new Chart(moistureContext, moistureConfig)
}

onMounted(async () => {
  try {
    const devices = await fetchMyDevices()
    const primaryDevice = devices[0]

    if (!primaryDevice) {
      noDevice.value = true
      return
    }

    const readings = await fetchHistoricalDeviceReadings(primaryDevice.id, 20)
    const series: SensorChartSeries = toChartSeries(readings)
    tempData.value = series.temperature
    moistureData.value = series.moisture
    ambientData.value = series.ambientTemp
  } catch (error) {
    loadError.value = error instanceof Error ? error.message : 'Unable to load analytics.'
  } finally {
    isLoading.value = false
  }
})

watch(
  () => [
    selectedLibrary.value,
    tempData.value.length,
    moistureData.value.length,
    ambientData.value.length
  ],
  async () => {
    await nextTick()
    renderChartJs()
  },
  { immediate: true }
)

onBeforeUnmount(() => {
  destroyCharts()
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

.empty-state {
  max-width: 1120px;
  margin: 0 auto 20px;
  padding: 18px 20px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.88);
  border: 1px dashed #d9c8d1;
  color: #526075;
}

.error-state {
  color: #b33f5a;
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

.chart-empty {
  min-height: 300px;
  border-radius: 22px;
  border: 1px dashed #d9c8d1;
  background: rgba(255, 255, 255, 0.72);
  display: grid;
  place-items: center;
  color: #6c7a8d;
  text-align: center;
  padding: 20px;
}

.integration-card {
  max-width: 1120px;
  margin: 28px auto 0;
  padding: 26px;
  display: grid;
  grid-template-columns: minmax(260px, 340px) 1fr;
  gap: 24px;
}

.library-switch {
  margin-top: 14px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.library-chip {
  min-height: 40px;
  padding: 0 14px;
  border-radius: 999px;
  border: 1px solid #eadfe5;
  background: rgba(255, 255, 255, 0.9);
  color: #526075;
  font-weight: 700;
  cursor: pointer;
}

.library-chip.active {
  background: linear-gradient(135deg, #f3a6ba, #9fd9cc);
  border-color: transparent;
  color: #1f2937;
}

.integration-preview {
  position: relative;
  min-height: 360px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid #eadfe5;
  padding: 14px;
}

.real-charts {
  display: grid;
  gap: 12px;
}

.real-chart-card {
  border: 1px solid #ebe1e6;
  border-radius: 16px;
  padding: 10px 12px 12px;
  background: rgba(255, 255, 255, 0.9);
}

.real-chart-title {
  margin: 0 0 8px;
  color: #526075;
  font-size: 0.9rem;
  font-weight: 700;
}

.chart-canvas-wrap {
  height: 130px;
}

.apex-placeholder {
  min-height: 300px;
  border-radius: 16px;
  border: 1px dashed #d9c8d1;
  background: rgba(255, 255, 255, 0.72);
  color: #6c7a8d;
  display: grid;
  place-items: center;
  text-align: center;
  padding: 20px;
}

.preview-badge {
  display: none;
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
