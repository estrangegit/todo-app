import { ApiError } from './api.errors'

export class InvalidCredentialsError extends ApiError {
  constructor() {
    super("Nom d'utilisateur ou mot de passe incorrect.")
    this.name = 'InvalidCredentialsError'
  }
}
