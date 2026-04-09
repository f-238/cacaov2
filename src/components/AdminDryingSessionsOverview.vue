<template>
  <section class="sessions-stack">
    <div class="summary-grid">
      <article class="summary-card">
        <span class="summary-label">Visible Sessions</span>
        <strong>{{ filteredSessions.length }}</strong>
      </article>
      <article class="summary-card">
        <span class="summary-label">Alert Sessions</span>
        <strong>{{ alertSessions }}</strong>
      </article>
    </div>

    <div class="panel">
      <div class="panel-head">
        <div>
          <h3>Drying Sessions Overview</h3>
          <p>Track batches, moisture progress, and session status from one admin view.</p>
        </div>
      </div>

      <div class="filter-row">
        <button
          v-for="option in filterOptions"
          :key="option.value"
          class="filter-chip"
          :class="{ active: activeFilter === option.value }"
          @click="activeFilter = option.value"
        >
          {{ option.label }}
        </button>
      </div>

      <div v-if="filteredSessions.length > 0" class="desktop-table">
        <table>
          <thead>
            <tr>
              <th>Batch Name</th>
              <th>Device</th>
              <th>User</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Current Moisture</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="session in filteredSessions" :key="session.id">
              <td>{{ session.batchName }}</td>
              <td>{{ session.device }}</td>
              <td>{{ session.user }}</td>
              <td>{{ formatDateTime(session.startDate) }}</td>
              <td>{{ session.endDate ? formatDateTime(session.endDate) : 'In progress' }}</td>
              <td>
                <div class="moisture-cell">
                  <span>{{ session.currentMoisture.toFixed(1) }}%</span>
                  <div class="progress-track" aria-hidden="true">
                    <div
                      class="progress-fill"
                      :class="progressClass(session.status)"
                      :style="{ width: `${Math.max(8, Math.min(session.currentMoisture, 100))}%` }"
                    ></div>
                  </div>
                </div>
              </td>
              <td>
                <span class="status-badge" :class="statusClass(session.status)">
                  {{ session.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mobile-cards" v-if="filteredSessions.length > 0">
        <article v-for="session in filteredSessions" :key="`mobile-${session.id}`" class="session-card">
          <div class="session-top">
            <div>
              <h4>{{ session.batchName }}</h4>
              <p>{{ session.device }} · {{ session.user }}</p>
            </div>
            <span class="status-badge" :class="statusClass(session.status)">
              {{ session.status }}
            </span>
          </div>

          <div class="session-meta">
            <span><strong>Start:</strong> {{ formatDateTime(session.startDate) }}</span>
            <span><strong>End:</strong> {{ session.endDate ? formatDateTime(session.endDate) : 'In progress' }}</span>
          </div>

          <div class="moisture-block">
            <div class="moisture-head">
              <strong>Current Moisture</strong>
              <span>{{ session.currentMoisture.toFixed(1) }}%</span>
            </div>
            <div class="progress-track" aria-hidden="true">
              <div
                class="progress-fill"
                :class="progressClass(session.status)"
                :style="{ width: `${Math.max(8, Math.min(session.currentMoisture, 100))}%` }"
              ></div>
            </div>
          </div>
        </article>
      </div>

      <p v-if="filteredSessions.length === 0" class="empty-copy">No sessions match the selected filter.</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

type SessionStatus = 'Active' | 'Completed' | 'Alert'

type DryingSession = {
  id: string
  batchName: string
  device: string
  user: string
  startDate: string
  endDate: string | null
  currentMoisture: number
  status: SessionStatus
}

const seededSessions: DryingSession[] = [
  {
    id: 'session-001',
    batchName: 'Batch A-17',
    device: 'Dryer Unit 1',
    user: 'Maria Santos',
    startDate: '2026-04-09T08:30:00.000Z',
    endDate: null,
    currentMoisture: 31.9,
    status: 'Active'
  },
  {
    id: 'session-002',
    batchName: 'Batch B-03',
    device: 'Dryer Unit 2',
    user: 'Leo Rivera',
    startDate: '2026-04-08T06:00:00.000Z',
    endDate: '2026-04-08T17:30:00.000Z',
    currentMoisture: 12.4,
    status: 'Completed'
  },
  {
    id: 'session-003',
    batchName: 'Batch C-11',
    device: 'Dryer Unit 3',
    user: 'Ana Cruz',
    startDate: '2026-04-09T05:15:00.000Z',
    endDate: null,
    currentMoisture: 38.7,
    status: 'Alert'
  }
]

const filterOptions = [
  { label: 'All', value: 'All' as const },
  { label: 'Active', value: 'Active' as const },
  { label: 'Completed', value: 'Completed' as const },
  { label: 'Alerts', value: 'Alert' as const }
]

const activeFilter = ref<'All' | SessionStatus>('All')
const sessions = ref<DryingSession[]>(loadSessions())

function loadSessions() {
  const storedSessions = localStorage.getItem('dryingSessions')

  if (!storedSessions) {
    localStorage.setItem('dryingSessions', JSON.stringify(seededSessions))
    return seededSessions
  }

  try {
    const parsed = JSON.parse(storedSessions) as DryingSession[]
    return Array.isArray(parsed) && parsed.length > 0 ? parsed : seededSessions
  } catch {
    localStorage.setItem('dryingSessions', JSON.stringify(seededSessions))
    return seededSessions
  }
}

const filteredSessions = computed(() => {
  if (activeFilter.value === 'All') {
    return sessions.value
  }

  return sessions.value.filter((session) => session.status === activeFilter.value)
})

const alertSessions = computed(() => sessions.value.filter((session) => session.status === 'Alert').length)

function formatDateTime(value: string) {
  return new Date(value).toLocaleString()
}

function statusClass(status: SessionStatus) {
  return {
    active: status === 'Active',
    completed: status === 'Completed',
    alert: status === 'Alert'
  }
}

function progressClass(status: SessionStatus) {
  return {
    active: status === 'Active',
    completed: status === 'Completed',
    alert: status === 'Alert'
  }
}
</script>

<style scoped>
.sessions-stack {
  display: grid;
  gap: 20px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.summary-card,
.panel {
  padding: 22px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #efe3e7;
  box-shadow: 0 22px 50px rgba(36, 48, 66, 0.08);
}

.summary-label {
  color: #6b788c;
  font-size: 0.92rem;
  font-weight: 600;
}

.summary-card strong {
  display: block;
  margin-top: 10px;
  font-size: 1.35rem;
  color: #243042;
}

.panel-head {
  margin-bottom: 16px;
}

.panel-head h3 {
  margin: 0;
  color: #243042;
}

.panel-head p,
.empty-copy {
  margin: 10px 0 0;
  color: #5f6d81;
  line-height: 1.6;
}

.filter-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 18px;
}

.filter-chip {
  min-height: 40px;
  padding: 0 14px;
  border: 1px solid #eadfe5;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.88);
  color: #526075;
  cursor: pointer;
  font-weight: 700;
}

.filter-chip.active {
  background: linear-gradient(135deg, #f3a6ba, #9fd9cc);
  border-color: transparent;
  color: #1f2937;
}

.desktop-table {
  display: block;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 14px 12px;
  text-align: left;
  border-bottom: 1px solid #f1e8ec;
}

th {
  color: #526075;
  font-size: 0.92rem;
}

tbody tr:last-child td {
  border-bottom: 0;
}

.moisture-cell {
  min-width: 160px;
  display: grid;
  gap: 8px;
}

.progress-track {
  height: 10px;
  border-radius: 999px;
  background: #f2f4f8;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 999px;
}

.progress-fill.active {
  background: linear-gradient(90deg, #8cc7ea, #9fd9cc);
}

.progress-fill.completed {
  background: linear-gradient(90deg, #9ad8c5, #49a483);
}

.progress-fill.alert {
  background: linear-gradient(90deg, #f3a6ba, #e17f91);
}

.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 0.88rem;
  font-weight: 700;
}

.status-badge.active {
  background: #eef6ff;
  color: #4d7bb5;
}

.status-badge.completed {
  background: #effaf5;
  color: #3b9274;
}

.status-badge.alert {
  background: #fff1f3;
  color: #c05c72;
}

.mobile-cards {
  display: none;
}

.session-card {
  display: grid;
  gap: 14px;
  padding: 18px;
  border-radius: 18px;
  background: #fffdfd;
  border: 1px solid #f3eaee;
}

.session-top {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.session-top h4 {
  margin: 0;
  color: #243042;
}

.session-top p,
.session-meta {
  margin: 6px 0 0;
  color: #607085;
}

.session-meta {
  display: grid;
  gap: 6px;
}

.moisture-block {
  display: grid;
  gap: 8px;
}

.moisture-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  color: #243042;
}

@media (max-width: 720px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }

  .desktop-table {
    display: none;
  }

  .mobile-cards {
    display: grid;
    gap: 12px;
  }

  .summary-card,
  .panel {
    border-radius: 22px;
  }

  .session-top {
    flex-direction: column;
  }
}
</style>
