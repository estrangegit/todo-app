<script setup lang="ts">
import { computed } from 'vue'
import { z } from 'zod'

import { Form, type FormSubmitEvent } from '@primevue/forms'
import { zodResolver } from '@primevue/forms/resolvers/zod'

import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Select from 'primevue/select'
import { TaskStatus } from '@/enums/task-status'
import type { Task } from '@/models/task'
import type { TaskFormData } from '@/models/task-form'

const props = defineProps<{
  task?: Task | null
}>()

const emit = defineEmits<{
  submit: [TaskFormData]
}>()

const resolver = zodResolver(
  z.object({
    title: z.string().trim().min(1, 'Le titre est obligatoire').max(255, 'Le titre est trop long'),
    status: z.enum(TaskStatus),
  }),
)

const initialValues = computed<TaskFormData>(() => ({
  title: props.task?.title ?? '',
  status: props.task?.status ?? TaskStatus.TODO,
}))

const statusOptions = [
  {
    label: 'À faire',
    value: TaskStatus.TODO,
  },
  {
    label: 'En cours',
    value: TaskStatus.IN_PROGRESS,
  },
  {
    label: 'Terminée',
    value: TaskStatus.DONE,
  },
]

function onSubmit(event: FormSubmitEvent) {
  if (!event.valid) {
    return
  }

  emit('submit', event.values as TaskFormData)
}
</script>

<template>
  <Form :resolver="resolver" :initialValues="initialValues" @submit="onSubmit" v-slot="$form">
    <div class="flex flex-column gap-4">
      <div class="flex flex-column gap-2">
        <label for="title"> Titre </label>
        <InputText id="title" name="title" fluid />
        <Message v-if="$form.title?.invalid" severity="error" size="small" variant="simple">
          {{ $form.title.error?.message }}
        </Message>
      </div>

      <div class="flex flex-column gap-2">
        <label for="status"> Statut </label>
        <Select
          id="status"
          name="status"
          :options="statusOptions"
          optionLabel="label"
          optionValue="value"
          fluid
        />
        <Message v-if="$form.status?.invalid" severity="error" size="small" variant="simple">
          {{ $form.status.error?.message }}
        </Message>
      </div>

      <div class="flex justify-content-end gap-2">
        <Button type="submit" label="Enregistrer" />
      </div>
    </div>
  </Form>
</template>
