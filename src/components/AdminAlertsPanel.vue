<template>
  <section class="panel alerts-panel">
    <div class="panel-head">
      <div>
        <p class="eyebrow">Alerts</p>
        <h3>Alerts & Notifications</h3>
        <p>Review device events, filter by severity, and resolve handled notifications.</p>
      </div>

      <div class="summary-row">
        <span class="summary-pill">{{ filteredAlerts.length }} visible</span>
        <span class="summary-pill">{{ unresolvedCount }} unresolved</span>
      </div>
    </div>

    <div class="toolbar">
      <label class="filter-field">
        <span>Severity</span>
        <select v-model="selectedSeverity">
          <option value="all">All severities</option>
          <option value="info">Info</option>
          <option value="warning">Warning</option>
          <option value="critical">Critical</option>
        </select>
      </label>
    </div>

    <div v-if="filteredAlerts.length > 0" class="table-shell">
      <table class="alerts-table">
        <thead>
          <tr>
            <th>Device</th>
            <th>Type</th>
            <th>Severity</th>
            <th>Message</th>
            <th>Timestamp</th>
            <th>Resolved</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="alert in filteredAlerts" :key="alert.id">
            <td>{{ alert.device }}</td>
            <td>{{ alert.type }}</td>
            <td>
              <span class="severity-chip" :class="`severity-${alert.severity}`">
                <span class="chip-icon" aria-hidden="true">
                  <svg v-if="alert.severity === 'info'" viewBox="0 0 24 24" focusable="false">
                    <path d="M11 10h2v7h-2Zm0-3h2v2h-2Zm1-5a10 10 0 1 0 10 10A10 10 0 0 0 12 2Z" />
                  </svg>
                  <svg v-else-if="alert.severity === 'warning'" viewBox="0 0 24 24" focusable="false">
                    <path d="M1 21h22L12 2Zm12-3h-2v2h2Zm0-8h-2v6h2Z" />
                  </svg>
                  <svg v-else viewBox="0 0 24 24" focusable="false">
                    <path d="M12 2 1 21h22Zm1 15h-2v2h2Zm0-8h-2v6h2Z" />
                  </svg>
                </span>
                {{ alert.severity }}
              </span>
            </td>
            <td class="message-cell">{{ alert.message }}</td>
            <td>{{ formatTimestamp(alert.timestamp) }}</td>
            <td>
              <label class="resolved-toggle">
                <input
                  :checked="alert.resolved"
                  type="checkbox"
                  @change="toggleResolved(alert.id)"
                />
                <span>{{ alert.resolved ? 'Yes' : 'No' }}</span>
              </label>
            </td>
            <td>
              <button
                class="action-button"
                :disabled="alert.resolved"
                @click="markResolved(alert.id)"
              >
                <span class="button-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" focusable="false">
                    <path d="M9.55 18 3.85 12.3l1.41-1.41 4.29 4.29 9.19-9.18 1.41 1.41Z" />
                  </svg>
                </span>
                <span>{{ alert.resolved ? 'Resolved' : 'Mark Resolved' }}</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="filteredAlerts.length > 0" class="mobile-list">
      <article v-for="alert in filteredAlerts" :key="`${alert.id}-mobile`" class="mobile-card">
        <div class="mobile-top">
          <div>
            <p class="mobile-device">{{ alert.device }}</p>
            <p class="mobile-type">{{ alert.type }}</p>
          </div>
          <span class="severity-chip" :class="`severity-${alert.severity}`">
            <span class="chip-icon" aria-hidden="true">
              <svg v-if="alert.severity === 'info'" viewBox="0 0 24 24" focusable="false">
                <path d="M11 10h2v7h-2Zm0-3h2v2h-2Zm1-5a10 10 0 1 0 10 10A10 10 0 0 0 12 2Z" />
              </svg>
              <svg v-else-if="alert.severity === 'warning'" viewBox="0 0 24 24" focusable="false">
                <path d="M1 21h22L12 2Zm12-3h-2v2h2Zm0-8h-2v6h2Z" />
              </svg>
              <svg v-else viewBox="0 0 24 24" focusable="false">
                <path d="M12 2 1 21h22Zm1 15h-2v2h2Zm0-8h-2v6h2Z" />
              </svg>
            </span>
            {{ alert.severity }}
          </span>
        </div>

        <p class="mobile-message">{{ alert.message }}</p>

        <div class="mobile-meta">
          <span>{{ formatTimestamp(alert.timestamp) }}</span>
          <span>{{ alert.resolved ? 'Resolved' : 'Pending' }}</span>
        </div>

        <div class="mobile-actions">
          <label class="resolved-toggle">
            <input
              :checked="alert.resolved"
              type="checkbox"
              @change="toggleResolved(alert.id)"
            />
            <span>Resolved</span>
          </label>

          <button
            class="action-button"
            :disabled="alert.resolved"
            @click="markResolved(alert.id)"
          >
            <span class="button-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false">
                <path d="M9.55 18 3.85 12.3l1.41-1.41 4.29 4.29 9.19-9.18 1.41 1.41Z" />
              </svg>
            </span>
            <span>{{ alert.resolved ? 'Resolved' : 'Mark Resolved' }}</span>
          </button>
        </div>
      </article>
    </div>

    <div v-else class="empty-state">
      No alerts match the current severity filter.
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

type AlertSeverity = 'info' | 'warning' | 'critical'

type AdminAlert = {
  id: number
  device: string
  type: string
  severity: AlertSeverity
  message: string
  timestamp: string
  resolved: boolean
}

const sampleAlerts: AdminAlert[] = [
  {
    id: 1,
    device: 'Dryer Unit 1',
    type: 'Session Update',
    severity: 'info',
    message: 'Batch A-17 entered the stabilization stage.',
    timestamp: '2026-04-09T08:15:00.000Z',
    resolved: true
  },
  {
    id: 2,
    device: 'Dryer Unit 2',
    type: 'Moisture Threshold',
    severity: 'warning',
    message: 'Moisture level is above the target band for Batch B-03.',
    timestamp: '2026-04-09T10:20:00.000Z',
    resolved: false
  },
  {
    id: 3,
    device: 'Dryer Unit 3',
    type: 'Temperature Spike',
    severity: 'critical',
    message: 'Critical temperature spike detected. Immediate review recommended.',
    timestamp: '2026-04-09T12:05:00.000Z',
    resolved: false
  }
]

const alerts = ref<AdminAlert[]>([])
const selectedSeverity = ref<'all' | AlertSeverity>('all')

const normalizeAlert = (alert: Partial<AdminAlert>, index: number): AdminAlert => ({
  id: typeof alert.id === 'number' ? alert.id : index + 1,
  device: typeof alert.device === 'string' && alert.device.trim() ? alert.device : 'Unknown Device',
  type: typeof alert.type === 'string' && alert.type.trim() ? alert.type : 'General',
  severity:
    alert.severity === 'info' || alert.severity === 'warning' || alert.severity === 'critical'
      ? alert.severity
      : 'info',
  message: typeof alert.message === 'string' && alert.message.trim() ? alert.message : 'No message provided.',
  timestamp:
    typeof alert.timestamp === 'string' && alert.timestamp.trim()
      ? alert.timestamp
      : new Date().toISOString(),
  resolved: Boolean(alert.resolved)
})

const persistAlerts = () => {
  localStorage.setItem('alerts', JSON.stringify(alerts.value))
}

const loadAlerts = () => {
  const storedAlerts = localStorage.getItem('alerts')

  if (!storedAlerts) {
    alerts.value = sampleAlerts
    persistAlerts()
    return
  }

  try {
    const parsed = JSON.parse(storedAlerts) as Partial<AdminAlert>[]

    if (!Array.isArray(parsed)) {
      alerts.value = sampleAlerts
      persistAlerts()
      return
    }

    alerts.value = parsed.map((alert, index) => normalizeAlert(alert, index))
    persistAlerts()
  } catch {
    alerts.value = sampleAlerts
    persistAlerts()
  }
}

const filteredAlerts = computed(() => {
  const list =
    selectedSeverity.value === 'all'
      ? alerts.value
      : alerts.value.filter((alert) => alert.severity === selectedSeverity.value)

  return [...list].sort(
    (left, right) => new Date(right.timestamp).getTime() - new Date(left.timestamp).getTime()
  )
})

const unresolvedCount = computed(() => alerts.value.filter((alert) => !alert.resolved).length)

const toggleResolved = (id: number) => {
  alerts.value = alerts.value.map((alert) =>
    alert.id === id ? { ...alert, resolved: !alert.resolved } : alert
  )
  persistAlerts()
}

const markResolved = (id: number) => {
  alerts.value = alerts.value.map((alert) =>
    alert.id === id ? { ...alert, resolved: true } : alert
  )
  persistAlerts()
}

const formatTimestamp = (value: string) =>
  new Date(value).toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  })

onMounted(() => {
  loadAlerts()
})
</script>

<style scoped>
.alerts-panel {
  display: grid;
  gap: 20px;
}

.panel-head {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: flex-start;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #d17890;
}

.panel-head h3 {
  margin: 0;
  color: #243042;
}

.panel-head p {
  margin: 10px 0 0;
  color: #5f6d81;
  line-height: 1.6;
}

.summary-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.summary-pill {
  display: inline-flex;
  align-items: center;
  padding: 10px 14px;
  border-radius: 999px;
  background: #fff7f9;
  border: 1px solid #efe1e6;
  color: #526075;
  font-weight: 700;
}

.toolbar {
  display: flex;
  justify-content: flex-start;
}

.filter-field {
  display: grid;
  gap: 8px;
  min-width: 220px;
  color: #526075;
  font-weight: 600;
}

.filter-field select {
  min-height: 48px;
  padding: 0 14px;
  border-radius: 16px;
  border: 1px solid #e6dfe4;
  background: #fffdfd;
  color: #243042;
  font: inherit;
}

.table-shell {
  overflow-x: auto;
  border: 1px solid #f0e6ea;
  border-radius: 22px;
  background: #fffdfd;
}

.alerts-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 960px;
}

.alerts-table th,
.alerts-table td {
  padding: 16px 18px;
  border-bottom: 1px solid #f4ebee;
  text-align: left;
  vertical-align: top;
}

.alerts-table th {
  font-size: 0.84rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #7a8799;
  background: #fff7f9;
}

.alerts-table tbody tr:last-child td {
  border-bottom: none;
}

.message-cell {
  min-width: 280px;
  color: #243042;
}

.severity-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 0.88rem;
  font-weight: 700;
  text-transform: capitalize;
}

.chip-icon {
  width: 16px;
  height: 16px;
  display: inline-flex;
}

.chip-icon svg,
.button-icon svg {
  width: 100%;
  height: 100%;
  fill: currentColor;
  display: block;
}

.severity-info {
  background: #eef7fd;
  color: #4f8ab2;
}

.severity-warning {
  background: #fff7e8;
  color: #b88a2b;
}

.severity-critical {
  background: #fff1f3;
  color: #c05c72;
}

.resolved-toggle {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: #526075;
  font-weight: 600;
}

.resolved-toggle input {
  width: 16px;
  height: 16px;
  accent-color: #d17890;
}

.action-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 40px;
  padding: 0 14px;
  border: 1px solid #ead7de;
  border-radius: 14px;
  background: #fff7f9;
  color: #7a4555;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.action-button:hover:not(:disabled) {
  transform: translateY(-1px);
  background: #ffeef3;
  box-shadow: 0 12px 24px rgba(36, 48, 66, 0.08);
}

.action-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.button-icon {
  width: 16px;
  height: 16px;
  display: inline-flex;
}

.mobile-list {
  display: none;
}

.mobile-card {
  display: grid;
  gap: 14px;
  padding: 18px;
  border-radius: 20px;
  background: #fffdfd;
  border: 1px solid #f0e6ea;
}

.mobile-top {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  align-items: flex-start;
}

.mobile-device {
  margin: 0;
  font-weight: 700;
  color: #243042;
}

.mobile-type,
.mobile-message,
.mobile-meta {
  margin: 0;
  color: #5f6d81;
}

.mobile-message {
  line-height: 1.6;
}

.mobile-meta {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  font-size: 0.92rem;
}

.mobile-actions {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

.empty-state {
  padding: 24px;
  border-radius: 20px;
  background: #fffdfd;
  border: 1px dashed #ead7de;
  color: #7a8799;
  text-align: center;
}

@media (max-width: 920px) {
  .panel-head {
    flex-direction: column;
  }

  .table-shell {
    display: none;
  }

  .mobile-list {
    display: grid;
    gap: 14px;
  }
}

@media (max-width: 640px) {
  .toolbar,
  .filter-field {
    width: 100%;
  }

  .filter-field {
    min-width: 0;
  }

  .mobile-top,
  .mobile-meta,
  .mobile-actions {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
