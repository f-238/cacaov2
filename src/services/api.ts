const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  (import.meta.env.DEV ? 'http://127.0.0.1:8000/api' : '/api')

type RequestOptions = {
  method?: string
  token?: string | null
  body?: unknown
}

type FormRequestOptions = {
  method?: string
  token?: string | null
  formData: FormData
}

export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...(options.token ? { Authorization: `Bearer ${options.token}` } : {})
    },
    body: options.body ? JSON.stringify(options.body) : undefined
  })

  if (!response.ok) {
    let message = 'Request failed.'

    try {
      const errorPayload = (await response.json()) as { detail?: string }
      if (typeof errorPayload.detail === 'string') {
        message = errorPayload.detail
      }
    } catch {
      message = response.statusText || message
    }

    throw new Error(message)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return (await response.json()) as T
}

export async function apiFormRequest<T>(path: string, options: FormRequestOptions): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? 'POST',
    headers: {
      ...(options.token ? { Authorization: `Bearer ${options.token}` } : {})
    },
    body: options.formData
  })

  if (!response.ok) {
    let message = 'Request failed.'

    try {
      const errorPayload = (await response.json()) as { detail?: string }
      if (typeof errorPayload.detail === 'string') {
        message = errorPayload.detail
      }
    } catch {
      message = response.statusText || message
    }

    throw new Error(message)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return (await response.json()) as T
}

export { API_BASE_URL }
