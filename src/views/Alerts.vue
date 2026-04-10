<template>
  <section class="alerts-shell">
    <div class="alerts-header">
      <div>
        <p class="eyebrow">Alert Center</p>
        <h1>System Notifications</h1>
        <p class="subtitle">
          Backend alert records for your registered device.
        </p>
      </div>

      <div class="summary-pills">
        <span class="summary-pill">{{ summaryText }}</span>
      </div>
    </div>

    <div v-if="isLoading" class="empty-state">
      Loading alerts...
    </div>

    <div v-else-if="noDevice" class="empty-state">
      No device is registered to your account yet.
    </div>

    <div v-else-if="loadError" class="empty-state error-state">
      {{ loadError }}
    </div>

    <div class="alerts-list" v-else-if="alerts.length > 0">
      <article
        v-for="alert in alerts"
        :key="alert.id"
        class="alert-card"
        :class="`severity-${alert.type}`"
      >
        <div class="alert-icon" :class="`icon-${alert.type}`" aria-hidden="true">
          <svg v-if="alert.type === 'info'" viewBox="0 0 24 24" focusable="false">
            <path
              d="M11 10h2v7h-2Zm0-3h2v2h-2Zm1-5a10 10 0 1 0 10 10A10 10 0 0 0 12 2Z"
            />
          </svg>
          <svg v-else-if="alert.type === 'warning'" viewBox="0 0 24 24" focusable="false">
            <path
              d="M1 21h22L12 2Zm12-3h-2v2h2Zm0-8h-2v6h2Z"
            />
          </svg>
          <svg v-else viewBox="0 0 24 24" focusable="false">
            <path
              d="M12 2 1 21h22Zm1 15h-2v2h2Zm0-8h-2v6h2Z"
            />
          </svg>
        </div>

        <div class="alert-content">
          <div class="alert-top">
            <span class="severity-badge" :class="`badge-${alert.type}`">
              {{ alert.type }}
            </span>
            <time class="timestamp">{{ formatTimestamp(alert.timestamp) }}</time>
          </div>

          <p class="message">{{ alert.message }}</p>
        </div>
      </article>
    </div>

    <div v-else class="empty-state">
      No alerts available yet.
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { fetchDeviceAlerts, type ApiAlertSeverity } from '../services/alerts'
import { fetchMyDevices } from '../services/devices'

type AlertItem = {
  id: number
  message: string
  type: 'info' | 'warning' | 'critical'
  timestamp: string
}

const alerts = ref<AlertItem[]>([])
const isLoading = ref(true)
const noDevice = ref(false)
const loadError = ref('')

const summaryText = computed(() => {
  if (isLoading.value) {
    return 'Loading alerts...'
  }

  return `${alerts.value.length} alerts`
})

const mapSeverity = (severity: ApiAlertSeverity): AlertItem['type'] => {
  if (severity === 'critical') {
    return 'critical'
  }

  if (severity === 'warning') {
    return 'warning'
  }

  return 'info'
}

const formatTimestamp = (value: string) =>
  new Date(value).toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  })

onMounted(async () => {
  try {
    const devices = await fetchMyDevices()
    const primaryDevice = devices[0]

    if (!primaryDevice) {
      noDevice.value = true
      return
    }

    const backendAlerts = await fetchDeviceAlerts(primaryDevice.id)
    alerts.value = backendAlerts.map((alert) => ({
      id: alert.id,
      message: alert.message,
      type: mapSeverity(alert.severity),
      timestamp: alert.created_at
    }))
  } catch (error) {
    loadError.value = error instanceof Error ? error.message : 'Unable to load alerts.'
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
:global(body) {
  font-family: 'Inter', 'Poppins', 'Roboto', sans-serif;
}

.alerts-shell {
  min-height: calc(100vh - 72px);
  padding: 32px 20px 48px;
  background:
    radial-gradient(circle at top left, rgba(255, 229, 235, 0.92), transparent 24%),
    radial-gradient(circle at bottom right, rgba(223, 246, 240, 0.92), transparent 28%),
    #fcfcfd;
}

.alerts-header {
  max-width: 980px;
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

.subtitle {
  margin: 12px 0 0;
  color: #5f6d81;
  line-height: 1.6;
  max-width: 620px;
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

.alerts-list {
  max-width: 980px;
  margin: 0 auto;
  display: grid;
  gap: 16px;
}

.alert-card {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 16px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #efe3e7;
  border-radius: 22px;
  box-shadow: 0 22px 50px rgba(36, 48, 66, 0.08);
}

.alert-icon {
  width: 52px;
  height: 52px;
  display: grid;
  place-items: center;
  border-radius: 18px;
}

.alert-icon svg {
  width: 24px;
  height: 24px;
  fill: currentColor;
}

.alert-content {
  min-width: 0;
}

.alert-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  margin-bottom: 10px;
}

.severity-badge {
  display: inline-flex;
  align-items: center;
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 0.88rem;
  font-weight: 700;
  text-transform: capitalize;
}

.timestamp {
  color: #7a8799;
  font-size: 0.95rem;
}

.message {
  margin: 0;
  color: #243042;
  font-size: 1rem;
  line-height: 1.6;
}

.severity-info {
  border-left: 5px solid #8cc7ea;
}

.severity-warning {
  border-left: 5px solid #f3c66b;
}

.severity-critical {
  border-left: 5px solid #e78a97;
}

.icon-info,
.badge-info {
  background: #eef7fd;
  color: #4f8ab2;
}

.icon-warning,
.badge-warning {
  background: #fff7e8;
  color: #b88a2b;
}

.icon-critical,
.badge-critical {
  background: #fff1f3;
  color: #c05c72;
}

.empty-state {
  max-width: 980px;
  margin: 0 auto;
  padding: 28px;
  text-align: center;
  color: #7a8799;
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid #efe3e7;
  border-radius: 22px;
  box-shadow: 0 22px 50px rgba(36, 48, 66, 0.08);
}

.error-state {
  color: #b33f5a;
}

@media (max-width: 720px) {
  .alerts-shell {
    padding: 22px 14px 36px;
  }

  .alerts-header {
    flex-direction: column;
  }

  .alert-card {
    grid-template-columns: 1fr;
  }

  .alert-top {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
