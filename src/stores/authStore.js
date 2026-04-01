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
          localStorage.setItem('token', token)
        } else {
          sessionStorage.setItem('token', token)
        }
        await this.fetchMe()
        return true
      } catch (err) {
        console.error('Login error details:', err.response?.data);
        this.error = err.response?.data?.message || 'Ошибка входа'
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
        console.error('Registration error details:', err.response?.data);
        this.error = err.response?.data?.message || 'Ошибка регистрации'
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