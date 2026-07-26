<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

import Menubar from 'primevue/menubar'
import Button from 'primevue/button'

import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const items = computed(() => [
  {
    label: 'Accueil',
    icon: 'pi pi-home',
    command: () => router.push({ name: 'home' }),
  },
  {
    label: 'Tâches',
    icon: 'pi pi-list-check',
    command: () => router.push({ name: 'tasks' }),
  },
])

function logout(): void {
  authStore.logout()
}
</script>

<template>
  <Menubar :model="items">
    <template #end>
      <div class="flex align-items-center gap-3">
        <span> Bonjour {{ authStore.username }} </span>
        <Button label="Déconnexion" icon="pi pi-sign-out" text @click="logout" />
      </div>
    </template>
  </Menubar>
</template>
