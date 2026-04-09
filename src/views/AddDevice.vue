<template>
  <section class="add-device-shell">
    <div class="add-device-card">
      <div class="intro">
        <p class="eyebrow">Register Device</p>
        <h1>Add a New Dryer Unit</h1>
        <p class="subtitle">
          Save a device locally for UI testing before real backend integration.
        </p>
      </div>

      <form class="device-form" @submit.prevent="addDevice">
        <label class="field">
          <span class="field-label">Device ID</span>
          <div class="input-group">
            <span class="input-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false">
                <path
                  d="M9 3h6v2h2a2 2 0 0 1 2 2v2h2v2h-2v2h2v2h-2v2a2 2 0 0 1-2 2h-2v2H9v-2H7a2 2 0 0 1-2-2v-2H3v-2h2v-2H3V9h2V7a2 2 0 0 1 2-2h2Zm-2 4v10h10V7Zm3 2h4v6h-4Z"
                />
              </svg>
            </span>
            <input
              v-model.trim="deviceId"
              type="text"
              name="deviceId"
              placeholder="CACAO-DRV-002"
              autocomplete="off"
              required
            >
          </div>
        </label>

        <p v-if="message" class="message" :class="messageType">
          {{ message }}
        </p>

        <button class="submit-button" type="submit">
          <span class="button-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" focusable="false">
              <path d="M11 5h2v6h6v2h-6v6h-2v-6H5v-2h6Z" />
            </svg>
          </span>
          Add Device
        </button>
      </form>

      <div class="device-list">
        <div class="list-head">
          <h2>Saved test devices</h2>
          <span class="count-pill">{{ devices.length }}</span>
        </div>

        <ul v-if="devices.length > 0">
          <li v-for="device in devices" :key="device.id">
            <span class="list-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false">
                <path
                  d="M6 3h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-4v2h2v2H8v-2h2v-2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Zm0 2v9h12V5Z"
                />
              </svg>
            </span>
            <div class="device-meta">
              <strong>{{ device.id }}</strong>
              <span>Saved {{ formatSavedAt(device.createdAt) }}</span>
            </div>
          </li>
        </ul>

        <p v-else class="empty-state">No devices added yet.</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

type StoredDevice = {
  id: string
  createdAt: string
}

const seedDevices: StoredDevice[] = [
  {
    id: 'CACAO-DRV-001',
    createdAt: '2026-04-09T09:00:00.000Z'
  }
]

const deviceId = ref('')
const message = ref('')
const messageType = ref<'success' | 'error'>('success')
const devices = ref<StoredDevice[]>([])

const loadDevices = () => {
  const storedDevices = localStorage.getItem('devices')

  if (!storedDevices) {
    localStorage.setItem('devices', JSON.stringify(seedDevices))
    devices.value = seedDevices
    return
  }

  try {
    const parsed = JSON.parse(storedDevices) as StoredDevice[]
    devices.value = Array.isArray(parsed) ? parsed : seedDevices

    if (!Array.isArray(parsed)) {
      localStorage.setItem('devices', JSON.stringify(seedDevices))
    }
  } catch {
    localStorage.setItem('devices', JSON.stringify(seedDevices))
    devices.value = seedDevices
  }
}

const addDevice = () => {
  message.value = ''

  if (!deviceId.value) {
    message.value = 'Please enter a device ID.'
    messageType.value = 'error'
    return
  }

  const normalizedId = deviceId.value.toUpperCase()
  const exists = devices.value.some((device) => device.id.toUpperCase() === normalizedId)

  if (exists) {
    message.value = 'That device ID already exists in local storage.'
    messageType.value = 'error'
    return
  }

  const newDevice: StoredDevice = {
    id: normalizedId,
    createdAt: new Date().toISOString()
  }

  devices.value = [newDevice, ...devices.value]
  localStorage.setItem('devices', JSON.stringify(devices.value))
  localStorage.setItem(
    'deviceInfo',
    JSON.stringify({
      id: normalizedId,
      status: 'online',
      lastSeen: new Date().toISOString()
    })
  )

  message.value = 'Device added successfully and synced to local device info.'
  messageType.value = 'success'
  deviceId.value = ''
}

const formatSavedAt = (value: string) =>
  new Date(value).toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  })

onMounted(() => {
  loadDevices()
})
</script>

<style scoped>
:global(body) {
  font-family: 'Inter', 'Poppins', 'Roboto', sans-serif;
}

.add-device-shell {
  min-height: calc(100vh - 72px);
  padding: 32px 16px 48px;
  background:
    radial-gradient(circle at top left, rgba(255, 228, 235, 0.92), transparent 24%),
    radial-gradient(circle at bottom right, rgba(221, 244, 238, 0.92), transparent 28%),
    #fcfcfd;
}

.add-device-card {
  width: min(100%, 760px);
  margin: 0 auto;
  padding: 28px;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid #efe3e7;
  border-radius: 26px;
  box-shadow: 0 24px 60px rgba(36, 48, 66, 0.1);
}

.intro {
  margin-bottom: 24px;
}

.eyebrow {
  margin: 0 0 10px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #d17890;
}

h1,
h2 {
  margin: 0;
  color: #243042;
}

h1 {
  font-size: clamp(1.9rem, 4vw, 2.7rem);
}

h2 {
  font-size: 1.1rem;
}

.subtitle {
  margin: 12px 0 0;
  color: #5f6d81;
  line-height: 1.6;
  max-width: 560px;
}

.device-form {
  display: grid;
  gap: 16px;
}

.field {
  display: grid;
  gap: 8px;
}

.field-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #435066;
}

.input-group {
  position: relative;
}

.input-icon {
  position: absolute;
  top: 50%;
  left: 16px;
  width: 20px;
  height: 20px;
  color: #7b88a0;
  transform: translateY(-50%);
}

.input-icon svg,
.button-icon svg,
.list-icon svg {
  width: 100%;
  height: 100%;
  display: block;
  fill: currentColor;
}

input {
  width: 100%;
  min-height: 54px;
  border: 1px solid #e6dce2;
  border-radius: 16px;
  padding: 0 16px 0 48px;
  background: #fff;
  font-size: 1rem;
  color: #243042;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

input::placeholder {
  color: #9aa6b6;
}

input:focus {
  border-color: #d9a6b8;
  box-shadow: 0 0 0 4px rgba(233, 189, 204, 0.35);
}

.message {
  margin: 0;
  border-radius: 14px;
  padding: 12px 14px;
  font-size: 0.95rem;
}

.success {
  background: #edf9f5;
  color: #2b7a62;
}

.error {
  background: #fff1f3;
  color: #b33f5a;
}

.submit-button {
  min-height: 54px;
  border: 0;
  border-radius: 16px;
  background: linear-gradient(135deg, #f3a6ba, #9fd9cc);
  color: #1f2937;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.submit-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 30px rgba(159, 217, 204, 0.28);
}

.button-icon {
  width: 18px;
  height: 18px;
}

.device-list {
  margin-top: 26px;
  padding-top: 22px;
  border-top: 1px solid #f0e5e9;
}

.list-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.count-pill {
  min-width: 34px;
  height: 34px;
  padding: 0 10px;
  border-radius: 999px;
  display: inline-grid;
  place-items: center;
  background: #eef8f4;
  color: #2f8669;
  font-weight: 700;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 12px;
}

li {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  background: #fffdfd;
  border: 1px solid #f3eaee;
  border-radius: 18px;
}

.list-icon {
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: #fff2ed;
  color: #ca6e4f;
  flex-shrink: 0;
}

.device-meta {
  display: grid;
  gap: 4px;
}

.device-meta strong {
  color: #243042;
}

.device-meta span,
.empty-state {
  color: #738196;
  font-size: 0.95rem;
}

.empty-state {
  margin: 0;
}

@media (max-width: 640px) {
  .add-device-shell {
    padding: 20px 14px 36px;
  }

  .add-device-card {
    padding: 22px;
    border-radius: 22px;
  }

  .list-head {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
