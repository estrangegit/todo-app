<script setup lang="ts">
import { onMounted, ref } from 'vue'

import type { Task } from '@/models/task'
import { taskService } from '@/services/task.service'

import AppDialog from '@/components/AppDialog.vue'
import TaskForm from '@/components/tasks/TaskForm.vue'
import TaskPaginator from '@/components/tasks/TaskPaginator.vue'
import TaskTable from '@/components/tasks/TaskTable.vue'
import TaskToolbar from '@/components/tasks/TaskToolbar.vue'
import type { TaskFormData } from '@/models/task-form'
import { notificationService } from '@/services/notification.service'

const tasks = ref<Task[]>([])
const loading = ref(false)

const page = ref(0)
const rows = ref(10)
const totalRecords = ref(0)

const dialogVisible = ref(false)

const selectedTask = ref<Task | null>(null)

interface PendingDeletion {
  task: Task
  index: number
  timeoutId?: ReturnType<typeof setTimeout>
}

const pendingDeletion = ref<PendingDeletion | null>(null)

async function loadTasks() {
  loading.value = true

  try {
    const result = await taskService.findAll(page.value, rows.value)

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
  selectedTask.value = null
}

function onEditTask(task: Task) {
  dialogVisible.value = true
  selectedTask.value = task
}

async function onDeleteTask(task: Task) {
  const index = tasks.value.findIndex((t) => t.id === task.id)

  if (index === -1) {
    return
  }

  const timeoutId = setTimeout(async () => {
    try {
      await taskService.delete(task.id)
    } catch (error) {
      console.error(error)
      tasks.value.splice(index, 0, task)
    } finally {
      pendingDeletion.value = null
    }
  }, 3000)

  pendingDeletion.value = { task, index, timeoutId }
  tasks.value = tasks.value.filter((t) => t.id !== task.id)

  notificationService.info('Tâche supprimée avec succès.', {
    group: 'undo',
    action: {
      label: 'Annuler',
      onClick: () => onUndoDelete(),
    },
  })
}

async function onUndoDelete() {
  const pending = pendingDeletion.value
  if (!pending) {
    return
  }
  clearTimeout(pending.timeoutId)
  tasks.value.splice(pending.index, 0, pending.task)
  pendingDeletion.value = null
}

async function saveTask(data: TaskFormData) {
  try {
    if (selectedTask.value) {
      await taskService.update(selectedTask.value.id, data)
      notificationService.success('Tâche mise à jour avec succès.')
    } else {
      await taskService.create(data)
      notificationService.success('Tâche créée avec succès.')
    }
    dialogVisible.value = false
    selectedTask.value = null
    await loadTasks()
  } catch (error) {
    notificationService.error("Une erreur est survenue lors de l'enregistrement de la tâche.")
    console.error(error)
  }
}

onMounted(loadTasks)
</script>

<template>
  <div class="flex flex-column justify-content-between h-full">
    <TaskToolbar @create="onCreateTask" />
    <div class="flex-1 overflow-hidden">
      <TaskTable :tasks="tasks" :loading="loading" @edit="onEditTask" @delete="onDeleteTask" />
    </div>
    <TaskPaginator :page="page" :rows="rows" :total-records="totalRecords" @page="changePage" />
  </div>
  <AppDialog
    v-model:visible="dialogVisible"
    :header="selectedTask ? 'Modifier une tâche' : 'Nouvelle tâche'"
  >
    <TaskForm :task="selectedTask" @submit="saveTask" />
  </AppDialog>
</template>
