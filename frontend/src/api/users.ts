import { api } from '@/api/api'
import type { User } from '@/models/user'

export async function getCurrentUser(): Promise<User> {
  const response = await api.get<User>('/users/me')

  return response.data
}
