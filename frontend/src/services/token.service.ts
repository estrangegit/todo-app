class TokenService {
  private readonly key = 'access_token'

  get(): string | null {
    return localStorage.getItem(this.key)
  }

  set(token: string): void {
    localStorage.setItem(this.key, token)
  }

  remove(): void {
    localStorage.removeItem(this.key)
  }
}

export const tokenService = new TokenService()
