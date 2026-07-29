export type AppNotificationSeverity = 'success' | 'info' | 'warn' | 'error'

export interface AppNotificationAction {
  label: string
  onClick: () => void
}

export interface AppNotification {
  severity: AppNotificationSeverity
  summary: string
  detail: string
  life?: number
  action?: AppNotificationAction
  group?: string
}
