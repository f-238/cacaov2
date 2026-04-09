<template>
  <section class="user-shell">
    <aside class="sidebar">
      <div class="sidebar-brand">
        <p class="eyebrow">User Workspace</p>
        <h2>Cacao Monitor</h2>
        <p class="sidebar-copy">View drying progress, sensor history, and device information.</p>
      </div>

      <nav class="sidebar-nav" aria-label="User navigation">
        <button
          v-for="item in navItems"
          :key="item.key"
          class="sidebar-link"
          :class="{ active: activeSection === item.key }"
          @click="activeSection = item.key"
        >
          <span class="nav-icon" aria-hidden="true">
            <svg v-if="item.key === 'Dashboard'" viewBox="0 0 24 24" focusable="false">
              <path d="M3 13h8V3H3Zm10 8h8V11h-8ZM3 21h8v-6H3Zm10-10h8V3h-8Z" />
            </svg>
            <svg v-else-if="item.key === 'History'" viewBox="0 0 24 24" focusable="false">
              <path d="M13 3a9 9 0 1 0 8.95 10h-2.02A7 7 0 1 1 13 5a6.96 6.96 0 0 1 4.24 1.43L14 10h7V3l-2.3 2.3A8.96 8.96 0 0 0 13 3Zm-1 5h2v6h-2Zm0 7h2v2h-2Z" />
            </svg>
            <svg v-else-if="item.key === 'Analytics'" viewBox="0 0 24 24" focusable="false">
              <path d="M5 19h14v2H5Zm1-3h2V8H6Zm5 0h2V4h-2Zm5 0h2v-6h-2Z" />
            </svg>
            <svg v-else-if="item.key === 'Device Info'" viewBox="0 0 24 24" focusable="false">
              <path d="M6 3h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-4v2h2v2H8v-2h2v-2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Zm0 2v9h12V5Z" />
            </svg>
            <svg v-else viewBox="0 0 24 24" focusable="false">
              <path d="M12 2 1 21h22Zm1 15h-2v2h2Zm0-8h-2v6h2Z" />
            </svg>
          </span>
          <span>{{ item.label }}</span>
        </button>
      </nav>
    </aside>

    <div class="user-content">
      <header class="content-header">
        <div>
          <p class="eyebrow">Monitoring</p>
          <h1>{{ activeSection }}</h1>
          <p class="content-copy">{{ sectionDescriptions[activeSection] }}</p>
        </div>
      </header>

      <section v-if="activeSection === 'Dashboard'" class="section-stack">
        <DashboardModern />
      </section>

      <section v-else-if="activeSection === 'History'" class="section-stack">
        <History />
      </section>

      <section v-else-if="activeSection === 'Analytics'" class="section-stack">
        <Analytics />
      </section>

      <section v-else-if="activeSection === 'Device Info'" class="section-stack">
        <DeviceInfo />
      </section>

      <section v-else class="section-stack">
        <Alerts />
      </section>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import DashboardModern from './DashboardModern.vue'
import History from './History.vue'
import Analytics from './Analytics.vue'
import DeviceInfo from './DeviceInfo.vue'
import Alerts from './Alerts.vue'

type UserSection = 'Dashboard' | 'History' | 'Analytics' | 'Device Info' | 'Alerts'

const activeSection = ref<UserSection>('Dashboard')

const navItems = [
  { key: 'Dashboard' as const, label: 'Dashboard' },
  { key: 'History' as const, label: 'History' },
  { key: 'Analytics' as const, label: 'Analytics' },
  { key: 'Device Info' as const, label: 'Device Info' },
  { key: 'Alerts' as const, label: 'Alerts' }
]

const sectionDescriptions: Record<UserSection, string> = {
  Dashboard: 'Monitor the latest sensor readings from the drying device.',
  History: 'Review complete ThingSpeak reading history sorted by newest first.',
  Analytics: 'Inspect moisture and temperature trends for drying performance.',
  'Device Info': 'Check the currently connected device status and last seen time.',
  Alerts: 'Read current warnings, notices, and critical sensor notifications.'
}
</script>

<style scoped>
.user-shell {
  min-height: calc(100vh - 112px);
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
  gap: 24px;
  padding: 24px 20px 32px;
  background:
    radial-gradient(circle at top left, rgba(255, 231, 237, 0.9), transparent 22%),
    radial-gradient(circle at bottom right, rgba(223, 247, 242, 0.9), transparent 26%),
    #fcfcfd;
}

.sidebar {
  position: sticky;
  top: 128px;
  align-self: start;
  padding: 24px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #efe3e7;
  box-shadow: 0 22px 50px rgba(36, 48, 66, 0.08);
}

.sidebar-brand h2,
.content-header h1 {
  margin: 0;
  color: #243042;
}

.sidebar-copy,
.content-copy {
  margin: 10px 0 0;
  color: #5f6d81;
  line-height: 1.6;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #d17890;
}

.sidebar-nav {
  margin-top: 24px;
  display: grid;
  gap: 10px;
}

.sidebar-link {
  width: 100%;
  min-height: 52px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 14px;
  border: 1px solid #eadfe5;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.92);
  color: #526075;
  cursor: pointer;
  text-align: left;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.sidebar-link:hover {
  transform: translateY(-1px);
  background: #fff7f9;
  box-shadow: 0 10px 24px rgba(36, 48, 66, 0.08);
}

.sidebar-link.active {
  background: linear-gradient(135deg, #f3a6ba, #9fd9cc);
  border-color: transparent;
  color: #1f2937;
  font-weight: 700;
}

.nav-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

.nav-icon svg {
  width: 100%;
  height: 100%;
  fill: currentColor;
  display: block;
}

.user-content {
  min-width: 0;
}

.content-header {
  margin-bottom: 20px;
}

.content-header h1 {
  font-size: clamp(1.9rem, 3vw, 2.7rem);
}

.section-stack {
  display: grid;
  gap: 20px;
}

@media (max-width: 1080px) {
  .user-shell {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
  }

  .sidebar-nav {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .user-shell {
    padding: 18px 14px 28px;
  }

  .sidebar {
    border-radius: 22px;
  }

  .sidebar-nav {
    grid-template-columns: 1fr;
  }
}
</style>
