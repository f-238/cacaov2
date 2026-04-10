import { apiFormRequest } from './api'

export type ApiProfile = {
  id: number
  full_name: string
  email: string
  avatar_url: string | null
  role: 'user' | 'admin'
  is_active: boolean
  created_at: string
  updated_at: string
}

export type UpdateProfilePayload = {
  fullName?: string
  email?: string
  currentPassword?: string
  newPassword?: string
  avatar?: File | null
}

export async function updateProfile(token: string, payload: UpdateProfilePayload) {
  const formData = new FormData()

  if (typeof payload.fullName === 'string' && payload.fullName.trim()) {
    formData.set('full_name', payload.fullName.trim())
  }

  if (typeof payload.email === 'string' && payload.email.trim()) {
    formData.set('email', payload.email.trim())
  }

  if (typeof payload.currentPassword === 'string' && payload.currentPassword) {
    formData.set('current_password', payload.currentPassword)
  }

  if (typeof payload.newPassword === 'string' && payload.newPassword) {
    formData.set('new_password', payload.newPassword)
  }

  if (payload.avatar instanceof File) {
    formData.set('avatar', payload.avatar)
  }

  return apiFormRequest<ApiProfile>('/user/profile', {
    method: 'PATCH',
    token,
    formData
  })
}
