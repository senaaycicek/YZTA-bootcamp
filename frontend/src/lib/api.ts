// API istemcisi — JWT token'ı her isteğe ekler.
//
// NOT (güvenlik): Token şu an localStorage'da tutuluyor. Production'da XSS'e
// karşı daha güvenli seçenek, backend'in token'ı httpOnly bir cookie olarak
// set etmesidir (bkz. README). Bu projede basitlik için Bearer + localStorage
// yaklaşımı kullanıldı.
import type { GenerateResult, Product, ProductInput, User } from './types'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

const TOKEN_KEY = 'orkestrai_token'

export const tokenStore = {
  get: () => localStorage.getItem(TOKEN_KEY),
  set: (token: string) => localStorage.setItem(TOKEN_KEY, token),
  clear: () => localStorage.removeItem(TOKEN_KEY),
}

export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  }
  const token = tokenStore.get()
  if (token) headers.Authorization = `Bearer ${token}`

  let res: Response
  try {
    res = await fetch(`${API_URL}${path}`, { ...options, headers })
  } catch {
    throw new ApiError(0, 'Sunucuya ulaşılamıyor. Backend çalışıyor mu?')
  }

  if (!res.ok) {
    let detail = 'Beklenmeyen bir hata oluştu.'
    try {
      const body = await res.json()
      if (typeof body.detail === 'string') detail = body.detail
    } catch {
      /* gövde JSON değilse varsayılan mesaj kalır */
    }
    if (res.status === 401) tokenStore.clear()
    throw new ApiError(res.status, detail)
  }

  return res.json() as Promise<T>
}

async function requestBlob(path: string, options: RequestInit = {}): Promise<Blob> {
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  }
  const token = tokenStore.get()
  if (token) headers.Authorization = `Bearer ${token}`

  let res: Response
  try {
    res = await fetch(`${API_URL}${path}`, { ...options, headers })
  } catch {
    throw new ApiError(0, 'Sunucuya ulaşılamıyor. Backend çalışıyor mu?')
  }

  if (!res.ok) {
    let detail = 'Beklenmeyen bir hata oluştu.'
    try {
      const body = await res.json()
      if (typeof body.detail === 'string') detail = body.detail
    } catch {
      detail = await res.text()
    }
    if (res.status === 401) tokenStore.clear()
    throw new ApiError(res.status, detail)
  }

  return res.blob()
}

// ---------- Auth ----------
export const api = {
  register: (email: string, password: string) =>
    request<{ access_token: string }>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),

  login: (email: string, password: string) =>
    request<{ access_token: string }>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),

  me: () => request<User>('/api/auth/me'),

  // ---------- Products ----------
  listProducts: () => request<Product[]>('/api/products'),

  getProduct: (id: number) => request<Product>(`/api/products/${id}`),

  getProductImage: (id: number) => requestBlob(`/api/products/${id}/image`),

  createProduct: (input: ProductInput) =>
    request<Product>('/api/products', {
      method: 'POST',
      body: JSON.stringify(input),
    }),

  generate: (id: number) =>
    request<GenerateResult>(`/api/products/${id}/generate`, { method: 'POST' }),
}
