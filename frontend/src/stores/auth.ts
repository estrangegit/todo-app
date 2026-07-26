import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

import { login as loginApi } from '@/api/auth'
import { tokenService } from '@/services/token.service'
import router from '@/router'
import type { User } from '@/models/user'
import { getCurrentUser } from '@/api/users'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(tokenService.get())
  const user = ref<User | null>(null)
  const username = computed(() => user.value?.username ?? '')
  const isAuthenticated = computed(() => token.value !== null)

  async function login(username: string, password: string): Promise<void> {
    const response = await loginApi(username, password)

    token.value = response.access_token
    tokenService.set(response.access_token)

    user.value = await getCurrentUser()
  }

  async function initialize(): Promise<void> {
    if (!token.value) {
      return
    }

    try {
      user.value = await getCurrentUser()
    } catch {
      clearSession()
    }
  }

  function clearSession(): void {
    token.value = null
    user.value = null
    tokenService.remove()
  }

  function logout(): void {
    clearSession()
    router.push({ name: 'login' })
  }

  return {
    token,
    username,
    isAuthenticated,
    login,
    initialize,
    logout,
  }
})
