<script setup lang="ts">
import { Button } from 'primevue'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'
import { RouterView } from 'vue-router'

import { notificationService } from '@/services/notification.service'
import { onMounted } from 'vue'

const toast = useToast()

onMounted(() => {
  notificationService.register((notification) => {
    toast.add({
      ...notification,
    })
  })
})
</script>

<template>
  <!-- Toast classique -->
  <Toast position="top-right" />

  <!-- Toast avec bouton Annuler -->
  <Toast group="undo" position="top-right">
    <template #message="{ message }">
      <div class="flex justify-content-between align-items-start w-full">
        <div class="flex flex-column gap-2">
          <strong class="p-toast-summary">{{ message.summary }}</strong>
          <span class="p-toast-detail">{{ message.detail }}</span>
          <Button
            v-if="message.action"
            :label="message.action.label"
            link
            size="small"
            class="p-0 mt-2 justify-content-start"
            @click="message.action.onClick(); toast.removeGroup('undo');"
          />
        </div>
      </div>
    </template>
  </Toast>

  <RouterView />
</template>
