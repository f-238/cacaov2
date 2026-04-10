import { apiRequest } from './api'

export type ThemeMode = 'light' | 'dark' | 'system'
export type FontSize = 'small' | 'medium' | 'large'

export type ApiUserSettings = {
  id: number
  user_id: number
  theme_mode: ThemeMode
  font_size: FontSize
  primary_color: string
  secondary_color: string
  accent_color: string
  created_at: string
  updated_at: string
}

export type UpdateUserSettingsPayload = {
  themeMode: ThemeMode
  fontSize: FontSize
  primaryColor: string
  secondaryColor: string
  accentColor: string
}

export type FrontendUserSettings = {
  id: number
  userId: number
  themeMode: ThemeMode
  fontSize: FontSize
  primaryColor: string
  secondaryColor: string
  accentColor: string
  createdAt: string
  updatedAt: string
}

const USER_SETTINGS_STORAGE_KEY = 'userSettings'

const defaultUserSettings: FrontendUserSettings = {
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

let systemThemeQuery: MediaQueryList | null = null
let systemThemeListener: ((event: MediaQueryListEvent) => void) | null = null

export async function fetchUserSettings(token: string) {
  return apiRequest<ApiUserSettings>('/user/settings', { token })
}

export async function syncUserSettingsFromBackend(token: string) {
  const settings = toFrontendUserSettings(await fetchUserSettings(token))
  applyUserSettings(settings)
  return settings
}

export async function updateUserSettings(token: string, payload: UpdateUserSettingsPayload) {
  return apiRequest<ApiUserSettings>('/user/settings', {
    method: 'PUT',
    token,
    body: {
      theme_mode: payload.themeMode,
      font_size: payload.fontSize,
      primary_color: payload.primaryColor,
      secondary_color: payload.secondaryColor,
      accent_color: payload.accentColor
    }
  })
}

export function toFrontendUserSettings(settings: ApiUserSettings): FrontendUserSettings {
  return {
    id: settings.id,
    userId: settings.user_id,
    themeMode: settings.theme_mode,
    fontSize: settings.font_size,
    primaryColor: settings.primary_color,
    secondaryColor: settings.secondary_color,
    accentColor: settings.accent_color,
    createdAt: settings.created_at,
    updatedAt: settings.updated_at
  }
}

export function applyUserSettings(settings: FrontendUserSettings) {
  localStorage.setItem(USER_SETTINGS_STORAGE_KEY, JSON.stringify(settings))
  const root = document.documentElement
  root.dataset.themeMode = settings.themeMode

  root.style.setProperty('--user-primary-color', settings.primaryColor)
  root.style.setProperty('--user-secondary-color', settings.secondaryColor)
  root.style.setProperty('--user-accent-color', settings.accentColor)
  root.style.setProperty('--app-font-scale', toFontScale(settings.fontSize))

  applyResolvedTheme(settings.themeMode)
}

export function applyStoredUserSettings() {
  const storedSettings = localStorage.getItem(USER_SETTINGS_STORAGE_KEY)
  if (!storedSettings) {
    applyUserSettings(defaultUserSettings)
    return
  }

  try {
    const parsed = JSON.parse(storedSettings) as Partial<FrontendUserSettings>
    applyUserSettings({
      ...defaultUserSettings,
      ...parsed,
      themeMode: normalizeThemeMode(parsed.themeMode),
      fontSize: normalizeFontSize(parsed.fontSize)
    })
  } catch {
    applyUserSettings(defaultUserSettings)
  }
}

export function clearAppliedUserSettings() {
  localStorage.removeItem(USER_SETTINGS_STORAGE_KEY)
  removeSystemThemeListener()
  applyUserSettings(defaultUserSettings)
}

export function getStoredUserSettings(): FrontendUserSettings | null {
  const storedSettings = localStorage.getItem(USER_SETTINGS_STORAGE_KEY)
  if (!storedSettings) {
    return null
  }

  try {
    const parsed = JSON.parse(storedSettings) as Partial<FrontendUserSettings>
    return {
      ...defaultUserSettings,
      ...parsed,
      themeMode: normalizeThemeMode(parsed.themeMode),
      fontSize: normalizeFontSize(parsed.fontSize)
    }
  } catch {
    return null
  }
}

function applyResolvedTheme(themeMode: ThemeMode) {
  removeSystemThemeListener()
  const resolvedTheme = resolveTheme(themeMode)
  setThemeOnDocument(resolvedTheme)

  if (themeMode === 'system' && typeof window !== 'undefined' && typeof window.matchMedia === 'function') {
    systemThemeQuery = window.matchMedia('(prefers-color-scheme: dark)')
    systemThemeListener = (event: MediaQueryListEvent) => {
      setThemeOnDocument(event.matches ? 'dark' : 'light')
    }

    if (typeof systemThemeQuery.addEventListener === 'function') {
      systemThemeQuery.addEventListener('change', systemThemeListener)
    } else if (typeof systemThemeQuery.addListener === 'function') {
      systemThemeQuery.addListener(systemThemeListener)
    }
  }
}

function setThemeOnDocument(resolvedTheme: 'light' | 'dark') {
  const root = document.documentElement
  const body = document.body ?? root
  root.dataset.theme = resolvedTheme
  body.classList.toggle('theme-dark', resolvedTheme === 'dark')
  body.classList.toggle('theme-light', resolvedTheme === 'light')
  root.style.colorScheme = resolvedTheme
}

function resolveTheme(themeMode: ThemeMode): 'light' | 'dark' {
  if (themeMode === 'light' || themeMode === 'dark') {
    return themeMode
  }

  if (typeof window === 'undefined') {
    return 'light'
  }

  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function removeSystemThemeListener() {
  if (systemThemeQuery && systemThemeListener) {
    if (typeof systemThemeQuery.removeEventListener === 'function') {
      systemThemeQuery.removeEventListener('change', systemThemeListener)
    } else if (typeof systemThemeQuery.removeListener === 'function') {
      systemThemeQuery.removeListener(systemThemeListener)
    }
  }
  systemThemeQuery = null
  systemThemeListener = null
}

function toFontScale(fontSize: FontSize) {
  if (fontSize === 'small') {
    return '0.9375'
  }

  if (fontSize === 'large') {
    return '1.0625'
  }

  return '1'
}

function normalizeThemeMode(value: unknown): ThemeMode {
  if (value === 'light' || value === 'dark' || value === 'system') {
    return value
  }
  return 'system'
}

function normalizeFontSize(value: unknown): FontSize {
  if (value === 'small' || value === 'medium' || value === 'large') {
    return value
  }
  return 'medium'
}
