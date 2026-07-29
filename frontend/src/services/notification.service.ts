import type { AppNotification } from '@/models/app-notification'

class NotificationService {
  private handler?: (notification: AppNotification) => void

  register(handler: (notification: AppNotification) => void) {
    this.handler = handler
  }

  notify(notification: AppNotification) {
    this.handler?.(notification)
  }

  success(detail: string, options: Partial<Omit<AppNotification, 'severity' | 'detail'>> = {}) {
    this.notify({
      severity: 'success',
      summary: options.summary ?? 'Succès',
      detail,
      action: options.action,
      life: options.life ?? 3000,
      group: options.group
    })
  }

  info(detail: string, options: Partial<Omit<AppNotification, 'severity' | 'detail'>> = {}) {
    this.notify({
      severity: 'info',
      summary: options.summary ?? 'Information',
      detail,
      action: options.action,
      life: options.life ?? 3000,
      group: options.group
    })
  }

  warn(detail: string, options: Partial<Omit<AppNotification, 'severity' | 'detail'>> = {}) {
    this.notify({
      severity: 'warn',
      summary: options.summary ?? 'Attention',
      detail,
      action: options.action,
      life: options.life ?? 3000,
      group: options.group
    })
  }

  error(detail: string, options: Partial<Omit<AppNotification, 'severity' | 'detail'>> = {}) {
    this.notify({
      severity: 'error',
      summary: options.summary ?? 'Erreur',
      detail,
      action: options.action,
      life: options.life ?? 3000,
      group: options.group
    })
  }
}

export const notificationService = new NotificationService()
