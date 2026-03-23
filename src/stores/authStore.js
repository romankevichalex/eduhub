import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    autoLogin: false
  }),
  actions: {
    // Мок-вход – просто имитируем успешный ответ
    async login(email, password, autoLogin) {
      // Здесь потом будет реальный вызов API
      // Имитируем задержку
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          // Условная проверка: если почта и пароль не пустые – успешно
          if (email && password) {
            this.user = { email }
            this.isAuthenticated = true
            this.autoLogin = autoLogin
            // Сохраняем токен в localStorage, если нужно
            if (autoLogin) {
              localStorage.setItem('user', JSON.stringify({ email }))
            }
            resolve()
          } else {
            reject(new Error('Неверные данные'))
          }
        }, 500)
      })
    },
    logout() {
      this.user = null
      this.isAuthenticated = false
      this.autoLogin = false
      localStorage.removeItem('user')
    },
    // Проверка автовхода при загрузке приложения
    checkAutoLogin() {
      const savedUser = localStorage.getItem('user')
      if (savedUser) {
        this.user = JSON.parse(savedUser)
        this.isAuthenticated = true
        this.autoLogin = true
      }
    }
  }
})