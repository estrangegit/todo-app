import type { TokenResponse } from '@/types/auth'
import { api } from './api'
import axios from 'axios'
import { InvalidCredentialsError } from '@/errors/auth.errors'
import { NetworkError, ServerError } from '@/errors/api.errors'

export async function login(username: string, password: string): Promise<TokenResponse> {
  try {
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
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (!error.response) {
        throw new NetworkError()
      }

      switch (error.response.status) {
        case 401:
          throw new InvalidCredentialsError()

        default:
          if (error.response.status >= 500) {
            throw new ServerError()
          }
      }
    }

    throw error
  }
}
