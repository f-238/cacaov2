<template>
  <section class="device-shell">
    <div class="device-header">
      <div>
        <p class="eyebrow">Device Overview</p>
        <h1>Connected Dryer Unit</h1>
        <p class="subtitle">
          Temporary frontend device data for status monitoring and UI testing.
        </p>
      </div>

      <div class="status-pill" :class="device.status === 'online' ? 'is-online' : 'is-offline'">
        <span class="status-icon" aria-hidden="true">
          <svg v-if="device.status === 'online'" viewBox="0 0 24 24" focusable="false">
            <path
              d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm-1 14-4-4 1.41-1.41L11 13.17l4.59-4.58L17 10Z"
            />
          </svg>
          <svg v-else viewBox="0 0 24 24" focusable="false">
            <path
              d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm4.59 13.17L15.17 16.6 12 13.41 8.83 16.6l-1.42-1.43L10.59 12 7.41 8.83 8.83 7.4 12 10.59l3.17-3.18 1.42 1.43L13.41 12Z"
            />
          </svg>
        </span>
        {{ device.status === 'online' ? 'Online' : 'Offline' }}
      </div>
    </div>

    <div class="device-grid">
      <article class="device-card hero-card">
        <div class="hero-top">
          <span class="device-badge">Primary unit</span>
          <span class="device-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" focusable="false">
              <path
                d="M6 3h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-4v2h2v2H8v-2h2v-2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Zm0 2v9h12V5Z"
              />
            </svg>
          </span>
        </div>

        <p class="hero-label">Device ID</p>
        <h2>{{ device.id }}</h2>
        <p class="hero-copy">
          This identifier is loaded from local storage and can be swapped with real hardware data later.
        </p>
      </article>

      <article class="device-card info-card">
        <div class="info-row">
          <span class="info-label">Current status</span>
          <span class="info-value" :class="device.status === 'online' ? 'text-online' : 'text-offline'">
            {{ device.status === 'online' ? 'Online' : 'Offline' }}
          </span>
        </div>

        <div class="info-row">
          <span class="info-label">Last seen</span>
          <span class="info-value">{{ formattedLastSeen }}</span>
        </div>

        <div class="info-row">
          <span class="info-label">Local source</span>
          <span class="info-value muted">`localStorage.deviceInfo`</span>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

type Device = {
  id: string
  status: 'online' | 'offline'
  lastSeen: string
}

const defaultDevice: Device = {
  id: 'CACAO-DRV-001',
  status: 'online',
  lastSeen: '2026-04-09T13:45:00.000Z'
}

const device = ref<Device>(defaultDevice)

const formattedLastSeen = computed(() =>
  new Date(device.value.lastSeen).toLocaleString()
)

const loadDeviceInfo = () => {
  const storedDevice = localStorage.getItem('deviceInfo')

  if (!storedDevice) {
    localStorage.setItem('deviceInfo', JSON.stringify(defaultDevice))
    return
  }

  try {
    const parsed = JSON.parse(storedDevice) as Partial<Device>

    device.value = {
      id: typeof parsed.id === 'string' ? parsed.id : defaultDevice.id,
      status: parsed.status === 'offline' ? 'offline' : 'online',
      lastSeen: typeof parsed.lastSeen === 'string' ? parsed.lastSeen : defaultDevice.lastSeen
    }
  } catch {
    localStorage.setItem('deviceInfo', JSON.stringify(defaultDevice))
    device.value = defaultDevice
  }
}

onMounted(() => {
  loadDeviceInfo()
})
</script>

<style scoped>
:global(body) {
  font-family: 'Inter', 'Poppins', 'Roboto', sans-serif;
}

.device-shell {
  min-height: calc(100vh - 72px);
  padding: 32px 20px 48px;
  background:
    radial-gradient(circle at top left, rgba(255, 230, 236, 0.92), transparent 24%),
    radial-gradient(circle at bottom right, rgba(224, 246, 240, 0.92), transparent 28%),
    #fcfcfd;
}

.device-header {
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
  font-size: clamp(1.6rem, 3vw, 2.3rem);
}

.subtitle {
  margin: 12px 0 0;
  color: #5f6d81;
  line-height: 1.6;
  max-width: 620px;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 999px;
  border: 1px solid;
  box-shadow: 0 16px 30px rgba(36, 48, 66, 0.08);
  font-weight: 700;
}

.status-icon {
  width: 20px;
  height: 20px;
}

.status-icon svg {
  width: 100%;
  height: 100%;
  fill: currentColor;
  display: block;
}

.is-online {
  background: #eefaf5;
  border-color: #d6efe5;
  color: #2f8b6b;
}

.is-offline {
  background: #fff1f3;
  border-color: #f1d9de;
  color: #c05672;
}

.device-grid {
  max-width: 1120px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 22px;
}

.device-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #efe3e7;
  border-radius: 24px;
  box-shadow: 0 22px 50px rgba(36, 48, 66, 0.08);
}

.hero-card {
  padding: 26px;
}

.hero-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 26px;
}

.device-badge {
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 999px;
  background: #fff7f9;
  color: #b95d79;
  font-size: 0.92rem;
  font-weight: 700;
}

.device-icon {
  width: 58px;
  height: 58px;
  display: grid;
  place-items: center;
  border-radius: 18px;
  background: linear-gradient(135deg, #ffe5ed, #def6f0);
  color: #4f7088;
}

.device-icon svg {
  width: 28px;
  height: 28px;
  fill: currentColor;
}

.hero-label {
  margin: 0 0 10px;
  color: #7a8799;
  font-size: 0.92rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.hero-copy {
  margin: 14px 0 0;
  color: #627085;
  line-height: 1.6;
  max-width: 40ch;
}

.info-card {
  padding: 26px;
  display: grid;
  gap: 18px;
  align-content: start;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 16px 18px;
  border-radius: 18px;
  background: #fffdfd;
  border: 1px solid #f3eaee;
}

.info-label {
  color: #6e7b8f;
  font-weight: 600;
}

.info-value {
  text-align: right;
  color: #243042;
  font-weight: 700;
}

.text-online {
  color: #2f8b6b;
}

.text-offline {
  color: #c05672;
}

.muted {
  color: #7d8a9d;
  font-weight: 600;
}

@media (max-width: 900px) {
  .device-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .device-shell {
    padding: 22px 14px 36px;
  }

  .device-header {
    flex-direction: column;
  }

  .device-card {
    border-radius: 20px;
  }

  .info-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .info-value {
    text-align: left;
  }
}
</style>
