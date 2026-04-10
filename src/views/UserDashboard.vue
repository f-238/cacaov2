<template>
  <section class="user-shell" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
    <aside class="sidebar" :class="{ collapsed: isSidebarCollapsed }">
      <div class="sidebar-top">
        <div class="sidebar-brand">
          <p class="eyebrow">User Workspace</p>
          <h2>Cacao Monitor</h2>
          <p class="sidebar-copy">View drying progress, sensor history, and device information.</p>
        </div>
        <button
          class="sidebar-toggle"
          type="button"
          :aria-label="isSidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
          @click="toggleSidebar"
        >
          <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
            <path d="M9.29 6.71 13.58 11l-4.29 4.29 1.42 1.42L16.42 11l-5.71-5.71Z" />
          </svg>
        </button>
      </div>

      <div class="sidebar-user">
        <span class="user-avatar">{{ userInitials }}</span>
        <div class="user-meta">
          <span class="user-name">{{ props.currentUserName }}</span>
          <span class="user-role">Viewer</span>
        </div>
      </div>

      <nav class="sidebar-nav" aria-label="User navigation">
        <button
          v-for="item in navItems"
          :key="item.key"
          class="sidebar-link"
          :class="{ active: activeSection === item.key }"
          :aria-label="item.label"
          :title="isSidebarCollapsed ? item.label : undefined"
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
            <svg v-else-if="item.key === 'Settings'" viewBox="0 0 24 24" focusable="false">
              <path d="M19.14 12.94a7.43 7.43 0 0 0 .05-.94 7.43 7.43 0 0 0-.05-.94l2.11-1.65a.5.5 0 0 0 .12-.64l-2-3.46a.48.48 0 0 0-.6-.22l-2.49 1a7.28 7.28 0 0 0-1.63-.94l-.38-2.65A.49.49 0 0 0 13.79 1h-3.58a.49.49 0 0 0-.49.41l-.38 2.65a7.28 7.28 0 0 0-1.63.94l-2.49-1a.48.48 0 0 0-.6.22l-2 3.46a.5.5 0 0 0 .12.64l2.11 1.65a7.43 7.43 0 0 0-.05.94 7.43 7.43 0 0 0 .05.94L2.74 14.6a.5.5 0 0 0-.12.64l2 3.46a.48.48 0 0 0 .6.22l2.49-1a7.28 7.28 0 0 0 1.63.94l.38 2.65a.49.49 0 0 0 .49.41h3.58a.49.49 0 0 0 .49-.41l.38-2.65a7.28 7.28 0 0 0 1.63-.94l2.49 1a.48.48 0 0 0 .6-.22l2-3.46a.5.5 0 0 0-.12-.64ZM12 15.5A3.5 3.5 0 1 1 15.5 12 3.5 3.5 0 0 1 12 15.5Z" />
            </svg>
            <svg v-else viewBox="0 0 24 24" focusable="false">
              <path d="M12 2 1 21h22Zm1 15h-2v2h2Zm0-8h-2v6h2Z" />
            </svg>
          </span>
          <span class="nav-label">{{ item.label }}</span>
        </button>
      </nav>

      <button
        class="sidebar-signout"
        type="button"
        aria-label="Sign Out"
        :title="isSidebarCollapsed ? 'Sign Out' : undefined"
        @click="emit('sign-out')"
      >
        <span class="nav-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" focusable="false">
            <path d="M10 17v-2h4V9h-4V7h6v10Zm-4 4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7v2H6v14h7v2Zm11-4-1.41-1.41L18.17 13H9v-2h9.17l-2.58-2.59L17 7l5 5Z" />
          </svg>
        </span>
        <span class="nav-label">Sign Out</span>
      </button>
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

      <section v-else-if="activeSection === 'Settings'" class="section-stack">
        <Settings @sign-out="emit('sign-out')" @profile-updated="emit('profile-updated', $event)" />
      </section>

      <section v-else class="section-stack">
        <Alerts />
      </section>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import DashboardModern from './DashboardModern.vue'
import History from './History.vue'
import Analytics from './Analytics.vue'
import DeviceInfo from './DeviceInfo.vue'
import Settings from './Settings.vue'
import Alerts from './Alerts.vue'

type UserSection = 'Dashboard' | 'History' | 'Analytics' | 'Device Info' | 'Settings' | 'Alerts'

const props = defineProps<{
  currentUserName: string
}>()

const emit = defineEmits<{
  'sign-out': []
  'profile-updated': [payload: { fullName: string; email: string }]
}>()

const activeSection = ref<UserSection>('Dashboard')
const isSidebarCollapsed = ref(false)

const navItems = [
  { key: 'Dashboard' as const, label: 'Dashboard' },
  { key: 'History' as const, label: 'History' },
  { key: 'Analytics' as const, label: 'Analytics' },
  { key: 'Device Info' as const, label: 'Device Info' },
  { key: 'Settings' as const, label: 'Settings' },
  { key: 'Alerts' as const, label: 'Alerts' }
]

const sectionDescriptions: Record<UserSection, string> = {
  Dashboard: 'Monitor the latest backend-ingested sensor readings from your drying device.',
  History: 'Review complete device reading history sorted by newest first.',
  Analytics: 'Inspect moisture and temperature trends for drying performance.',
  'Device Info': 'Check the currently connected device status and last seen time.',
  Settings: 'Customize appearance, profile details, and account session actions.',
  Alerts: 'Read current warnings, notices, and critical sensor notifications.'
}

const userInitials = computed(() => {
  const normalized = props.currentUserName.trim()
  if (!normalized) {
    return 'U'
  }

  return normalized
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? '')
    .join('')
})

function toggleSidebar() {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}
</script>

<style scoped>
.user-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 272px minmax(0, 1fr);
  gap: 24px;
  padding: 20px;
  background:
    radial-gradient(circle at top left, rgba(255, 231, 237, 0.9), transparent 22%),
    radial-gradient(circle at bottom right, rgba(223, 247, 242, 0.9), transparent 26%),
    #fcfcfd;
}

.user-shell.sidebar-collapsed {
  grid-template-columns: 92px minmax(0, 1fr);
}

.sidebar {
  position: sticky;
  top: 20px;
  max-height: calc(100vh - 40px);
  align-self: start;
  padding: 18px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #efe3e7;
  box-shadow: 0 22px 50px rgba(36, 48, 66, 0.08);
  display: grid;
  grid-template-rows: auto auto 1fr auto;
  gap: 14px;
}

.sidebar-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}

.sidebar-toggle {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  border: 1px solid #eadfe5;
  background: #fff;
  color: #526075;
  cursor: pointer;
  display: grid;
  place-items: center;
}

.sidebar-toggle svg {
  width: 20px;
  height: 20px;
  fill: currentColor;
}

.sidebar.collapsed .sidebar-toggle svg {
  transform: rotate(180deg);
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

.sidebar-user {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid #efe3e7;
}

.user-avatar {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  font-weight: 700;
  font-size: 0.86rem;
  color: #1f2937;
  background: linear-gradient(135deg, #f3a6ba, #9fd9cc);
}

.user-meta {
  min-width: 0;
  display: grid;
}

.user-name,
.user-role {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.user-name {
  font-weight: 700;
  color: #243042;
}

.user-role {
  font-size: 0.8rem;
  color: #5f6d81;
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
  display: grid;
  gap: 10px;
  align-content: start;
}

.sidebar-link,
.sidebar-signout {
  width: 100%;
  min-height: 50px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 12px;
  border: 1px solid #eadfe5;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.92);
  color: #526075;
  cursor: pointer;
  text-align: left;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.sidebar-link:hover,
.sidebar-signout:hover {
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

.sidebar-signout {
  color: #b33f5a;
  background: #fff1f3;
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

.nav-label {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.sidebar.collapsed .sidebar-brand h2,
.sidebar.collapsed .sidebar-copy,
.sidebar.collapsed .user-meta,
.sidebar.collapsed .nav-label,
.sidebar.collapsed .eyebrow {
  display: none;
}

.sidebar.collapsed .sidebar-link,
.sidebar.collapsed .sidebar-signout {
  justify-content: center;
  padding: 0;
}

.sidebar.collapsed .sidebar-user {
  justify-content: center;
  padding: 8px;
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
  .user-shell,
  .user-shell.sidebar-collapsed {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
    max-height: none;
  }

  .sidebar-nav {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .user-shell {
    padding: 14px;
  }

  .sidebar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px;
    border-radius: 22px;
    overflow: hidden;
    position: sticky;
    top: 8px;
    z-index: 30;
    backdrop-filter: blur(12px);
  }

  .sidebar-top,
  .sidebar-user {
    display: none;
  }

  .sidebar-nav {
    flex: 1;
    display: flex;
    gap: 8px;
    align-items: center;
    overflow-x: auto;
    overflow-y: hidden;
    white-space: nowrap;
    scrollbar-width: thin;
  }

  .sidebar-link {
    width: 42px;
    min-height: 42px;
    padding: 0;
    flex: 0 0 auto;
    border-radius: 12px;
    justify-content: center;
  }

  .sidebar-signout {
    width: 42px;
    min-height: 42px;
    padding: 0;
    flex: 0 0 auto;
    justify-content: center;
    border-radius: 12px;
  }

  .sidebar-signout .nav-label {
    display: none;
  }

  .sidebar-link .nav-label,
  .sidebar.collapsed .nav-label,
  .sidebar.collapsed .sidebar-signout .nav-label {
    display: none;
  }

  .sidebar.collapsed .sidebar-link {
    justify-content: center;
    padding: 0;
  }

  .sidebar.collapsed .sidebar-signout {
    justify-content: center;
    padding: 0;
  }
}
</style>
