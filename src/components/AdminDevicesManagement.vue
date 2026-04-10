<template>
  <section class="devices-stack">
    <div class="summary-grid">
      <article class="summary-card">
        <span class="summary-label">Total Devices</span>
        <strong>{{ sortedDevices.length }}</strong>
      </article>
      <article class="summary-card">
        <span class="summary-label">Online Devices</span>
        <strong>{{ onlineDevices }}</strong>
      </article>
    </div>

    <div class="panel">
      <div class="panel-head">
        <div>
          <h3>Devices Management</h3>
          <p>Search, filter, sort, and manage locally stored device records.</p>
        </div>
      </div>

      <div class="toolbar">
        <label class="search-field">
          <span class="search-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" focusable="false">
              <path d="M10 2a8 8 0 1 0 5.29 14l4.35 4.35 1.41-1.41-4.35-4.35A8 8 0 0 0 10 2Zm0 2a6 6 0 1 1-6 6 6 6 0 0 1 6-6Z" />
            </svg>
          </span>
          <input
            v-model.trim="searchQuery"
            type="search"
            placeholder="Search device, serial, or owner"
          >
        </label>

        <label class="filter-field">
          <span>Status</span>
          <select v-model="statusFilter">
            <option value="All">All Statuses</option>
            <option value="online">Online</option>
            <option value="offline">Offline</option>
          </select>
        </label>

        <label class="filter-field">
          <span>Sort By</span>
          <select v-model="sortBy">
            <option value="lastSeen-desc">Last Seen: Newest</option>
            <option value="lastSeen-asc">Last Seen: Oldest</option>
            <option value="deviceName-asc">Device Name: A-Z</option>
            <option value="owner-asc">Owner: A-Z</option>
            <option value="status-asc">Status</option>
          </select>
        </label>
      </div>

      <div v-if="sortedDevices.length > 0" class="desktop-table">
        <table>
          <thead>
            <tr>
              <th>Device Name</th>
              <th>Serial</th>
              <th>Owner</th>
              <th>Status</th>
              <th>Last Seen</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="device in sortedDevices" :key="device.serial">
              <template v-if="editingSerial === device.serial">
                <td><input v-model.trim="draftDevice.deviceName" class="inline-input"></td>
                <td><input v-model.trim="draftDevice.serial" class="inline-input"></td>
                <td><input v-model.trim="draftDevice.owner" class="inline-input"></td>
                <td>
                  <select v-model="draftDevice.status" class="inline-input inline-select">
                    <option value="online">Online</option>
                    <option value="offline">Offline</option>
                  </select>
                </td>
                <td><input v-model="draftDevice.lastSeen" class="inline-input" type="datetime-local"></td>
                <td>
                  <div class="action-row">
                    <button class="action-button save" @click="saveEdit(device.serial)">Save</button>
                    <button class="action-button ghost" @click="cancelEdit">Cancel</button>
                  </div>
                </td>
              </template>

              <template v-else>
                <td>{{ device.deviceName }}</td>
                <td>{{ device.serial }}</td>
                <td>{{ device.owner }}</td>
                <td>
                  <span class="status-badge" :class="device.status">
                    <span class="status-icon" aria-hidden="true">
                      <svg v-if="device.status === 'online'" viewBox="0 0 24 24" focusable="false">
                        <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm-1 14-4-4 1.41-1.41L11 13.17l4.59-4.58L17 10Z" />
                      </svg>
                      <svg v-else viewBox="0 0 24 24" focusable="false">
                        <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm4.59 13.17L15.17 16.6 12 13.41 8.83 16.6l-1.42-1.43L10.59 12 7.41 8.83 8.83 7.4 12 10.59l3.17-3.18 1.42 1.43L13.41 12Z" />
                      </svg>
                    </span>
                    {{ device.status === 'online' ? 'Online' : 'Offline' }}
                  </span>
                </td>
                <td>{{ formatLastSeen(device.lastSeen) }}</td>
                <td>
                  <div class="action-row">
                    <button class="icon-button reboot" @click="rebootDevice(device.serial)" aria-label="Reboot device">
                      <svg viewBox="0 0 24 24" focusable="false">
                        <path d="M12 6V3l4 4-4 4V8a4 4 0 1 0 4 4h2a6 6 0 1 1-6-6Z" />
                      </svg>
                    </button>
                    <button class="icon-button claim" @click="claimDevice(device.serial)" aria-label="Claim device">
                      <svg viewBox="0 0 24 24" focusable="false">
                        <path d="M12 2 4 7v5c0 5 3.4 9.74 8 11 4.6-1.26 8-6 8-11V7Zm-1 15-4-4 1.41-1.41L11 14.17l4.59-4.58L17 11Z" />
                      </svg>
                    </button>
                    <button class="icon-button edit" @click="startEdit(device)" aria-label="Edit device">
                      <svg viewBox="0 0 24 24" focusable="false">
                        <path d="m3 17.25 9.81-9.81 3.75 3.75L6.75 21H3Zm14.71-9.04a1 1 0 0 0 0-1.42l-2.5-2.5a1 1 0 0 0-1.42 0l-1.56 1.56 3.75 3.75Z" />
                      </svg>
                    </button>
                    <button class="icon-button delete" @click="removeDevice(device.serial)" aria-label="Remove device">
                      <svg viewBox="0 0 24 24" focusable="false">
                        <path d="M9 3h6l1 2h5v2H3V5h5Zm1 7h2v8h-2Zm4 0h2v8h-2ZM7 10h2v8H7Zm1 11a2 2 0 0 1-2-2V8h12v11a2 2 0 0 1-2 2Z" />
                      </svg>
                    </button>
                  </div>
                </td>
              </template>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mobile-cards" v-if="sortedDevices.length > 0">
        <article v-for="device in sortedDevices" :key="`mobile-${device.serial}`" class="device-card">
          <template v-if="editingSerial === device.serial">
            <input v-model.trim="draftDevice.deviceName" class="inline-input" placeholder="Device Name">
            <input v-model.trim="draftDevice.serial" class="inline-input" placeholder="Serial">
            <input v-model.trim="draftDevice.owner" class="inline-input" placeholder="Owner">
            <select v-model="draftDevice.status" class="inline-input inline-select">
              <option value="online">Online</option>
              <option value="offline">Offline</option>
            </select>
            <input v-model="draftDevice.lastSeen" class="inline-input" type="datetime-local">
            <div class="action-row">
              <button class="action-button save" @click="saveEdit(device.serial)">Save</button>
              <button class="action-button ghost" @click="cancelEdit">Cancel</button>
            </div>
          </template>

          <template v-else>
            <div class="device-card-top">
              <div>
                <h4>{{ device.deviceName }}</h4>
                <p>{{ device.serial }}</p>
              </div>
              <span class="status-badge" :class="device.status">
                <span class="status-icon" aria-hidden="true">
                  <svg v-if="device.status === 'online'" viewBox="0 0 24 24" focusable="false">
                    <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm-1 14-4-4 1.41-1.41L11 13.17l4.59-4.58L17 10Z" />
                  </svg>
                  <svg v-else viewBox="0 0 24 24" focusable="false">
                    <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm4.59 13.17L15.17 16.6 12 13.41 8.83 16.6l-1.42-1.43L10.59 12 7.41 8.83 8.83 7.4 12 10.59l3.17-3.18 1.42 1.43L13.41 12Z" />
                  </svg>
                </span>
                {{ device.status === 'online' ? 'Online' : 'Offline' }}
              </span>
            </div>

            <div class="card-meta">
              <span><strong>Owner:</strong> {{ device.owner }}</span>
              <span><strong>Last Seen:</strong> {{ formatLastSeen(device.lastSeen) }}</span>
            </div>

            <div class="action-row">
              <button class="action-button reboot" @click="rebootDevice(device.serial)">Reboot</button>
              <button class="action-button claim" @click="claimDevice(device.serial)">Claim</button>
              <button class="action-button edit" @click="startEdit(device)">Edit</button>
              <button class="action-button delete" @click="removeDevice(device.serial)">Remove</button>
            </div>
          </template>
        </article>
      </div>

      <p v-if="sortedDevices.length === 0" class="empty-copy">No devices match the current search and filters.</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'

type DeviceStatus = 'online' | 'offline'

type ManagedDevice = {
  deviceName: string
  serial: string
  owner: string
  status: DeviceStatus
  lastSeen: string
  createdAt?: string
}

const searchQuery = ref('')
const statusFilter = ref<'All' | DeviceStatus>('All')
const sortBy = ref<'lastSeen-desc' | 'lastSeen-asc' | 'deviceName-asc' | 'owner-asc' | 'status-asc'>('lastSeen-desc')
const editingSerial = ref('')
const devices = ref<ManagedDevice[]>(loadDevices())

const draftDevice = reactive<ManagedDevice>({
  deviceName: '',
  serial: '',
  owner: '',
  status: 'online',
  lastSeen: ''
})

function normalizeDevice(device: Partial<ManagedDevice>, index: number): ManagedDevice {
  return {
    deviceName: device.deviceName || `Dryer Unit ${index + 1}`,
    serial: device.serial || device.serial === '' ? (device.serial as string) : device.serial ?? '',
    owner: device.owner || ['Farm A', 'Farm B', 'QA Team'][index % 3],
    status: device.status === 'offline' ? 'offline' : 'online',
    lastSeen: device.lastSeen || new Date().toISOString(),
    createdAt: device.createdAt
  }
}

function loadDevices() {
  const storedDevices = localStorage.getItem('devices')

  if (!storedDevices) {
    return []
  }

  try {
    const parsed = JSON.parse(storedDevices) as Array<string | Partial<ManagedDevice>>

    if (!Array.isArray(parsed)) {
      return []
    }

    return parsed.map((device, index) => {
      if (typeof device === 'string') {
        return normalizeDevice(
          {
            deviceName: `Dryer Unit ${index + 1}`,
            serial: device,
            owner: ['Farm A', 'Farm B', 'QA Team'][index % 3],
            status: index % 2 === 0 ? 'online' : 'offline',
            lastSeen: new Date(Date.now() - index * 60 * 60 * 1000).toISOString()
          },
          index
        )
      }

      return normalizeDevice(
        {
          ...device,
          serial: device.id || device.serial || ''
        },
        index
      )
    })
  } catch {
    return []
  }
}

function persistDevices() {
  localStorage.setItem(
    'devices',
    JSON.stringify(
      devices.value.map((device) => ({
        deviceName: device.deviceName,
        serial: device.serial,
        owner: device.owner,
        status: device.status,
        lastSeen: device.lastSeen,
        createdAt: device.createdAt
      }))
    )
  )
}

const onlineDevices = computed(() => devices.value.filter((device) => device.status === 'online').length)

const filteredDevices = computed(() => {
  const query = searchQuery.value.toLowerCase()

  return devices.value.filter((device) => {
    const matchesQuery =
      !query ||
      device.deviceName.toLowerCase().includes(query) ||
      device.serial.toLowerCase().includes(query) ||
      device.owner.toLowerCase().includes(query)

    const matchesStatus = statusFilter.value === 'All' || device.status === statusFilter.value

    return matchesQuery && matchesStatus
  })
})

const sortedDevices = computed(() => {
  const nextDevices = [...filteredDevices.value]

  switch (sortBy.value) {
    case 'lastSeen-asc':
      return nextDevices.sort((a, b) => new Date(a.lastSeen).getTime() - new Date(b.lastSeen).getTime())
    case 'deviceName-asc':
      return nextDevices.sort((a, b) => a.deviceName.localeCompare(b.deviceName))
    case 'owner-asc':
      return nextDevices.sort((a, b) => a.owner.localeCompare(b.owner))
    case 'status-asc':
      return nextDevices.sort((a, b) => a.status.localeCompare(b.status))
    default:
      return nextDevices.sort((a, b) => new Date(b.lastSeen).getTime() - new Date(a.lastSeen).getTime())
  }
})

function startEdit(device: ManagedDevice) {
  editingSerial.value = device.serial
  Object.assign(draftDevice, {
    ...device,
    lastSeen: toDatetimeLocal(device.lastSeen)
  })
}

function cancelEdit() {
  editingSerial.value = ''
}

function saveEdit(originalSerial: string) {
  const nextSerial = draftDevice.serial?.trim() ?? ''
  const nextDeviceName = draftDevice.deviceName?.trim() ?? ''
  const nextOwner = draftDevice.owner?.trim() ?? ''

  if (!nextSerial || !nextDeviceName || !nextOwner) {
    return
  }

  if (!window.confirm('Save device changes?')) {
    return
  }

  devices.value = devices.value.map((device) =>
    device.serial === originalSerial
      ? {
          ...device,
          deviceName: nextDeviceName,
          serial: nextSerial,
          owner: nextOwner,
          status: draftDevice.status,
          lastSeen: fromDatetimeLocal(draftDevice.lastSeen)
        }
      : device
  )

  persistDevices()
  syncPrimaryDevice()
  cancelEdit()
}

function rebootDevice(serial: string) {
  if (!window.confirm(`Reboot device ${serial}?`)) {
    return
  }

  devices.value = devices.value.map((device) =>
    device.serial === serial
      ? {
          ...device,
          status: 'online',
          lastSeen: new Date().toISOString()
        }
      : device
  )

  persistDevices()
  syncPrimaryDevice()
}

function claimDevice(serial: string) {
  if (!window.confirm(`Claim device ${serial} for Admin Team?`)) {
    return
  }

  devices.value = devices.value.map((device) =>
    device.serial === serial
      ? {
          ...device,
          owner: 'Admin Team'
        }
      : device
  )

  persistDevices()
}

function removeDevice(serial: string) {
  if (!window.confirm(`Remove device ${serial}? This action cannot be undone.`)) {
    return
  }

  devices.value = devices.value.filter((device) => device.serial !== serial)
  persistDevices()
  syncPrimaryDevice()

  if (editingSerial.value === serial) {
    cancelEdit()
  }
}

function syncPrimaryDevice() {
  const primaryDevice = devices.value[0]

  if (!primaryDevice) {
    localStorage.removeItem('deviceInfo')
    return
  }

  localStorage.setItem(
    'deviceInfo',
    JSON.stringify({
      id: primaryDevice.serial,
      status: primaryDevice.status,
      lastSeen: primaryDevice.lastSeen
    })
  )
}

function formatLastSeen(value: string) {
  return new Date(value).toLocaleString()
}

function toDatetimeLocal(value: string) {
  const date = new Date(value)
  const pad = (unit: number) => String(unit).padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`
}

function fromDatetimeLocal(value: string) {
  return value ? new Date(value).toISOString() : new Date().toISOString()
}
</script>

<style scoped>
.devices-stack {
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

.toolbar {
  display: grid;
  grid-template-columns: minmax(240px, 1.2fr) repeat(2, minmax(160px, 0.5fr));
  gap: 12px;
  margin-bottom: 18px;
}

.search-field,
.filter-field {
  display: grid;
  gap: 6px;
}

.search-field span,
.filter-field span {
  color: #526075;
  font-size: 0.92rem;
  font-weight: 600;
}

.search-field {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 14px;
  bottom: 12px;
  width: 18px;
  height: 18px;
  color: #7a8799;
}

.search-icon svg,
.icon-button svg,
.status-icon svg {
  width: 100%;
  height: 100%;
  fill: currentColor;
  display: block;
}

.search-field input,
.filter-field select,
.inline-input {
  min-height: 44px;
  padding: 0 12px;
  border: 1px solid #e6dce2;
  border-radius: 14px;
  background: #fff;
  color: #243042;
}

.search-field input {
  padding-left: 42px;
}

.search-field input:focus,
.filter-field select:focus,
.inline-input:focus {
  outline: none;
  border-color: #d9a6b8;
  box-shadow: 0 0 0 4px rgba(233, 189, 204, 0.25);
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

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 0.88rem;
  font-weight: 700;
}

.status-badge.online {
  background: #effaf5;
  color: #3b9274;
}

.status-badge.offline {
  background: #fff1f3;
  color: #c05c72;
}

.status-icon {
  width: 16px;
  height: 16px;
}

.action-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.icon-button,
.action-button {
  min-height: 38px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}

.icon-button {
  width: 38px;
  padding: 8px;
  border: 0;
}

.icon-button.reboot,
.action-button.reboot {
  background: #eef6ff;
  color: #4d7bb5;
}

.icon-button.claim,
.action-button.claim {
  background: #effaf5;
  color: #3b9274;
}

.icon-button.edit,
.action-button.edit {
  background: #fff7e8;
  color: #b88a2b;
}

.icon-button.delete,
.action-button.delete {
  background: #fff1f3;
  color: #c05c72;
}

.action-button.save {
  padding: 0 12px;
  border: 0;
  background: linear-gradient(135deg, #f3a6ba, #9fd9cc);
  color: #1f2937;
}

.action-button.ghost {
  padding: 0 12px;
  border: 1px solid #eadfe5;
  background: rgba(255, 255, 255, 0.88);
  color: #526075;
}

.mobile-cards {
  display: none;
}

.device-card {
  display: grid;
  gap: 14px;
  padding: 18px;
  border-radius: 18px;
  background: #fffdfd;
  border: 1px solid #f3eaee;
}

.device-card-top {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.device-card-top h4 {
  margin: 0;
  color: #243042;
}

.device-card-top p,
.card-meta {
  margin: 6px 0 0;
  color: #607085;
}

.card-meta {
  display: grid;
  gap: 6px;
}

.inline-select {
  width: 100%;
}

@media (max-width: 900px) {
  .toolbar {
    grid-template-columns: 1fr;
  }
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
}
</style>
