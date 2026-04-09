<template>
  <section class="dashboard-shell">
    <div class="dashboard-header">
      <div>
        <p class="eyebrow">Live Overview</p>
        <h1>Cacao Drying Dashboard</h1>
        <p class="subtitle">
          Latest reading from ThingSpeak, with local fallback data if the API is temporarily unavailable.
        </p>
      </div>

      <div class="status-pill">
        <span class="status-dot"></span>
        Last update: {{ formattedLastUpdate }}
      </div>
    </div>

    <div class="cards">
      <article
        v-for="metric in metrics"
        :key="metric.label"
        class="metric-card"
        :class="metric.tone"
      >
        <div class="card-head">
          <span class="card-icon" aria-hidden="true">
            <svg v-if="metric.icon === 'temperature'" viewBox="0 0 24 24" focusable="false">
              <path
                d="M14 14.76V5a2 2 0 1 0-4 0v9.76a4 4 0 1 0 4 0ZM12 20a2 2 0 0 1-1-3.73V6a1 1 0 0 1 2 0v10.27A2 2 0 0 1 12 20Z"
              />
            </svg>
            <svg v-else-if="metric.icon === 'moisture'" viewBox="0 0 24 24" focusable="false">
              <path
                d="M12 3.25C12 3.25 6 10 6 14a6 6 0 0 0 12 0c0-4-6-10.75-6-10.75Zm0 14.75a4 4 0 0 1-4-4c0-2.13 2.46-5.77 4-7.7 1.54 1.93 4 5.57 4 7.7a4 4 0 0 1-4 4Z"
              />
            </svg>
            <svg v-else viewBox="0 0 24 24" focusable="false">
              <path
                d="M6 19a4 4 0 0 1-.57-7.96A6.5 6.5 0 0 1 18 9.5a4.5 4.5 0 1 1 .5 9H6Z"
              />
            </svg>
          </span>
          <span class="metric-label">{{ metric.label }}</span>
        </div>

        <p class="metric-value">{{ metric.value }} <span>{{ metric.unit }}</span></p>
        <p class="metric-note">{{ metric.note }}</p>
      </article>
    </div>

    <section class="chart-section">
      <div class="chart-copy">
        <p class="eyebrow">Future Charts</p>
        <h2>Reserved analytics area</h2>
        <p>
          This panel is ready for upcoming trend charts, comparisons, and drying history visuals.
        </p>
      </div>

      <div class="chart-placeholder" aria-label="Future chart placeholder">
        <div class="chart-grid"></div>
        <div class="chart-line chart-line-one"></div>
        <div class="chart-line chart-line-two"></div>
      </div>
    </section>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { fetchLatestSensorSnapshot, type SensorSnapshot } from '../services/thingspeak'

const sensorData = ref<SensorSnapshot>({
  temperature: 30.5,
  moisture: 12.3,
  ambientTemp: 27.1,
  lastUpdate: new Date().toISOString()
})

const formattedLastUpdate = computed(() =>
  new Date(sensorData.value.lastUpdate).toLocaleString()
)

const metrics = computed(() => [
  {
    label: 'Bean Temperature',
    value: sensorData.value.temperature.toFixed(1),
    unit: '°C',
    note: 'Core drying chamber reading',
    icon: 'temperature',
    tone: 'tone-peach'
  },
  {
    label: 'Moisture',
    value: sensorData.value.moisture.toFixed(1),
    unit: '%',
    note: 'Current moisture level estimate',
    icon: 'moisture',
    tone: 'tone-mint'
  },
  {
    label: 'Ambient Temp',
    value: sensorData.value.ambientTemp.toFixed(1),
    unit: '°C',
    note: 'Surrounding air temperature',
    icon: 'ambient',
    tone: 'tone-sky'
  }
])

const loadLocalSensorData = () => {
  const existingData = localStorage.getItem('sensorData')

  if (!existingData) {
    localStorage.setItem('sensorData', JSON.stringify(sensorData.value))
    return
  }

  try {
    const parsed = JSON.parse(existingData) as Partial<SensorSnapshot>

    sensorData.value = {
      temperature: typeof parsed.temperature === 'number' ? parsed.temperature : 30.5,
      moisture: typeof parsed.moisture === 'number' ? parsed.moisture : 12.3,
      ambientTemp: typeof parsed.ambientTemp === 'number' ? parsed.ambientTemp : 27.1,
      lastUpdate:
        typeof parsed.lastUpdate === 'string' ? parsed.lastUpdate : new Date().toISOString()
    }
  } catch {
    localStorage.setItem('sensorData', JSON.stringify(sensorData.value))
  }
}

onMounted(() => {
  fetchLatestSensorSnapshot()
    .then((latest) => {
      sensorData.value = latest
      localStorage.setItem('sensorData', JSON.stringify(latest))
    })
    .catch(() => {
      loadLocalSensorData()
    })
})
</script>

<style scoped>
:global(body) {
  font-family: 'Inter', 'Poppins', 'Roboto', sans-serif;
}

.dashboard-shell {
  min-height: calc(100vh - 72px);
  padding: 32px 20px 48px;
  background:
    radial-gradient(circle at top left, rgba(255, 226, 234, 0.9), transparent 28%),
    radial-gradient(circle at top right, rgba(221, 245, 239, 0.9), transparent 26%),
    #fcfcfd;
}

.dashboard-header {
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
  font-size: clamp(1.4rem, 3vw, 2rem);
}

.subtitle,
.chart-copy p {
  margin: 12px 0 0;
  color: #5f6d81;
  line-height: 1.6;
  max-width: 640px;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid #e9dfe5;
  color: #4a596f;
  white-space: nowrap;
  box-shadow: 0 16px 30px rgba(36, 48, 66, 0.08);
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #74c6a4;
  box-shadow: 0 0 0 5px rgba(116, 198, 164, 0.16);
}

.cards {
  max-width: 1120px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.metric-card,
.chart-section {
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid #efe3e7;
  border-radius: 24px;
  box-shadow: 0 22px 50px rgba(36, 48, 66, 0.08);
}

.metric-card {
  padding: 22px;
}

.card-head {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-icon {
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  border-radius: 16px;
}

.card-icon svg {
  width: 24px;
  height: 24px;
  fill: currentColor;
}

.metric-label {
  font-size: 1rem;
  font-weight: 700;
  color: #334155;
}

.metric-value {
  margin: 18px 0 10px;
  font-size: clamp(2rem, 4vw, 2.6rem);
  font-weight: 700;
  color: #1f2937;
}

.metric-value span {
  font-size: 1rem;
  font-weight: 600;
  color: #64748b;
}

.metric-note {
  margin: 0;
  color: #6c7a8d;
  line-height: 1.5;
}

.tone-peach .card-icon {
  background: #fff1ec;
  color: #d78065;
}

.tone-mint .card-icon {
  background: #ebfaf4;
  color: #48a786;
}

.tone-sky .card-icon {
  background: #eef6ff;
  color: #5c90d4;
}

.chart-section {
  max-width: 1120px;
  margin: 28px auto 0;
  padding: 26px;
  display: grid;
  grid-template-columns: minmax(240px, 320px) 1fr;
  gap: 24px;
}

.chart-placeholder {
  position: relative;
  min-height: 280px;
  overflow: hidden;
  border-radius: 22px;
  background:
    linear-gradient(180deg, rgba(252, 226, 234, 0.55), rgba(223, 247, 242, 0.55)),
    #fff;
  border: 1px dashed #d9c8d1;
}

.chart-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(to right, rgba(120, 134, 156, 0.12) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(120, 134, 156, 0.12) 1px, transparent 1px);
  background-size: 52px 52px;
}

.chart-line {
  position: absolute;
  left: 7%;
  right: 7%;
  height: 3px;
  border-radius: 999px;
}

.chart-line-one {
  top: 42%;
  background: linear-gradient(90deg, #f0a7ba, #d889a0, #9fd9cc);
  transform: rotate(-6deg);
}

.chart-line-two {
  top: 62%;
  background: linear-gradient(90deg, #8cc7ea, #9fd9cc, #f8c79b);
  transform: rotate(4deg);
}

@media (max-width: 900px) {
  .cards {
    grid-template-columns: 1fr;
  }

  .chart-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .dashboard-shell {
    padding: 22px 14px 36px;
  }

  .dashboard-header {
    flex-direction: column;
  }

  .status-pill {
    white-space: normal;
  }

  .metric-card,
  .chart-section {
    border-radius: 20px;
  }
}
</style>
