import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { login as loginApi } from '@/api/auth'
import type { User } from '@/models/user'
import router from '@/router'
import { tokenService } from '@/services/token.service'
import { userService } from '@/services/user.service'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(tokenService.get())
  const user = ref<User | null>(null)
  const username = computed(() => user.value?.username ?? '')
  const isAuthenticated = computed(() => token.value !== null)

  async function login(username: string, password: string): Promise<void> {
    const response = await loginApi(username, password)

    token.value = response.access_token
    tokenService.set(response.access_token)

    user.value = await userService.getCurrentUser()
  }

  async function initialize(): Promise<void> {
    if (!token.value) {
      return
    }

    try {
      user.value = await userService.getCurrentUser()
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
