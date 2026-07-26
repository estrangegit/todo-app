import type { Task } from './task'

export interface TaskPage {
  items: Task[]
  page: number
  size: number
  total_items: number
  total_pages: number
}
