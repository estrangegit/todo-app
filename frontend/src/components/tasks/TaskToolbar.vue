<script setup lang="ts">
import Button from 'primevue/button'

const emit = defineEmits<{
  create: []
}>()
</script>

<template>
  <div class="flex justify-content-between align-items-center mb-3">
    <h2>Mes tâches</h2>
    <Button label="Nouvelle tâche" icon="pi pi-plus" @click="emit('create')" />
  </div>
</template>
