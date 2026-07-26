import type { TokenResponse } from '@/types/auth'
import { api } from './api'

export async function login(username: string, password: string): Promise<TokenResponse> {
  const data = new URLSearchParams({
    username,
    password,
  })

  const response = await api.post('/auth/login', data, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })

  return response.data
}
