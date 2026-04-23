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
        const user = this.users.find(u => u.id === userId)
        if (user) user.is_verified = true
        return true
      } catch (err) {
        this.error = err.response?.data?.message || 'Ошибка верификации'
        return false
      }
    },
    async deleteUser(userId) {
      try {
        await api.delete(`/api/v1/admin/users/${userId}`)
        this.users = this.users.filter(u => u.id !== userId)
      } catch (err) {
        this.error = err.response?.data?.message || 'Ошибка удаления пользователя'
        throw err
      }
    }
  }
})