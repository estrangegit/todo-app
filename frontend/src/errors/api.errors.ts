export class ApiError extends Error {}

export class NetworkError extends ApiError {
  constructor() {
    super('Impossible de contacter le serveur.')
    this.name = 'NetworkError'
  }
}

export class ServerError extends ApiError {
  constructor() {
    super('Une erreur est survenue sur le serveur.')
    this.name = 'ServerError'
  }
}
