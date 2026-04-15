import { defineStore } from 'pinia'
import api from '@/services/api'

export const useUsersStore = defineStore('users', {
  state: () => ({
    users: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchUsers() {
      this.loading = true
      this.error = null
      try {
        const response = await api.get('/api/v1/admin/users')
        this.users = response.data
      } catch (err) {
        this.error = err.response?.data?.message || 'Ошибка загрузки пользователей'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    async verifyUser(userId) {
      try {
        await api.patch(`/api/v1/admin/users/${userId}/verify`)
        // Обновляем статус верификации в списке
        const user = this.users.find(u => u.id === userId)
        if (user) user.is_verified = true
        return true
      } catch (err) {
        this.error = err.response?.data?.message || 'Ошибка верификации'
        return false
      }
    },
    // Удаление пока заглушка
    async deleteUser(userId) {
      // TODO: реализовать после добавления эндпоинта
      console.log('Удаление пользователя', userId)
      alert('Функция удаления будет добавлена позже')
    }
  }
})