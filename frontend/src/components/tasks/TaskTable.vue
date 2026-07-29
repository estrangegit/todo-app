<script setup lang="ts">
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Tag from 'primevue/tag'
import { Button } from 'primevue'

import { TaskStatus } from '@/enums/task-status'
import type { Task } from '@/models/task'

defineProps<{
  tasks: Task[]
  loading: boolean
}>()

type TagSeverity = 'warn' | 'info' | 'success'

const severityMap: Record<TaskStatus, TagSeverity> = {
  [TaskStatus.TODO]: 'warn',
  [TaskStatus.IN_PROGRESS]: 'info',
  [TaskStatus.DONE]: 'success',
}

function getSeverity(status: TaskStatus): TagSeverity {
  return severityMap[status]
}
</script>

<template>
  <DataTable :value="tasks" :loading="loading" scrollable scrollHeight="flex">
    <Column field="title" header="Titre" />

    <Column header="Statut">
      <template #body="{ data }">
        <Tag :value="data.status" :severity="getSeverity(data.status)" />
      </template>
    </Column>

    <Column header="Actions">
      <template #body="{ data }">
        <Button
          class="mr-1"
          severity="secondary"
          icon="pi pi-pencil"
          @click="$emit('edit', data)"
        />
        <Button severity="secondary" icon="pi pi-trash" @click="$emit('delete', data)" />
      </template>
    </Column>
  </DataTable>
</template>
