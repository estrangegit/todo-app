<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { getTasks } from '@/api/tasks'
import type { Task } from '@/models/task'

import TaskPaginator from '@/components/tasks/TaskPaginator.vue'
import TaskTable from '@/components/tasks/TaskTable.vue'
import TaskToolbar from '@/components/tasks/TaskToolbar.vue'
import TaskDialog from '@/components/tasks/TaskDialog.vue'

const tasks = ref<Task[]>([])
const loading = ref(false)

const page = ref(0)
const rows = ref(10)
const totalRecords = ref(0)

const dialogVisible = ref(false)

async function loadTasks() {
  loading.value = true

  try {
    const result = await getTasks(page.value, rows.value)

    tasks.value = result.items
    totalRecords.value = result.total_items
  } finally {
    loading.value = false
  }
}

async function changePage(event: { page: number; rows: number }) {
  page.value = event.page
  rows.value = event.rows

  await loadTasks()
}

function onCreateTask() {
    dialogVisible.value = true
}

onMounted(loadTasks)
</script>

<template>
  <div class="flex flex-column justify-content-between h-full">
    <TaskToolbar @create="onCreateTask"/>

    <div class="flex-1 overflow-hidden">
      <TaskTable :tasks="tasks" :loading="loading" />
    </div>

    <TaskPaginator :page="page" :rows="rows" :total-records="totalRecords" @page="changePage" />
  </div>

  <TaskDialog v-model:visible="dialogVisible" />
</template>
