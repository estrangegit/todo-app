<script setup lang="ts">
import Card from 'primevue/card'

import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <Card>
    <template #title> Bienvenue {{ authStore.username }} </template>

    <template #content>
      <p>Gérez vos tâches grâce au menu de navigation.</p>
    </template>
  </Card>
</template>
