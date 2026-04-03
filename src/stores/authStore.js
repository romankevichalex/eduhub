import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || sessionStorage.getItem('token') || null,
    loading: false,
    error: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(email, password, rememberMe = false) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('/api/v1/auth/login', { email, password })
        this.token = response.data.access_token
        if (rememberMe) {
          localStorage.setItem('token', this.token)
        } else {
          sessionStorage.setItem('token', this.token)
        }
        await this.fetchMe()
        return true
      } catch (err) {
        if (!err.response) {
          this.error = 'Нет соединения с сервером. Проверьте интернет'
          return false
        }
        console.error('Login error details:', err.response?.data)
        
        // Получаем статус и данные ошибки
        const status = err.response?.status
        const data = err.response?.data

        // Формируем сообщение в зависимости от статуса
        let userMessage = 'Ошибка входа'
        if (status === 401) {
          userMessage = data?.message || 'Неверный email или пароль'
        } else if (status === 422) {
          // Валидационная ошибка (например, неправильный формат email)
          userMessage = data?.message || 'Проверьте правильность введённых данных'
        } else if (status === 429) {
          userMessage = 'Слишком много попыток входа. Попробуйте позже'
        } else if (status >= 500) {
          userMessage = 'Сервер временно недоступен. Повторите попытку позже'
        } else if (status === 400) {
          userMessage = data?.message || 'Некорректный запрос'
        }
        
        this.error = userMessage
        return false
      } finally {
        this.loading = false
      }
    },

    async register(userData) {
      this.loading = true
      this.error = null
      try {
        await api.post('/api/v1/auth/register', userData)
        // после регистрации можно сразу залогиниться или перенаправить на страницу входа
        return true
      } catch (err) {
        if (!err.response) {
          this.error = 'Нет соединения с сервером. Проверьте интернет'
          return false
        }
        console.error('Registration error details:', err.response?.data);

        const status = err.response.status
        const data = err.response.data

        // Обработка разных статусов
        if (status === 400) {
          this.error = data?.message || 'Пользователь с таким email уже зарегистрирован'
        } else if (status === 409) {
          // Часто 409 означает конфликт, например email уже существует
          this.error = data?.message || 'Пользователь с таким email уже зарегистрирован'
        } else if (status === 422) {
          // Валидационная ошибка — можно попробовать вытащить детали
          if (data?.errors) {
            // Если ошибки приходят в виде объекта { email: ['...'], password: ['...'] }
            const messages = Object.values(data.errors).flat()
            this.error = messages.join(', ')
          } else {
            this.error = data?.message || 'Проверьте правильность введённых данных'
          }
        } else if (status === 429) {
          this.error = 'Слишком много попыток регистрации. Попробуйте позже'
        } else if (status >= 500) {
          this.error = 'Сервер временно недоступен. Повторите попытку позже'
        } else {
          this.error = data?.message || 'Ошибка регистрации'
        }
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchMe() {
      if (!this.token) return
      try {
        const response = await api.get('/api/v1/auth/me')
        this.user = response.data
      } catch (err) {
        // если токен невалиден, очищаем его
        this.logout()
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      sessionStorage.removeItem('token')
    },
  },
})