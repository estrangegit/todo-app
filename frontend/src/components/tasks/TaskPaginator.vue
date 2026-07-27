<script setup lang="ts">
import Paginator, { type PageState } from 'primevue/paginator'

const props = defineProps<{
  page: number
  rows: number
  totalRecords: number
}>()

const emit = defineEmits<{
  page: [PageState]
}>()
</script>

<template>
  <Paginator
    :first="page * rows"
    :rows="rows"
    :totalRecords="totalRecords"
    :rowsPerPageOptions="[5, 10, 20]"
    @page="emit('page', $event)"
  />
</template>
