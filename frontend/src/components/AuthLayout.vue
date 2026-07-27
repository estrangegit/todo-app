<script setup lang="ts">
import AppNavbar from '@/components/AppNavbar.vue'
</script>

<template>
  <div class="flex flex-column h-full">
    <AppNavbar />

    <main class="flex-1 overflow-hidden p-4">
      <RouterView />
    </main>
  </div>
</template>
