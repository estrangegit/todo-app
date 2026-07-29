import type { TaskStatus } from '@/enums/task-status'

export interface TaskFormData {
  title: string
  status: TaskStatus
}
