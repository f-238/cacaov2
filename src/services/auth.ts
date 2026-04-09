import { apiRequest } from './api'

export type ApiUserRole = 'user' | 'admin'

export type ApiUser = {
  id: number
  full_name: string
  email: string
  role: ApiUserRole
  is_active: boolean
  created_at: string
}

export type AuthTokens = {
  access_token: string
  refresh_token: string
  token_type: string
}

export type FrontendAuthUser = {
  fullName: string
  email: string
  role: 'Admin' | 'Viewer'
}

export async function registerUser(payload: {
  fullName: string
  email: string
  password: string
  role?: ApiUserRole
}) {
  return apiRequest<ApiUser>('/auth/register', {
    method: 'POST',
    body: {
      full_name: payload.fullName,
      email: payload.email,
      password: payload.password,
      role: payload.role ?? 'user'
    }
  })
}

export async function loginUser(payload: { email: string; password: string }) {
  return apiRequest<AuthTokens>('/auth/login', {
    method: 'POST',
    body: payload
  })
}

export async function fetchCurrentUser(token: string) {
  return apiRequest<ApiUser>('/auth/me', { token })
}

export function toFrontendAuthUser(user: ApiUser): FrontendAuthUser {
  return {
    fullName: user.full_name,
    email: user.email,
    role: user.role === 'admin' ? 'Admin' : 'Viewer'
  }
}
