<script setup lang="ts">
import { computed, ref } from 'vue'
import Register from './views/Register.vue'
import Login from './views/Login.vue'
import AdminDashboard from './views/AdminDashboard.vue'
import UserDashboard from './views/UserDashboard.vue'
import {
  fetchCurrentUser,
  logoutUser,
  toFrontendAuthUser,
  type FrontendAuthUser
} from './services/auth'
import {
  clearAppliedUserSettings,
  syncUserSettingsFromBackend
} from './services/userSettings'

const authScreen = ref<'Login' | 'Register'>('Login')
const currentUser = ref<FrontendAuthUser | null>(loadStoredUser())

function loadStoredUser(): FrontendAuthUser | null {
  const storedUser = localStorage.getItem('authUser')

  if (!storedUser) {
    return null
  }

  try {
    const parsed = JSON.parse(storedUser) as Partial<FrontendAuthUser>

    return {
      fullName: typeof parsed.fullName === 'string' ? parsed.fullName : '',
      email: typeof parsed.email === 'string' ? parsed.email : '',
      role: parsed.role === 'Admin' ? 'Admin' : 'Viewer'
    }
  } catch {
    clearStoredSession()
    return null
  }
}

function clearStoredSession() {
  localStorage.removeItem('authUser')
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
}

const handleLoginSuccess = async (user: FrontendAuthUser) => {
  currentUser.value = user
  localStorage.setItem('authUser', JSON.stringify(user))

  const token = localStorage.getItem('accessToken')
  if (!token) {
    return
  }

  await loadAndApplyUserSettings(token)
}

const handleRegisterSuccess = () => {
  authScreen.value = 'Login'
}

const handleProfileUpdated = (payload: { fullName: string; email: string }) => {
  if (!currentUser.value) {
    return
  }

  currentUser.value = {
    ...currentUser.value,
    fullName: payload.fullName,
    email: payload.email
  }
  localStorage.setItem('authUser', JSON.stringify(currentUser.value))
}

const logout = async () => {
  if (!window.confirm('Sign out from this account on this device?')) {
    return
  }

  const accessToken = localStorage.getItem('accessToken')
  const refreshToken = localStorage.getItem('refreshToken')

  if (accessToken) {
    try {
      await logoutUser({ accessToken, refreshToken })
    } catch {
      // Clear local session even if backend logout fails.
    }
  }

  currentUser.value = null
  clearStoredSession()
  clearAppliedUserSettings()
  authScreen.value = 'Login'
}

const isAdmin = computed(() => currentUser.value?.role === 'Admin')

const loadAndApplyUserSettings = async (token: string) => {
  try {
    await syncUserSettingsFromBackend(token)
  } catch {
    clearAppliedUserSettings()
  }
}

const accessToken = localStorage.getItem('accessToken')

if (accessToken) {
  loadAndApplyUserSettings(accessToken)
}

if (accessToken && !currentUser.value) {
  fetchCurrentUser(accessToken)
    .then((user) => {
      const frontendUser = toFrontendAuthUser(user)
      currentUser.value = frontendUser
      localStorage.setItem('authUser', JSON.stringify(frontendUser))
    })
    .catch(() => {
      clearStoredSession()
    })
}
</script>

<template>
  <div class="app-shell">
    <template v-if="currentUser">
      <main class="content">
        <AdminDashboard
          v-if="isAdmin"
          :current-user-name="currentUser.fullName"
          @sign-out="logout"
        />
        <UserDashboard
          v-else
          :current-user-name="currentUser.fullName"
          @sign-out="logout"
          @profile-updated="handleProfileUpdated"
        />
      </main>
    </template>

    <template v-else>
      <header class="auth-topbar">
        <div class="auth-topbar-copy">
          <p class="eyebrow">Cacao Drying Monitor</p>
          <h1>Secure Access</h1>
          <p class="subtitle">
            Sign in or create an account first. Protected monitoring views stay hidden until login.
          </p>
        </div>

        <nav class="auth-nav" aria-label="Authentication navigation">
          <button
            class="auth-nav-button"
            :class="{ active: authScreen === 'Login' }"
            @click="authScreen = 'Login'"
          >
            Login
          </button>
          <button
            class="auth-nav-button"
            :class="{ active: authScreen === 'Register' }"
            @click="authScreen = 'Register'"
          >
            Register
          </button>
        </nav>
      </header>

      <main class="content">
        <Login
          v-if="authScreen === 'Login'"
          @login-success="handleLoginSuccess"
          @switch-auth="authScreen = $event"
        />
        <Register
          v-else
          @register-success="handleRegisterSuccess"
          @switch-auth="authScreen = $event"
        />
      </main>
    </template>
  </div>
</template>

<style>
:root {
  --user-primary-color: #1f2937;
  --user-secondary-color: #526075;
  --user-accent-color: #f3a6ba;
  --app-font-scale: 1;
  --app-text-color: #17202b;
  --app-text-secondary: #546170;
  --app-text-tertiary: #768394;
  --app-muted-color: #6f7b8c;
  --app-bg: #f3f5f7;
  --app-bg-overlay-1: rgba(255, 255, 255, 0.7);
  --app-bg-overlay-2: rgba(223, 229, 236, 0.9);
  --app-surface-bg: rgba(255, 255, 255, 0.78);
  --app-surface-strong: rgba(255, 255, 255, 0.92);
  --app-surface-muted: rgba(245, 247, 250, 0.92);
  --app-border-color: rgba(199, 208, 218, 0.9);
  --app-border-strong: rgba(150, 164, 179, 0.9);
  --app-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
  --app-shadow-strong: 0 28px 60px rgba(15, 23, 42, 0.12);
  --app-chip-bg: rgba(240, 244, 248, 0.95);
  --app-success-bg: rgba(219, 246, 235, 0.92);
  --app-success-text: #146c43;
  --app-danger-bg: rgba(254, 234, 234, 0.92);
  --app-danger-text: #b42318;
  --app-warning-bg: rgba(255, 244, 214, 0.92);
  --app-warning-text: #9a6700;
  --app-info-bg: rgba(229, 241, 255, 0.92);
  --app-info-text: #1d4ed8;
  --app-focus-ring: 0 0 0 4px rgba(15, 23, 42, 0.08);
  font-family: 'Segoe UI Variable Text', 'IBM Plex Sans', 'Segoe UI', sans-serif;
  color: var(--app-text-color);
  background: var(--app-bg);
}

html {
  font-size: calc(16px * var(--app-font-scale));
  scroll-behavior: smooth;
}

* {
  box-sizing: border-box;
}

html,
body,
#app {
  min-height: 100%;
}

body {
  margin: 0;
  color: var(--app-text-color);
  background:
    radial-gradient(circle at top left, var(--app-bg-overlay-1), transparent 24%),
    radial-gradient(circle at bottom right, var(--app-bg-overlay-2), transparent 28%),
    var(--app-bg);
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
  accent-color: var(--user-accent-color);
}

body.theme-dark {
  --app-text-color: #e7ecf2;
  --app-text-secondary: #aab4c1;
  --app-text-tertiary: #8d98a8;
  --app-muted-color: #95a2b3;
  --app-bg: #0b1220;
  --app-bg-overlay-1: rgba(31, 41, 55, 0.62);
  --app-bg-overlay-2: rgba(17, 24, 39, 0.96);
  --app-surface-bg: rgba(15, 23, 42, 0.72);
  --app-surface-strong: rgba(17, 24, 39, 0.9);
  --app-surface-muted: rgba(27, 36, 52, 0.92);
  --app-border-color: rgba(66, 77, 95, 0.92);
  --app-border-strong: rgba(96, 109, 130, 0.92);
  --app-shadow: 0 18px 40px rgba(2, 6, 23, 0.3);
  --app-shadow-strong: 0 28px 60px rgba(2, 6, 23, 0.38);
  --app-chip-bg: rgba(31, 41, 55, 0.95);
  --app-success-bg: rgba(9, 57, 41, 0.9);
  --app-success-text: #8de2bc;
  --app-danger-bg: rgba(78, 25, 29, 0.92);
  --app-danger-text: #f7b4b8;
  --app-warning-bg: rgba(84, 55, 18, 0.92);
  --app-warning-text: #f1d08f;
  --app-info-bg: rgba(22, 52, 104, 0.92);
  --app-info-text: #b6d2ff;
  --app-focus-ring: 0 0 0 4px rgba(148, 163, 184, 0.14);
  color-scheme: dark;
}

body::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

body::-webkit-scrollbar-thumb {
  background: var(--app-border-strong);
  border-radius: 999px;
}

body::-webkit-scrollbar-track {
  background: transparent;
}

button,
input,
textarea,
select {
  font: inherit;
}

a {
  color: inherit;
}

.app-shell {
  min-height: 100vh;
}

.auth-topbar {
  position: sticky;
  top: 0;
  z-index: 20;
  padding: 24px 20px 14px;
  backdrop-filter: blur(22px);
  background: linear-gradient(180deg, var(--app-surface-strong), rgba(255, 255, 255, 0));
}

.auth-topbar-copy {
  max-width: 1120px;
  margin: 0 auto 16px;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--app-text-tertiary);
}

.auth-topbar h1 {
  margin: 0;
  font-size: clamp(1.75rem, 4vw, 3rem);
  color: var(--app-text-color);
  letter-spacing: -0.03em;
}

.subtitle {
  margin: 10px 0 0;
  color: var(--app-text-secondary);
  line-height: 1.65;
  max-width: 720px;
}

.auth-nav-button {
  min-height: 44px;
  padding: 0 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
  border: 1px solid var(--app-border-color);
  background: var(--app-surface-bg);
  color: var(--app-text-secondary);
}

.auth-nav-button:hover {
  transform: translateY(-1px);
  background: var(--app-surface-strong);
  border-color: var(--app-border-strong);
}

.auth-nav {
  max-width: 1120px;
  margin: 0 auto;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.auth-nav-button.active {
  background: var(--app-surface-muted);
  border-color: var(--app-border-strong);
  color: var(--app-text-color);
  font-weight: 700;
  box-shadow: inset 3px 0 0 var(--user-accent-color);
}

.content {
  min-height: 100vh;
}

:is(
  .login-shell,
  .register-shell,
  .user-shell,
  .admin-shell,
  .dashboard-shell,
  .history-shell,
  .analytics-shell,
  .device-shell,
  .alerts-shell,
  .settings-shell
) {
  background: transparent !important;
}

:is(.login-shell, .register-shell) {
  min-height: calc(100vh - 148px) !important;
  padding: 28px 20px 42px !important;
  display: grid !important;
  place-items: center !important;
}

:is(.login-card, .register-card) {
  width: min(100%, 540px) !important;
  background: var(--app-surface-strong) !important;
  border: 1px solid var(--app-border-color) !important;
  border-radius: 22px !important;
  box-shadow: var(--app-shadow-strong) !important;
  backdrop-filter: blur(22px);
}

.login-image-wrap {
  background: transparent !important;
  padding: 18px 18px 0 !important;
}

.login-image {
  height: 200px !important;
  border-radius: 18px !important;
  box-shadow: var(--app-shadow) !important;
}

:is(.login-copy, .register-copy) {
  padding: 22px 28px 8px !important;
  margin-bottom: 0 !important;
}

.login-copy h1,
.register-copy h1 {
  margin: 0 !important;
  font-size: clamp(1.7rem, 4vw, 2.4rem) !important;
  line-height: 1.08 !important;
  letter-spacing: -0.03em;
  color: var(--app-text-color) !important;
}

.login-copy .subtitle,
.register-copy .subtitle {
  margin-top: 10px !important;
  max-width: none !important;
}

:is(.login-form, .register-form) {
  gap: 14px !important;
  padding: 0 28px 6px !important;
}

:is(.field, .filter-field) {
  gap: 8px !important;
}

:is(.field span, .field-label, .filter-field span, .summary-label, .toolbar-note, .token-note, .signout-copy, .autosave-copy, .timestamp, .meta-item, .serial, .mobile-type, .panel-head p, .empty-copy) {
  color: var(--app-text-secondary) !important;
}

:is(input, select, textarea, .inline-input) {
  min-height: 46px;
  border: 1px solid var(--app-border-color) !important;
  border-radius: 12px !important;
  background: var(--app-surface-muted) !important;
  color: var(--app-text-color) !important;
  box-shadow: none !important;
}

:is(input, select, textarea)::placeholder {
  color: var(--app-text-tertiary) !important;
}

:is(input, select, textarea, .inline-input):focus {
  outline: none;
  border-color: var(--app-border-strong) !important;
  box-shadow: var(--app-focus-ring) !important;
}

.input-group .icon,
.search-icon,
.button-icon,
.nav-icon,
.title-icon,
.card-icon,
.chart-icon,
.alert-icon {
  color: var(--app-text-tertiary) !important;
}

:is(
  .summary-card,
  .panel,
  .table-card,
  .chart-card,
  .metric-card,
  .chart-section,
  .integration-card,
  .token-card,
  .form-card,
  .list-card,
  .settings-card,
  .alert-card,
  .user-card,
  .device-card,
  .session-card,
  .mobile-card,
  .device-row,
  .table-shell
) {
  background: var(--app-surface-strong) !important;
  border: 1px solid var(--app-border-color) !important;
  border-radius: 20px !important;
  box-shadow: var(--app-shadow) !important;
}

:is(.summary-card, .panel, .table-card, .chart-card, .metric-card, .chart-section, .integration-card, .token-card, .form-card, .list-card, .settings-card) {
  backdrop-filter: blur(18px);
}

:is(.summary-card strong, .metric-value, .token-title, h1, h2, h3, h4, .user-name) {
  color: var(--app-text-color) !important;
}

:is(.metric-note, .card-head, .metric-label, .toolbar-copy p, .chart-copy p, .integration-copy p, .token-serial, .mobile-message, .message-cell, .card-meta, .session-meta, .moisture-head strong) {
  color: var(--app-text-secondary) !important;
}

:is(.summary-pill, .status-pill, .pill, .severity-chip, .metric-chip, .severity-badge, .status-badge, .resolved-toggle, .role-pill) {
  border: 1px solid var(--app-border-color) !important;
  background: var(--app-chip-bg) !important;
  color: var(--app-text-secondary) !important;
  box-shadow: none !important;
}

:is(.status-pill.is-online, .status-badge.online, .status-badge.active, .severity-chip.severity-info, .badge-info) {
  background: var(--app-info-bg) !important;
  color: var(--app-info-text) !important;
  border-color: transparent !important;
}

:is(.status-pill.is-offline, .status-badge.offline, .severity-chip.severity-critical, .badge-critical, .pill.inactive) {
  background: var(--app-danger-bg) !important;
  color: var(--app-danger-text) !important;
  border-color: transparent !important;
}

:is(.severity-chip.severity-warning, .badge-warning, .status-badge.alert, .pill.pending) {
  background: var(--app-warning-bg) !important;
  color: var(--app-warning-text) !important;
  border-color: transparent !important;
}

:is(.status-badge.completed, .pill.active) {
  background: var(--app-success-bg) !important;
  color: var(--app-success-text) !important;
  border-color: transparent !important;
}

:is(.status-dot) {
  background: #22c55e !important;
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.12) !important;
}

:is(.primary-button, .login-button, .register-button, .export-button, .save-button) {
  border: 1px solid transparent !important;
  background: var(--app-text-color) !important;
  color: #f8fafc !important;
  box-shadow: var(--app-shadow) !important;
}

:is(.primary-button, .login-button, .register-button, .export-button, .save-button):hover {
  transform: translateY(-1px);
}

:is(.secondary-button, .action-button, .auth-nav-button, .segmented-button, .filter-chip) {
  border: 1px solid var(--app-border-color) !important;
  background: var(--app-surface-bg) !important;
  color: var(--app-text-secondary) !important;
  box-shadow: none !important;
}

:is(.secondary-button, .action-button, .auth-nav-button, .segmented-button, .filter-chip):hover {
  border-color: var(--app-border-strong) !important;
  background: var(--app-surface-strong) !important;
}

:is(.segmented-button.active, .filter-chip.active) {
  background: var(--app-surface-muted) !important;
  border-color: var(--app-border-strong) !important;
  color: var(--app-text-color) !important;
  box-shadow: inset 3px 0 0 var(--user-accent-color) !important;
}

.danger-button,
.sidebar-signout,
.action-button.delete,
.icon-button.delete {
  background: var(--app-danger-bg) !important;
  color: var(--app-danger-text) !important;
  border-color: transparent !important;
}

.message {
  border-radius: 12px !important;
  border: 1px solid transparent !important;
}

.message.error {
  background: var(--app-danger-bg) !important;
  color: var(--app-danger-text) !important;
}

.message.success {
  background: var(--app-success-bg) !important;
  color: var(--app-success-text) !important;
}

:is(.user-shell, .admin-shell) {
  min-height: 100vh !important;
  padding: 18px !important;
  gap: 18px !important;
}

:is(.user-shell .sidebar, .admin-shell .sidebar) {
  background: var(--app-surface-strong) !important;
  border: 1px solid var(--app-border-color) !important;
  box-shadow: var(--app-shadow) !important;
  border-radius: 20px !important;
  top: 18px !important;
  max-height: calc(100vh - 36px) !important;
}

:is(.user-shell .sidebar-toggle, .admin-shell .sidebar-toggle) {
  background: var(--app-surface-muted) !important;
  border: 1px solid var(--app-border-color) !important;
  color: var(--app-text-secondary) !important;
}

:is(.user-shell .sidebar-user, .admin-shell .sidebar-user) {
  background: var(--app-surface-muted) !important;
  border-color: var(--app-border-color) !important;
}

:is(.user-shell .user-avatar, .admin-shell .user-avatar) {
  background: var(--app-text-color) !important;
  color: #f8fafc !important;
}

:is(.user-shell .sidebar-link, .admin-shell .sidebar-link) {
  min-height: 46px !important;
  border-radius: 12px !important;
  background: transparent !important;
  border: 1px solid transparent !important;
  color: var(--app-text-secondary) !important;
}

:is(.user-shell .sidebar-link.active, .admin-shell .sidebar-link.active) {
  background: var(--app-surface-muted) !important;
  border-color: var(--app-border-color) !important;
  color: var(--app-text-color) !important;
  box-shadow: inset 3px 0 0 var(--user-accent-color) !important;
}

:is(.content-header, .dashboard-header, .history-header, .analytics-header, .device-header, .alerts-header) {
  margin-bottom: 18px !important;
}

:is(.content-header h1, .dashboard-header h1, .history-header h1, .analytics-header h1, .device-header h1, .alerts-header h1) {
  font-size: clamp(1.8rem, 3vw, 2.6rem) !important;
  line-height: 1.05 !important;
  letter-spacing: -0.03em;
}

:is(.dashboard-header, .history-header, .analytics-header, .device-header, .alerts-header) {
  max-width: 1120px !important;
  margin-left: auto !important;
  margin-right: auto !important;
}

:is(.cards, .chart-grid, .device-grid, .summary-grid) {
  gap: 16px !important;
}

:is(.table-scroll table, .desktop-table table, .alerts-table) {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

:is(.table-scroll thead th, .desktop-table thead th, .alerts-table thead th) {
  padding: 14px 16px;
  text-align: left;
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--app-text-tertiary) !important;
  border-bottom: 1px solid var(--app-border-color);
}

:is(.table-scroll tbody td, .desktop-table tbody td, .alerts-table tbody td) {
  padding: 14px 16px;
  color: var(--app-text-secondary) !important;
  border-bottom: 1px solid rgba(127, 140, 157, 0.14);
  vertical-align: middle;
}

:is(.table-scroll tbody tr:last-child td, .desktop-table tbody tr:last-child td, .alerts-table tbody tr:last-child td) {
  border-bottom: 0;
}

:is(.empty-state, .empty-copy) {
  padding: 20px !important;
  border-radius: 16px !important;
  background: var(--app-surface-muted) !important;
  border: 1px dashed var(--app-border-color) !important;
  color: var(--app-text-secondary) !important;
}

:is(.chart-placeholder, .integration-preview) {
  background: linear-gradient(180deg, var(--app-surface-muted), var(--app-surface-bg)) !important;
  border: 1px solid var(--app-border-color) !important;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

:is(.preview-grid, .chart-grid) {
  opacity: 0.55;
}

:is(.login-card, .register-card, .summary-card, .panel, .table-card, .chart-card, .metric-card, .chart-section, .integration-card, .token-card, .form-card, .list-card, .settings-card, .alert-card, .device-row) {
  animation: card-enter 0.35s ease;
}

@keyframes card-enter {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 640px) {
  .auth-topbar {
    padding: 18px 14px 12px;
  }

  .auth-topbar-copy {
    margin-bottom: 14px;
  }

  .auth-nav {
    gap: 8px;
  }

  .auth-nav-button {
    min-height: 40px;
    padding: 0 12px;
    font-size: 0.94rem;
  }

  :is(.login-shell, .register-shell) {
    padding: 18px 14px 28px !important;
  }

  :is(.login-card, .register-card) {
    width: 100% !important;
  }

  :is(.login-copy, .register-copy, .login-form, .register-form, .switch-copy) {
    padding-left: 20px !important;
    padding-right: 20px !important;
  }

  :is(.user-shell, .admin-shell) {
    padding: 14px !important;
  }

  :is(.dashboard-shell, .history-shell, .analytics-shell, .device-shell, .alerts-shell) {
    padding: 20px 0 28px !important;
  }
}
</style>
