import { apiRequest } from './api'

export type ApiUserRole = 'user' | 'admin'

export type ApiManagedUser = {
  id: number
  full_name: string
  email: string
  role: ApiUserRole
  is_active: boolean
  avatar_url: string | null
  created_at: string
}

export type FrontendManagedUserRole = 'Admin' | 'Viewer'

export type FrontendManagedUser = {
  id: number
  fullName: string
  email: string
  role: FrontendManagedUserRole
  isActive: boolean
  createdAt: string
}

export type UpdateManagedUserPayload = {
  fullName?: string
  email?: string
  role?: FrontendManagedUserRole
  isActive?: boolean
}

function getAccessTokenOrThrow() {
  const token = localStorage.getItem('accessToken')
  if (!token) {
    throw new Error('You must be logged in to manage users.')
  }

  return token
}

function toApiRole(role: FrontendManagedUserRole): ApiUserRole {
  return role === 'Admin' ? 'admin' : 'user'
}

export function toFrontendManagedUser(user: ApiManagedUser): FrontendManagedUser {
  return {
    id: user.id,
    fullName: user.full_name,
    email: user.email,
    role: user.role === 'admin' ? 'Admin' : 'Viewer',
    isActive: user.is_active,
    createdAt: user.created_at
  }
}

export async function fetchAdminUsers() {
  const token = getAccessTokenOrThrow()
  return apiRequest<ApiManagedUser[]>('/user/users', { token })
}

export async function updateAdminUser(userId: number, payload: UpdateManagedUserPayload) {
  const token = getAccessTokenOrThrow()
  const body: Record<string, unknown> = {}

  if (payload.fullName !== undefined) {
    body.full_name = payload.fullName
  }
  if (payload.email !== undefined) {
    body.email = payload.email
  }
  if (payload.role !== undefined) {
    body.role = toApiRole(payload.role)
  }
  if (payload.isActive !== undefined) {
    body.is_active = payload.isActive
  }

  return apiRequest<ApiManagedUser>(`/user/users/${userId}`, {
    method: 'PATCH',
    token,
    body
  })
}

export async function deleteAdminUser(userId: number) {
  const token = getAccessTokenOrThrow()
  return apiRequest<void>(`/user/users/${userId}`, {
    method: 'DELETE',
    token
  })
}
