import { api } from '@/api/api'
import type { TaskPage } from '@/models/task-page'

export async function getTasks(page = 1, size = 10): Promise<TaskPage> {
  const response = await api.get<TaskPage>('/tasks', {
    params: {
      page,
      size,
    },
  })

  return response.data
}
