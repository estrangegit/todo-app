<script setup lang="ts">
import Dialog from 'primevue/dialog'

const visible = defineModel<boolean>('visible')
</script>

<template>
  <Dialog
    v-model:visible="visible"
    header="Nouvelle tâche"
    :modal="true"
    :style="{ width: '40rem' }"
  >
    <p>Le formulaire viendra ici.</p>
  </Dialog>
</template>
