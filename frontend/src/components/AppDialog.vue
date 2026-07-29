<script setup lang="ts">
import Dialog from 'primevue/dialog'

const visible = defineModel<boolean>('visible')
defineProps<{ header: string }>()
</script>

<template>
  <Dialog v-model:visible="visible" :header="header" :modal="true" :style="{ width: '30vw' }">
    <slot />
  </Dialog>
</template>
