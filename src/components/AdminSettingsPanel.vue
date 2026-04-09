<template>
  <section class="settings-shell">
    <div class="summary-grid">
      <article class="summary-card">
        <span class="summary-label">Workspace</span>
        <strong>Admin Settings</strong>
      </article>
      <article class="summary-card">
        <span class="summary-label">Persistence</span>
        <strong>Local Storage</strong>
      </article>
    </div>

    <form class="settings-form" @submit.prevent="saveSettings">
      <section class="panel">
        <div class="panel-head">
          <div class="section-title">
            <span class="title-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false">
                <path d="M19.14 12.94a7.43 7.43 0 0 0 .05-.94 7.43 7.43 0 0 0-.05-.94l2.11-1.65a.5.5 0 0 0 .12-.64l-2-3.46a.48.48 0 0 0-.6-.22l-2.49 1a7.28 7.28 0 0 0-1.63-.94l-.38-2.65A.49.49 0 0 0 13.79 1h-3.58a.49.49 0 0 0-.49.41l-.38 2.65a7.28 7.28 0 0 0-1.63.94l-2.49-1a.48.48 0 0 0-.6.22l-2 3.46a.5.5 0 0 0 .12.64l2.11 1.65a7.43 7.43 0 0 0-.05.94 7.43 7.43 0 0 0 .05.94L2.74 14.6a.5.5 0 0 0-.12.64l2 3.46a.48.48 0 0 0 .6.22l2.49-1a7.28 7.28 0 0 0 1.63.94l.38 2.65a.49.49 0 0 0 .49.41h3.58a.49.49 0 0 0 .49-.41l.38-2.65a7.28 7.28 0 0 0 1.63-.94l2.49 1a.48.48 0 0 0 .6-.22l2-3.46a.5.5 0 0 0-.12-.64ZM12 15.5A3.5 3.5 0 1 1 15.5 12 3.5 3.5 0 0 1 12 15.5Z" />
              </svg>
            </span>
            <div>
              <p class="eyebrow">System Settings</p>
              <h3>Platform Behavior</h3>
            </div>
          </div>
          <p>Control the app identity, environment mode, and notification defaults.</p>
        </div>

        <div class="form-grid">
          <label class="field">
            <span>System Name</span>
            <input v-model="form.systemName" type="text" placeholder="Cacao Monitor Admin" />
          </label>

          <label class="field">
            <span>Support Email</span>
            <input v-model="form.supportEmail" type="email" placeholder="support@example.com" />
          </label>

          <label class="field">
            <span>Environment</span>
            <select v-model="form.environment">
              <option value="Development">Development</option>
              <option value="Staging">Staging</option>
              <option value="Production">Production</option>
            </select>
          </label>

          <label class="field">
            <span>Alert Level</span>
            <select v-model="form.defaultAlertLevel">
              <option value="Info">Info</option>
              <option value="Warning">Warning</option>
              <option value="Critical">Critical</option>
            </select>
          </label>
        </div>

        <div class="toggle-grid">
          <label class="toggle-card">
            <div>
              <strong>Email Notifications</strong>
              <p>Send system notices to the admin support address.</p>
            </div>
            <input v-model="form.emailNotifications" type="checkbox" class="toggle-input" />
          </label>

          <label class="toggle-card">
            <div>
              <strong>Maintenance Mode</strong>
              <p>Temporarily reduce access while updates are in progress.</p>
            </div>
            <input v-model="form.maintenanceMode" type="checkbox" class="toggle-input" />
          </label>
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <div class="section-title">
            <span class="title-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false">
                <path d="M6 3h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-4v2h2v2H8v-2h2v-2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Zm0 2v9h12V5Z" />
              </svg>
            </span>
            <div>
              <p class="eyebrow">Device Config Defaults</p>
              <h3>New Device Presets</h3>
            </div>
          </div>
          <p>Set the standard values applied when a device is registered or claimed.</p>
        </div>

        <div class="form-grid">
          <label class="field">
            <span>Default Device Name Prefix</span>
            <input v-model="form.deviceNamePrefix" type="text" placeholder="Dryer Unit" />
          </label>

          <label class="field">
            <span>Default Owner</span>
            <input v-model="form.defaultOwner" type="text" placeholder="Unassigned" />
          </label>

          <label class="field">
            <span>Default Polling Interval</span>
            <select v-model="form.pollingInterval">
              <option value="15 seconds">15 seconds</option>
              <option value="30 seconds">30 seconds</option>
              <option value="1 minute">1 minute</option>
              <option value="5 minutes">5 minutes</option>
            </select>
          </label>

          <label class="field">
            <span>Default Device Status</span>
            <select v-model="form.defaultDeviceStatus">
              <option value="online">Online</option>
              <option value="offline">Offline</option>
            </select>
          </label>
        </div>

        <div class="toggle-grid">
          <label class="toggle-card">
            <div>
              <strong>Auto Claim New Devices</strong>
              <p>Automatically assign new devices to the default owner.</p>
            </div>
            <input v-model="form.autoClaimDevices" type="checkbox" class="toggle-input" />
          </label>

          <label class="toggle-card">
            <div>
              <strong>Enable Sensor Sync</strong>
              <p>Allow new devices to begin pulling readings immediately.</p>
            </div>
            <input v-model="form.enableSensorSync" type="checkbox" class="toggle-input" />
          </label>
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <div class="section-title">
            <span class="title-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false">
                <path d="M16 11a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm-8 0a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm0 2c-3.33 0-6 1.79-6 4v1h12v-1c0-2.21-2.67-4-6-4Zm8 0c-.29 0-.62 0-1 .05A5.59 5.59 0 0 1 18 17v1h4v-1c0-2.21-2.67-4-6-4Z" />
              </svg>
            </span>
            <div>
              <p class="eyebrow">User Roles</p>
              <h3>Access Defaults</h3>
            </div>
          </div>
          <p>Choose how new accounts are categorized and how privileged access is assigned.</p>
        </div>

        <div class="form-grid">
          <label class="field">
            <span>Default Role</span>
            <select v-model="form.defaultRole">
              <option value="Viewer">Viewer</option>
              <option value="Operator">Operator</option>
              <option value="Admin">Admin</option>
            </select>
          </label>

          <label class="field">
            <span>Privileged Approval Flow</span>
            <select v-model="form.approvalFlow">
              <option value="Single admin">Single admin</option>
              <option value="Two-step review">Two-step review</option>
              <option value="Manual approval only">Manual approval only</option>
            </select>
          </label>

          <label class="field">
            <span>Session Timeout</span>
            <select v-model="form.sessionTimeout">
              <option value="15 minutes">15 minutes</option>
              <option value="30 minutes">30 minutes</option>
              <option value="1 hour">1 hour</option>
              <option value="4 hours">4 hours</option>
            </select>
          </label>

          <label class="field">
            <span>Role Notes</span>
            <input v-model="form.roleNotes" type="text" placeholder="Optional guidance for administrators" />
          </label>
        </div>

        <div class="toggle-grid">
          <label class="toggle-card">
            <div>
              <strong>Allow Self Registration</strong>
              <p>Permit new accounts to sign up without manual invitation.</p>
            </div>
            <input v-model="form.allowSelfRegistration" type="checkbox" class="toggle-input" />
          </label>

          <label class="toggle-card">
            <div>
              <strong>Require Role Approval</strong>
              <p>Force elevated roles to wait for admin review before activation.</p>
            </div>
            <input v-model="form.requireRoleApproval" type="checkbox" class="toggle-input" />
          </label>
        </div>
      </section>

      <div class="footer-row">
        <p v-if="savedMessage" class="saved-message">{{ savedMessage }}</p>
        <button class="save-button" type="submit">
          <span class="button-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" focusable="false">
              <path d="M17 3H5a2 2 0 0 0-2 2v14l4-4h10a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2Zm-1 8H8V9h8Zm0-3H8V6h8Z" />
            </svg>
          </span>
          <span>Save Settings</span>
        </button>
      </div>
    </form>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

type AdminSettings = {
  systemName: string
  supportEmail: string
  environment: 'Development' | 'Staging' | 'Production'
  defaultAlertLevel: 'Info' | 'Warning' | 'Critical'
  emailNotifications: boolean
  maintenanceMode: boolean
  deviceNamePrefix: string
  defaultOwner: string
  pollingInterval: '15 seconds' | '30 seconds' | '1 minute' | '5 minutes'
  defaultDeviceStatus: 'online' | 'offline'
  autoClaimDevices: boolean
  enableSensorSync: boolean
  defaultRole: 'Viewer' | 'Operator' | 'Admin'
  approvalFlow: 'Single admin' | 'Two-step review' | 'Manual approval only'
  sessionTimeout: '15 minutes' | '30 minutes' | '1 hour' | '4 hours'
  roleNotes: string
  allowSelfRegistration: boolean
  requireRoleApproval: boolean
}

const defaultSettings: AdminSettings = {
  systemName: 'Cacao Monitor Admin',
  supportEmail: 'admin@cacaomonitor.local',
  environment: 'Development',
  defaultAlertLevel: 'Warning',
  emailNotifications: true,
  maintenanceMode: false,
  deviceNamePrefix: 'Dryer Unit',
  defaultOwner: 'Unassigned',
  pollingInterval: '30 seconds',
  defaultDeviceStatus: 'online',
  autoClaimDevices: false,
  enableSensorSync: true,
  defaultRole: 'Operator',
  approvalFlow: 'Two-step review',
  sessionTimeout: '1 hour',
  roleNotes: '',
  allowSelfRegistration: true,
  requireRoleApproval: true
}

const form = ref<AdminSettings>({ ...defaultSettings })
const savedMessage = ref('')

const normalizeSettings = (value: Partial<AdminSettings>): AdminSettings => ({
  ...defaultSettings,
  ...value
})

const loadSettings = () => {
  const stored = localStorage.getItem('adminSettings')

  if (!stored) {
    localStorage.setItem('adminSettings', JSON.stringify(defaultSettings))
    form.value = { ...defaultSettings }
    return
  }

  try {
    const parsed = JSON.parse(stored) as Partial<AdminSettings>
    form.value = normalizeSettings(parsed)
  } catch {
    form.value = { ...defaultSettings }
    localStorage.setItem('adminSettings', JSON.stringify(defaultSettings))
  }
}

const saveSettings = () => {
  localStorage.setItem('adminSettings', JSON.stringify(form.value))
  savedMessage.value = 'Settings saved locally.'

  window.setTimeout(() => {
    savedMessage.value = ''
  }, 2400)
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.settings-shell,
.settings-form {
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
  display: block;
  margin-bottom: 10px;
  font-size: 0.82rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #d17890;
}

.summary-card strong,
.panel-head h3 {
  color: #243042;
}

.panel-head {
  margin-bottom: 18px;
}

.section-title {
  display: flex;
  gap: 14px;
  align-items: center;
  margin-bottom: 10px;
}

.title-icon {
  width: 46px;
  height: 46px;
  display: grid;
  place-items: center;
  border-radius: 16px;
  background: #fff2f5;
  color: #d17890;
  flex-shrink: 0;
}

.title-icon svg,
.button-icon svg {
  width: 22px;
  height: 22px;
  fill: currentColor;
  display: block;
}

.eyebrow {
  margin: 0 0 6px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #d17890;
}

.panel-head h3 {
  margin: 0;
}

.panel-head p,
.toggle-card p {
  margin: 0;
  color: #5f6d81;
  line-height: 1.6;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.field {
  display: grid;
  gap: 8px;
  color: #526075;
  font-weight: 600;
}

.field input,
.field select {
  min-height: 48px;
  padding: 0 14px;
  border-radius: 16px;
  border: 1px solid #e6dfe4;
  background: #fffdfd;
  color: #243042;
  font: inherit;
}

.toggle-grid {
  margin-top: 18px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.toggle-card {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 18px;
  border-radius: 20px;
  background: #fffdfd;
  border: 1px solid #f0e6ea;
}

.toggle-card strong {
  display: block;
  margin-bottom: 8px;
  color: #243042;
}

.toggle-input {
  width: 18px;
  height: 18px;
  margin-top: 4px;
  accent-color: #d17890;
  flex-shrink: 0;
}

.footer-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.saved-message {
  margin: 0;
  color: #4c7a65;
  font-weight: 700;
}

.save-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  min-height: 48px;
  padding: 0 20px;
  border: none;
  border-radius: 16px;
  background: linear-gradient(135deg, #f3a6ba, #9fd9cc);
  color: #1f2937;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 18px 32px rgba(36, 48, 66, 0.14);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.save-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 20px 36px rgba(36, 48, 66, 0.16);
}

.button-icon {
  width: 18px;
  height: 18px;
  display: inline-flex;
}

@media (max-width: 900px) {
  .summary-grid,
  .form-grid,
  .toggle-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
  .summary-card,
  .panel {
    border-radius: 22px;
  }

  .toggle-card,
  .footer-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .save-button {
    width: 100%;
    justify-content: center;
  }
}
</style>
