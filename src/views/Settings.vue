<template>
  <section class="settings-shell">
    <article class="settings-card">
      <div class="section-head">
        <p class="eyebrow">Appearance</p>
        <h2>Theme and Interface</h2>
      </div>

      <div class="field-grid">
        <label class="field">
          <span>Theme Mode</span>
          <div class="segmented">
            <button
              v-for="mode in themeModes"
              :key="mode"
              type="button"
              class="segmented-button"
              :class="{ active: settingsForm.themeMode === mode }"
              @click="settingsForm.themeMode = mode"
            >
              {{ mode }}
            </button>
          </div>
        </label>

        <label class="field">
          <span>Font Size</span>
          <select v-model="settingsForm.fontSize">
            <option value="small">Small</option>
            <option value="medium">Medium</option>
            <option value="large">Large</option>
          </select>
        </label>
      </div>

      <div class="field-grid colors">
        <label class="field">
          <span>Primary Color</span>
          <input v-model="settingsForm.primaryColor" type="color">
        </label>
        <label class="field">
          <span>Secondary Color</span>
          <input v-model="settingsForm.secondaryColor" type="color">
        </label>
        <label class="field">
          <span>Accent Color</span>
          <input v-model="settingsForm.accentColor" type="color">
        </label>
      </div>

      <p class="autosave-copy">
        {{ syncingSettings ? 'Saving appearance changes...' : 'Appearance changes are saved automatically.' }}
      </p>
    </article>

    <article class="settings-card">
      <div class="section-head">
        <p class="eyebrow">Profile</p>
        <h2>Edit Account Info</h2>
      </div>

      <div class="profile-layout">
        <div class="avatar-block">
          <img
            v-if="avatarPreviewUrl"
            :src="avatarPreviewUrl"
            alt="Profile avatar"
            class="avatar-preview"
          >
          <div v-else class="avatar-fallback">{{ profileInitials }}</div>
          <label class="file-label">
            <input class="file-input" type="file" accept="image/*" @change="onAvatarSelected">
            <span class="file-button">Upload Avatar</span>
          </label>
          <p class="file-meta">{{ selectedAvatarFile ? selectedAvatarFile.name : 'No file selected' }}</p>
        </div>

        <div class="profile-fields">
          <label class="field">
            <span>Full Name</span>
            <input v-model.trim="profileForm.fullName" type="text" placeholder="Your name">
          </label>

          <label class="field">
            <span>Email</span>
            <input v-model.trim="profileForm.email" type="email" placeholder="you@example.com">
          </label>

          <label class="field">
            <span>Current Password</span>
            <input v-model="profileForm.currentPassword" type="password" placeholder="Required to change password">
          </label>

          <label class="field">
            <span>New Password</span>
            <input v-model="profileForm.newPassword" type="password" placeholder="Leave blank to keep current password">
          </label>

          <div class="actions">
            <button class="primary-button" type="button" :disabled="savingProfile" @click="saveProfile">
              {{ savingProfile ? 'Updating...' : 'Save Profile' }}
            </button>
          </div>
        </div>
      </div>
    </article>

    <article class="settings-card signout-card">
      <div class="section-head">
        <p class="eyebrow">Session</p>
        <h2>Account Session</h2>
      </div>
      <p class="signout-copy">Sign out from your current session on this device.</p>
      <button class="danger-button" type="button" @click="emit('sign-out')">Sign Out</button>
    </article>

    <p v-if="errorMessage" class="message error">{{ errorMessage }}</p>
    <p v-if="successMessage" class="message success">{{ successMessage }}</p>
  </section>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { API_BASE_URL } from '../services/api'
import { fetchCurrentUser } from '../services/auth'
import { updateProfile } from '../services/profile'
import {
  applyUserSettings,
  getStoredUserSettings,
  syncUserSettingsFromBackend,
  toFrontendUserSettings,
  updateUserSettings,
  type FrontendUserSettings,
  type FontSize,
  type ThemeMode
} from '../services/userSettings'

type SettingsForm = {
  themeMode: ThemeMode
  fontSize: FontSize
  primaryColor: string
  secondaryColor: string
  accentColor: string
}

type ProfileForm = {
  fullName: string
  email: string
  currentPassword: string
  newPassword: string
}

const emit = defineEmits<{
  'sign-out': []
  'profile-updated': [payload: { fullName: string; email: string }]
}>()

const themeModes: ThemeMode[] = ['light', 'dark', 'system']
const syncingSettings = ref(false)
const savingProfile = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const selectedAvatarFile = ref<File | null>(null)
const serverAvatarUrl = ref<string | null>(null)
const localAvatarPreviewUrl = ref('')
const settingsRecord = ref<FrontendUserSettings | null>(null)
const suppressAutoSettingsSync = ref(true)
let settingsSyncTimeout: ReturnType<typeof setTimeout> | null = null

const settingsForm = reactive<SettingsForm>({
  themeMode: 'system',
  fontSize: 'medium',
  primaryColor: '#1f2937',
  secondaryColor: '#526075',
  accentColor: '#f3a6ba'
})

const profileForm = reactive<ProfileForm>({
  fullName: '',
  email: '',
  currentPassword: '',
  newPassword: ''
})

const profileInitials = computed(() => {
  const name = profileForm.fullName.trim()
  if (!name) {
    return 'U'
  }

  return name
    .split(/\s+/)
    .slice(0, 2)
    .map((chunk) => chunk[0]?.toUpperCase() ?? '')
    .join('')
})

const avatarPreviewUrl = computed(() => {
  if (localAvatarPreviewUrl.value) {
    return localAvatarPreviewUrl.value
  }

  if (serverAvatarUrl.value) {
    return resolveAvatarUrl(serverAvatarUrl.value)
  }

  return ''
})

const accessToken = localStorage.getItem('accessToken')

function resolveAvatarUrl(path: string) {
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }

  if (API_BASE_URL.startsWith('http://') || API_BASE_URL.startsWith('https://')) {
    const origin = API_BASE_URL.replace(/\/api\/?$/, '')
    return `${origin}${path}`
  }

  const origin = `${window.location.protocol}//${window.location.hostname}:8000`
  return `${origin}${path}`
}

function onAvatarSelected(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  selectedAvatarFile.value = file ?? null
  if (localAvatarPreviewUrl.value) {
    URL.revokeObjectURL(localAvatarPreviewUrl.value)
    localAvatarPreviewUrl.value = ''
  }
  if (file) {
    localAvatarPreviewUrl.value = URL.createObjectURL(file)
  }
}

async function loadSettingsAndProfile() {
  if (!accessToken) {
    return
  }

  errorMessage.value = ''

  try {
    const [settings, currentUser] = await Promise.all([
      syncUserSettingsFromBackend(accessToken),
      fetchCurrentUser(accessToken)
    ])
    settingsRecord.value = settings

    patchSettingsForm(settings)

    profileForm.fullName = currentUser.full_name
    profileForm.email = currentUser.email
    serverAvatarUrl.value = currentUser.avatar_url

    applyUserSettings(settings)
  } catch (error) {
    const stored = getStoredUserSettings()
    if (stored) {
      settingsRecord.value = stored
      patchSettingsForm(stored)
    }

    errorMessage.value = error instanceof Error ? error.message : 'Failed to load settings.'
  }

  suppressAutoSettingsSync.value = false
}

function buildAppearanceSettings(): FrontendUserSettings {
  const baseline =
    settingsRecord.value ??
    getStoredUserSettings() ?? {
      id: 0,
      userId: 0,
      themeMode: 'system',
      fontSize: 'medium',
      primaryColor: '#1f2937',
      secondaryColor: '#526075',
      accentColor: '#f3a6ba',
      createdAt: new Date(0).toISOString(),
      updatedAt: new Date(0).toISOString()
    }

  return {
    ...baseline,
    themeMode: settingsForm.themeMode,
    fontSize: settingsForm.fontSize,
    primaryColor: settingsForm.primaryColor,
    secondaryColor: settingsForm.secondaryColor,
    accentColor: settingsForm.accentColor
  }
}

function patchSettingsForm(settings: FrontendUserSettings) {
  suppressAutoSettingsSync.value = true
  settingsForm.themeMode = settings.themeMode
  settingsForm.fontSize = settings.fontSize
  settingsForm.primaryColor = settings.primaryColor
  settingsForm.secondaryColor = settings.secondaryColor
  settingsForm.accentColor = settings.accentColor
  suppressAutoSettingsSync.value = false
}

function scheduleSettingsSync() {
  if (settingsSyncTimeout) {
    clearTimeout(settingsSyncTimeout)
  }

  settingsSyncTimeout = setTimeout(() => {
    saveSettings()
  }, 450)
}

async function saveSettings() {
  if (!accessToken) {
    errorMessage.value = 'You must be logged in to update settings.'
    return
  }

  const previousSettings = settingsRecord.value
  const optimisticSettings = buildAppearanceSettings()
  syncingSettings.value = true
  successMessage.value = ''

  try {
    const updated = await updateUserSettings(accessToken, {
      themeMode: settingsForm.themeMode,
      fontSize: settingsForm.fontSize,
      primaryColor: settingsForm.primaryColor,
      secondaryColor: settingsForm.secondaryColor,
      accentColor: settingsForm.accentColor
    })

    const updatedSettings = toFrontendUserSettings(updated)
    settingsRecord.value = updatedSettings
    applyUserSettings(updatedSettings)
    successMessage.value = 'Appearance settings saved.'
    errorMessage.value = ''
  } catch (error) {
    const rollbackSettings = previousSettings ?? getStoredUserSettings()
    if (rollbackSettings) {
      settingsRecord.value = rollbackSettings
      patchSettingsForm(rollbackSettings)
      applyUserSettings(rollbackSettings)
    }
    errorMessage.value = error instanceof Error ? error.message : 'Failed to update settings.'
  } finally {
    syncingSettings.value = false
  }
}

async function saveProfile() {
  if (!accessToken) {
    errorMessage.value = 'You must be logged in to update profile.'
    return
  }

  if (!window.confirm('Save profile changes for this account?')) {
    return
  }

  savingProfile.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const updated = await updateProfile(accessToken, {
      fullName: profileForm.fullName,
      email: profileForm.email,
      currentPassword: profileForm.currentPassword || undefined,
      newPassword: profileForm.newPassword || undefined,
      avatar: selectedAvatarFile.value
    })

    profileForm.fullName = updated.full_name
    profileForm.email = updated.email
    profileForm.currentPassword = ''
    profileForm.newPassword = ''
    selectedAvatarFile.value = null
    if (localAvatarPreviewUrl.value) {
      URL.revokeObjectURL(localAvatarPreviewUrl.value)
      localAvatarPreviewUrl.value = ''
    }
    serverAvatarUrl.value = updated.avatar_url
    emit('profile-updated', {
      fullName: updated.full_name,
      email: updated.email
    })
    successMessage.value = 'Profile updated successfully.'
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Failed to update profile.'
  } finally {
    savingProfile.value = false
  }
}

onMounted(() => {
  loadSettingsAndProfile()
})

watch(
  () => [
    settingsForm.themeMode,
    settingsForm.fontSize,
    settingsForm.primaryColor,
    settingsForm.secondaryColor,
    settingsForm.accentColor
  ],
  () => {
    if (suppressAutoSettingsSync.value) {
      return
    }

    applyUserSettings(buildAppearanceSettings())
    scheduleSettingsSync()
  }
)

onBeforeUnmount(() => {
  if (settingsSyncTimeout) {
    clearTimeout(settingsSyncTimeout)
    settingsSyncTimeout = null
  }
  if (localAvatarPreviewUrl.value) {
    URL.revokeObjectURL(localAvatarPreviewUrl.value)
    localAvatarPreviewUrl.value = ''
  }
})
</script>

<style scoped>
.settings-shell {
  display: grid;
  gap: 18px;
}

.settings-card {
  padding: 22px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #efe3e7;
  box-shadow: 0 22px 50px rgba(36, 48, 66, 0.08);
}

.section-head {
  margin-bottom: 14px;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--user-accent-color, #d17890);
}

h2 {
  margin: 0;
  color: var(--app-text-color, #243042);
}

.field-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.field-grid.colors {
  margin-top: 12px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.field {
  display: grid;
  gap: 8px;
}

.field span {
  color: var(--user-secondary-color, #526075);
  font-size: 0.92rem;
  font-weight: 600;
}

input,
select {
  min-height: 44px;
  border: 1px solid #e6dce2;
  border-radius: 14px;
  padding: 0 12px;
  background: #fff;
  color: var(--app-text-color, #243042);
}

input[type='color'] {
  padding: 6px;
}

.segmented {
  display: flex;
  gap: 8px;
}

.segmented-button {
  min-height: 42px;
  padding: 0 12px;
  border-radius: 12px;
  border: 1px solid #e6dce2;
  background: #fff;
  color: var(--user-secondary-color, #526075);
  cursor: pointer;
  text-transform: capitalize;
}

.segmented-button.active {
  background: linear-gradient(135deg, var(--user-accent-color, #f3a6ba), #9fd9cc);
  border-color: transparent;
  color: var(--user-primary-color, #1f2937);
  font-weight: 700;
}

.profile-layout {
  display: grid;
  grid-template-columns: 200px minmax(0, 1fr);
  gap: 18px;
}

.avatar-block {
  display: grid;
  gap: 10px;
  align-content: start;
}

.avatar-preview,
.avatar-fallback {
  width: 180px;
  height: 180px;
  border-radius: 18px;
  border: 1px solid #e6dce2;
  object-fit: cover;
}

.avatar-fallback {
  display: grid;
  place-items: center;
  background: #fff7f9;
  color: var(--user-primary-color, #1f2937);
  font-size: 2.1rem;
  font-weight: 700;
}

.file-label {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 1px;
  height: 1px;
  opacity: 0;
  pointer-events: none;
}

.file-button {
  min-height: 40px;
  padding: 0 14px;
  border-radius: 12px;
  border: 1px solid var(--app-border-color, #d6dde6);
  background: var(--app-surface-muted, #f3f6f9);
  color: var(--app-text-color, #1f2937);
  display: inline-flex;
  align-items: center;
  font-weight: 600;
  cursor: pointer;
}

.file-label:focus-within .file-button {
  outline: none;
  border-color: var(--app-border-strong, #94a3b8);
  box-shadow: var(--app-focus-ring, 0 0 0 4px rgba(15, 23, 42, 0.08));
}

.file-meta {
  margin: 0;
  font-size: 0.85rem;
  color: var(--app-text-secondary, #607085);
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-fields {
  display: grid;
  gap: 12px;
}

.actions {
  margin-top: 10px;
  display: flex;
  justify-content: flex-start;
}

.autosave-copy {
  margin: 14px 0 0;
  color: var(--app-muted-color, #5f6d81);
  font-size: 0.92rem;
}

.primary-button,
.danger-button {
  min-height: 44px;
  padding: 0 16px;
  border-radius: 14px;
  border: 0;
  cursor: pointer;
  font-weight: 700;
}

.primary-button {
  background: linear-gradient(135deg, var(--user-accent-color, #f3a6ba), #9fd9cc);
  color: var(--user-primary-color, #1f2937);
}

.danger-button {
  background: #fff1f3;
  color: #b33f5a;
}

.primary-button:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.signout-card {
  display: grid;
  gap: 10px;
}

.signout-copy {
  margin: 0;
  color: var(--app-muted-color, #5f6d81);
}

.message {
  margin: 0;
  border-radius: 14px;
  padding: 12px 14px;
  font-size: 0.95rem;
}

.error {
  background: #fff1f3;
  color: #b33f5a;
}

.success {
  background: #edf9f5;
  color: #2b7a62;
}

@media (max-width: 900px) {
  .field-grid,
  .field-grid.colors,
  .profile-layout {
    grid-template-columns: 1fr;
  }

  .avatar-preview,
  .avatar-fallback {
    width: 120px;
    height: 120px;
    border-radius: 14px;
  }
}
</style>
