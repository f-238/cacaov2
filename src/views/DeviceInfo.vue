<template>
  <section class="device-shell">
    <div class="device-header">
      <div>
        <p class="eyebrow">Device Registration</p>
        <h1>Manage Connected Dryer Units</h1>
        <p class="subtitle">
          Register devices to your account and issue ingest tokens for secure IoT uploads.
        </p>
      </div>
    </div>

    <article v-if="latestToken" class="token-card">
      <p class="token-title">Latest Device Ingest Token</p>
      <p class="token-serial">Device: {{ latestToken.deviceSerial }}</p>
      <code class="token-value">{{ latestToken.ingestToken }}</code>
      <p class="token-note">
        Save this token in your IoT device. For uploads, send it in header:
        <code>X-Device-Token</code>
      </p>
    </article>

    <article class="form-card">
      <h2>Add New Device</h2>
      <form class="device-form" @submit.prevent="createDevice">
        <label class="field">
          <span>Device Name</span>
          <input
            v-model.trim="form.deviceName"
            type="text"
            placeholder="Cacao Dryer Main Unit"
            required
          >
        </label>

        <label class="field">
          <span>Device Serial / ID</span>
          <input
            v-model.trim="form.deviceSerial"
            type="text"
            placeholder="CACAO-DEV-0001"
            required
          >
        </label>

        <label class="field">
          <span>Firmware Version (optional)</span>
          <input
            v-model.trim="form.firmwareVersion"
            type="text"
            placeholder="v1.2.0"
          >
        </label>

        <button class="primary-button" type="submit" :disabled="isSaving">
          {{ isSaving ? 'Saving...' : 'Add Device' }}
        </button>
      </form>

      <p v-if="errorMessage" class="message error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="message success">{{ successMessage }}</p>
    </article>

    <article class="list-card">
      <h2>Your Devices</h2>

      <p v-if="isLoading" class="empty-state">Loading devices...</p>
      <p v-else-if="devices.length === 0" class="empty-state">No devices registered yet.</p>

      <div v-else class="device-grid">
        <div v-for="device in devices" :key="device.id" class="device-row">
          <div class="device-main">
            <h3>{{ device.name }}</h3>
            <p class="serial">{{ device.serial }}</p>
          </div>

          <div class="meta">
            <span :class="['status-pill', device.isOnline ? 'is-online' : 'is-offline']">
              {{ device.isOnline ? 'Online' : 'Offline' }}
            </span>
            <span class="meta-item">
              Last seen: {{ device.lastSeen ? formatDateTime(device.lastSeen) : 'Never' }}
            </span>
            <span class="meta-item">
              Firmware: {{ device.firmwareVersion || 'N/A' }}
            </span>
          </div>

          <button
            class="secondary-button"
            type="button"
            :disabled="rotatingDeviceId === device.id"
            @click="rotateToken(device.id)"
          >
            {{ rotatingDeviceId === device.id ? 'Issuing...' : 'Rotate Ingest Token' }}
          </button>
        </div>
      </div>
    </article>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import {
  createMyDevice,
  fetchMyDevices,
  rotateMyDeviceIngestToken,
  toFrontendDevice,
  type FrontendDevice
} from '../services/devices'

type DeviceForm = {
  deviceName: string
  deviceSerial: string
  firmwareVersion: string
}

type TokenPreview = {
  deviceId: number
  deviceSerial: string
  ingestToken: string
  issuedAt: string
}

const devices = ref<FrontendDevice[]>([])
const isLoading = ref(true)
const isSaving = ref(false)
const rotatingDeviceId = ref<number | null>(null)
const errorMessage = ref('')
const successMessage = ref('')
const latestToken = ref<TokenPreview | null>(null)

const form = ref<DeviceForm>({
  deviceName: '',
  deviceSerial: '',
  firmwareVersion: ''
})

async function loadDevices() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const apiDevices = await fetchMyDevices()
    devices.value = apiDevices.map(toFrontendDevice)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Failed to load devices.'
  } finally {
    isLoading.value = false
  }
}

async function createDevice() {
  if (!window.confirm('Create this new device and issue an ingest token?')) {
    return
  }

  isSaving.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const created = await createMyDevice({
      deviceName: form.value.deviceName,
      deviceSerial: form.value.deviceSerial,
      firmwareVersion: form.value.firmwareVersion || undefined
    })

    latestToken.value = {
      deviceId: created.id,
      deviceSerial: created.device_serial,
      ingestToken: created.ingest_token,
      issuedAt: new Date().toISOString()
    }

    form.value = {
      deviceName: '',
      deviceSerial: '',
      firmwareVersion: ''
    }
    successMessage.value = `Device ${created.device_serial} created and token issued.`
    await loadDevices()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Failed to create device.'
  } finally {
    isSaving.value = false
  }
}

async function rotateToken(deviceId: number) {
  if (!window.confirm('Rotate ingest token for this device? The previous token will stop working.')) {
    return
  }

  rotatingDeviceId.value = deviceId
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const tokenData = await rotateMyDeviceIngestToken(deviceId)
    latestToken.value = {
      deviceId: tokenData.device_id,
      deviceSerial: tokenData.device_serial,
      ingestToken: tokenData.ingest_token,
      issuedAt: tokenData.issued_at
    }
    successMessage.value = `Ingest token rotated for ${tokenData.device_serial}.`
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Failed to rotate ingest token.'
  } finally {
    rotatingDeviceId.value = null
  }
}

function formatDateTime(value: string) {
  return new Date(value).toLocaleString()
}

onMounted(() => {
  loadDevices()
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
h2,
h3 {
  margin: 0;
  color: #243042;
}

h1 {
  font-size: clamp(2rem, 4vw, 3rem);
}

h2 {
  font-size: 1.25rem;
  margin-bottom: 14px;
}

.subtitle {
  margin: 12px 0 0;
  color: #5f6d81;
  line-height: 1.6;
  max-width: 720px;
}

.token-card,
.form-card,
.list-card {
  max-width: 1120px;
  margin: 0 auto 18px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #efe3e7;
  border-radius: 24px;
  box-shadow: 0 22px 50px rgba(36, 48, 66, 0.08);
  padding: 22px;
}

.token-title {
  margin: 0;
  color: #2d3b52;
  font-weight: 700;
}

.token-serial,
.token-note {
  margin: 10px 0 0;
  color: #5f6d81;
}

.token-value {
  display: block;
  margin-top: 12px;
  padding: 12px;
  border-radius: 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #0f172a;
  word-break: break-all;
  font-size: 0.9rem;
}

.device-form {
  display: grid;
  gap: 12px;
}

.field {
  display: grid;
  gap: 6px;
}

.field span {
  font-size: 0.92rem;
  color: #526075;
  font-weight: 600;
}

input {
  min-height: 44px;
  padding: 0 12px;
  border: 1px solid #e6dce2;
  border-radius: 14px;
  background: #fff;
  color: #243042;
}

input:focus {
  outline: none;
  border-color: #d9a6b8;
  box-shadow: 0 0 0 4px rgba(233, 189, 204, 0.25);
}

.primary-button,
.secondary-button {
  min-height: 42px;
  padding: 0 14px;
  border-radius: 14px;
  cursor: pointer;
  font-weight: 700;
}

.primary-button {
  border: 0;
  background: linear-gradient(135deg, #f3a6ba, #9fd9cc);
  color: #1f2937;
}

.secondary-button {
  border: 1px solid #eadfe5;
  background: rgba(255, 255, 255, 0.88);
  color: #526075;
}

.primary-button:disabled,
.secondary-button:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.message {
  margin: 14px 0 0;
  border-radius: 12px;
  padding: 10px 12px;
  font-size: 0.94rem;
}

.error {
  background: #fff1f3;
  color: #b33f5a;
}

.success {
  background: #edf9f5;
  color: #2b7a62;
}

.empty-state {
  margin: 0;
  color: #64748b;
}

.device-grid {
  display: grid;
  gap: 12px;
}

.device-row {
  border: 1px solid #f1e7eb;
  background: #fffdfd;
  border-radius: 18px;
  padding: 16px;
  display: grid;
  gap: 10px;
}

.device-main {
  display: flex;
  align-items: baseline;
  gap: 10px;
  flex-wrap: wrap;
}

.serial {
  margin: 0;
  color: #526075;
  font-weight: 600;
}

.meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.meta-item {
  color: #526075;
  font-size: 0.92rem;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 700;
}

.is-online {
  background: #eefaf5;
  color: #2f8b6b;
}

.is-offline {
  background: #fff1f3;
  color: #c05672;
}

@media (max-width: 640px) {
  .device-shell {
    padding: 22px 14px 36px;
  }

  .token-card,
  .form-card,
  .list-card {
    border-radius: 20px;
    padding: 16px;
  }
}
</style>
