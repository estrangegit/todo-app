import { api } from '@/api/api'
import type { User } from '@/models/user'

class UserService {
  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/users/me')

    return response.data
  }
}

export const userService = new UserService()
