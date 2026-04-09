<template>
  <section class="admin-shell">
    <aside class="sidebar">
      <div class="sidebar-brand">
        <p class="eyebrow">Admin Panel</p>
        <h2>Cacao Monitor</h2>
        <p class="sidebar-copy">Manage devices, sessions, alerts, and system settings.</p>
      </div>

      <nav class="sidebar-nav" aria-label="Admin navigation">
        <button
          v-for="item in navItems"
          :key="item.key"
          class="sidebar-link"
          :class="{ active: activeSection === item.key }"
          @click="activeSection = item.key"
        >
          <span class="nav-icon" aria-hidden="true">
            <svg v-if="item.key === 'Users'" viewBox="0 0 24 24" focusable="false">
              <path d="M16 11a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm-8 0a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm0 2c-3.33 0-6 1.79-6 4v1h12v-1c0-2.21-2.67-4-6-4Zm8 0c-.29 0-.62 0-1 .05A5.59 5.59 0 0 1 18 17v1h4v-1c0-2.21-2.67-4-6-4Z" />
            </svg>
            <svg v-else-if="item.key === 'Devices'" viewBox="0 0 24 24" focusable="false">
              <path d="M6 3h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-4v2h2v2H8v-2h2v-2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Zm0 2v9h12V5Z" />
            </svg>
            <svg v-else-if="item.key === 'Drying Sessions'" viewBox="0 0 24 24" focusable="false">
              <path d="M5 19h14v2H5Zm1-3h2V8H6Zm5 0h2V4h-2Zm5 0h2v-6h-2Z" />
            </svg>
            <svg v-else-if="item.key === 'Alerts'" viewBox="0 0 24 24" focusable="false">
              <path d="M12 2 1 21h22Zm1 15h-2v2h2Zm0-8h-2v6h2Z" />
            </svg>
            <svg v-else viewBox="0 0 24 24" focusable="false">
              <path d="M19.14 12.94a7.43 7.43 0 0 0 .05-.94 7.43 7.43 0 0 0-.05-.94l2.11-1.65a.5.5 0 0 0 .12-.64l-2-3.46a.48.48 0 0 0-.6-.22l-2.49 1a7.28 7.28 0 0 0-1.63-.94l-.38-2.65A.49.49 0 0 0 13.79 1h-3.58a.49.49 0 0 0-.49.41l-.38 2.65a7.28 7.28 0 0 0-1.63.94l-2.49-1a.48.48 0 0 0-.6.22l-2 3.46a.5.5 0 0 0 .12.64l2.11 1.65a7.43 7.43 0 0 0-.05.94 7.43 7.43 0 0 0 .05.94L2.74 14.6a.5.5 0 0 0-.12.64l2 3.46a.48.48 0 0 0 .6.22l2.49-1a7.28 7.28 0 0 0 1.63.94l.38 2.65a.49.49 0 0 0 .49.41h3.58a.49.49 0 0 0 .49-.41l.38-2.65a7.28 7.28 0 0 0 1.63-.94l2.49 1a.48.48 0 0 0 .6-.22l2-3.46a.5.5 0 0 0-.12-.64ZM12 15.5A3.5 3.5 0 1 1 15.5 12 3.5 3.5 0 0 1 12 15.5Z" />
            </svg>
          </span>
          <span>{{ item.label }}</span>
        </button>
      </nav>
    </aside>

    <div class="admin-content">
      <header class="content-header">
        <div>
          <p class="eyebrow">Administration</p>
          <h1>{{ activeSection }}</h1>
          <p class="content-copy">{{ sectionDescriptions[activeSection] }}</p>
        </div>
      </header>

      <section v-if="activeSection === 'Users'" class="section-stack">
        <AdminUsersManagement :current-user-name="currentUserName" />
      </section>

      <section v-else-if="activeSection === 'Devices'" class="section-stack">
        <AdminDevicesManagement />
      </section>

      <section v-else-if="activeSection === 'Drying Sessions'" class="section-stack">
        <AdminDryingSessionsOverview />
      </section>

      <section v-else-if="activeSection === 'Alerts'" class="section-stack">
        <AdminAlertsPanel />
      </section>

      <section v-else class="section-stack">
        <AdminSettingsPanel />
      </section>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import AdminUsersManagement from '../components/AdminUsersManagement.vue'
import AdminDevicesManagement from '../components/AdminDevicesManagement.vue'
import AdminDryingSessionsOverview from '../components/AdminDryingSessionsOverview.vue'
import AdminAlertsPanel from '../components/AdminAlertsPanel.vue'
import AdminSettingsPanel from '../components/AdminSettingsPanel.vue'

type AdminSection = 'Users' | 'Devices' | 'Drying Sessions' | 'Alerts' | 'Settings'

const props = defineProps<{
  currentUserName: string
}>()

const activeSection = ref<AdminSection>('Users')

const navItems = [
  { key: 'Users' as const, label: 'Users' },
  { key: 'Devices' as const, label: 'Devices' },
  { key: 'Drying Sessions' as const, label: 'Drying Sessions' },
  { key: 'Alerts' as const, label: 'Alerts' },
  { key: 'Settings' as const, label: 'Settings' }
]

const sectionDescriptions: Record<AdminSection, string> = {
  Users: 'Review registered accounts and quick admin-level user information.',
  Devices: 'Monitor the current device details and register new drying units.',
  'Drying Sessions': 'Track live readings, analytics, and historical drying session data.',
  Alerts: 'Review notifications and severity-based system warnings.',
  Settings: 'Keep space ready for future configuration, permissions, and integration controls.'
}

const currentUserName = computed(() => props.currentUserName)

</script>

<style scoped>
.admin-shell {
  min-height: calc(100vh - 112px);
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
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
.content-header h1,
.panel-head h3 {
  margin: 0;
  color: #243042;
}

.sidebar-copy,
.content-copy,
.panel-head p,
.empty-copy {
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

.admin-content {
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

.panel {
  padding: 22px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #efe3e7;
  box-shadow: 0 22px 50px rgba(36, 48, 66, 0.08);
}

.panel-head {
  margin-bottom: 16px;
}

@media (max-width: 1080px) {
  .admin-shell {
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
  .admin-shell {
    padding: 18px 14px 28px;
  }

  .sidebar,
  .panel {
    border-radius: 22px;
  }

  .sidebar-nav {
    grid-template-columns: 1fr;
  }
}
</style>
