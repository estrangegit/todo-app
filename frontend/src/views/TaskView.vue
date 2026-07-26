<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { getTasks } from '@/api/tasks'
import type { Task } from '@/models/task'

const tasks = ref<Task[]>([])
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  loading.value = true

  try {
    const page = await getTasks()
    tasks.value = page.items
  } catch {
    error.value = 'Impossible de charger les tâches.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <h1>Mes tâches</h1>

  <p v-if="loading">Chargement...</p>

  <p v-else-if="error">
    {{ error }}
  </p>

  <ul v-else>
    <li v-for="task in tasks" :key="task.id">
      {{ task.title }}
    </li>
  </ul>
</template>
