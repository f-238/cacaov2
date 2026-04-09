<script setup lang="ts">
import { computed, ref } from 'vue'
import Register from './views/Register.vue'
import Login from './views/Login.vue'
import AdminDashboard from './views/AdminDashboard.vue'
import UserDashboard from './views/UserDashboard.vue'
import { fetchCurrentUser, toFrontendAuthUser } from './services/auth'

type AuthUser = {
  fullName: string
  email: string
  role: 'Admin' | 'Manager' | 'Viewer'
}

const authScreen = ref<'Login' | 'Register'>('Login')
const currentUser = ref<AuthUser | null>(loadStoredUser())

function loadStoredUser(): AuthUser | null {
  const storedUser = localStorage.getItem('authUser')

  if (!storedUser) {
    return null
  }

  try {
    const parsed = JSON.parse(storedUser) as Partial<AuthUser>

    return {
      fullName: typeof parsed.fullName === 'string' ? parsed.fullName : '',
      email: typeof parsed.email === 'string' ? parsed.email : '',
      role: parsed.role === 'Admin' || parsed.role === 'Viewer'
        ? parsed.role
        : 'Viewer'
    }
  } catch {
    localStorage.removeItem('authUser')
    return null
  }
}

const handleLoginSuccess = (user: AuthUser) => {
  currentUser.value = user
  localStorage.setItem('authUser', JSON.stringify(user))
}

const handleRegisterSuccess = () => {
  authScreen.value = 'Login'
}

const logout = () => {
  currentUser.value = null
  localStorage.removeItem('authUser')
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  authScreen.value = 'Login'
}

const isAdmin = computed(() => currentUser.value?.role === 'Admin')

const accessToken = localStorage.getItem('accessToken')

if (accessToken && !currentUser.value) {
  fetchCurrentUser(accessToken)
    .then((user) => {
      const frontendUser = toFrontendAuthUser(user)
      currentUser.value = frontendUser
      localStorage.setItem('authUser', JSON.stringify(frontendUser))
    })
    .catch(() => {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('authUser')
    })
}
</script>

<template>
  <div class="app-shell">
    <template v-if="currentUser">
      <header class="topbar">
        <div class="topbar-copy">
          <div class="topbar-main">
            <div>
              <p class="eyebrow">Cacao Drying Monitor</p>
              <h1>{{ isAdmin ? 'Admin Dashboard' : 'User Dashboard' }}</h1>
              <p class="subtitle">
                {{ isAdmin
                  ? 'Responsive admin workspace for users, devices, drying sessions, alerts, and settings.'
                  : 'Protected monitoring workspace for sensor readings, history, analytics, and device status.' }}
              </p>
            </div>

            <div class="user-pill">
              <span class="user-name">{{ currentUser.fullName }}</span>
              <span class="role-pill">{{ currentUser.role }}</span>
              <button class="logout-button" @click="logout">Logout</button>
            </div>
          </div>
        </div>

      </header>

      <main class="content">
        <AdminDashboard v-if="isAdmin" :current-user-name="currentUser.fullName" />
        <UserDashboard v-else />
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
  font-family: 'Inter', 'Poppins', 'Roboto', sans-serif;
  color: #243042;
  background: #fcfcfd;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background:
    radial-gradient(circle at top left, rgba(255, 229, 235, 0.7), transparent 22%),
    radial-gradient(circle at top right, rgba(223, 246, 240, 0.8), transparent 24%),
    #fcfcfd;
}

button,
input,
textarea,
select {
  font: inherit;
}

.app-shell {
  min-height: 100vh;
}

.topbar,
.auth-topbar {
  position: sticky;
  top: 0;
  z-index: 20;
  padding: 18px 20px 16px;
  backdrop-filter: blur(16px);
  background: rgba(252, 252, 253, 0.82);
  border-bottom: 1px solid rgba(233, 223, 229, 0.9);
}

.topbar-copy,
.auth-topbar-copy {
  max-width: 1120px;
  margin: 0 auto 16px;
}

.topbar-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #d17890;
}

.topbar h1,
.auth-topbar h1 {
  margin: 0;
  font-size: clamp(1.5rem, 2.5vw, 2rem);
  color: #243042;
}

.subtitle {
  margin: 10px 0 0;
  color: #5f6d81;
  line-height: 1.6;
  max-width: 720px;
}

.user-pill {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid #eadfe5;
  box-shadow: 0 12px 24px rgba(36, 48, 66, 0.08);
}

.user-name {
  font-weight: 700;
  color: #4b596f;
}

.role-pill {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  background: #eef6ff;
  color: #4d7bb5;
  font-size: 0.85rem;
  font-weight: 700;
}

.logout-button,
.auth-nav-button {
  min-height: 42px;
  padding: 0 14px;
  border-radius: 999px;
  cursor: pointer;
  transition:
    background 0.2s ease,
    color 0.2s ease,
    border-color 0.2s ease,
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.logout-button,
.auth-nav-button {
  border: 1px solid #eadfe5;
  background: rgba(255, 255, 255, 0.88);
  color: #526075;
}

.logout-button:hover,
.auth-nav-button:hover {
  transform: translateY(-1px);
  background: #fff7f9;
  border-color: #e6cfd8;
  box-shadow: 0 10px 24px rgba(36, 48, 66, 0.08);
}

.auth-nav {
  max-width: 1120px;
  margin: 0 auto;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.auth-nav-button.active {
  background: linear-gradient(135deg, #f3a6ba, #9fd9cc);
  border-color: transparent;
  color: #1f2937;
  font-weight: 700;
  box-shadow: 0 12px 26px rgba(159, 217, 204, 0.24);
}

.content {
  min-height: calc(100vh - 132px);
}

@media (max-width: 640px) {
  .topbar,
  .auth-topbar {
    padding: 16px 14px 14px;
  }

  .topbar-copy,
  .auth-topbar-copy {
    margin-bottom: 14px;
  }

  .topbar-main {
    flex-direction: column;
  }

  .auth-nav {
    gap: 8px;
  }

  .logout-button,
  .auth-nav-button {
    min-height: 40px;
    padding: 0 12px;
    font-size: 0.94rem;
  }
}
</style>
