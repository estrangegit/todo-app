import { api } from '@/api/api'
import type { Task } from '@/models/task'
import type { TaskFormData } from '@/models/task-form'
import type { TaskPage } from '@/models/task-page'

class TaskService {
  async findAll(page = 1, size = 10): Promise<TaskPage> {
    const response = await api.get<TaskPage>('/tasks?sort=title', {
      params: {
        page,
        size,
      },
    })
    return response.data
  }

  async create(data: TaskFormData): Promise<Task> {
    const response = await api.post<Task>('/tasks', data)
    return response.data
  }

  async update(id: number, data: TaskFormData): Promise<Task> {
    const response = await api.patch<Task>(`/tasks/${id}`, data)
    return response.data
  }

  async delete(id: number): Promise<Task> {
    const response = await api.delete<Task>(`/tasks/${id}`)
    return response.data
  }
}

export const taskService = new TaskService()
