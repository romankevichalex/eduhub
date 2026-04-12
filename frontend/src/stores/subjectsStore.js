import { defineStore } from 'pinia'
import api from '@/services/api'

export const useSubjectsStore = defineStore('subjects', {
  state: () => ({
    subjects: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchSubjects() {
      this.loading = true
      this.error = null
      try {
        const response = await api.get('/api/v1/subjects/')
        this.subjects = response.data
      } catch (err) {
        this.error = err.response?.data?.message || 'Ошибка загрузки предметов'
        console.error(err)
      } finally {
        this.loading = false
      }
    },

    async fetchSubjectById(id) {
      try {
        const response = await api.get(`/api/v1/subjects/${id}`)
        return response.data
      } catch (err) {
        console.error(err)
        throw err
      }
    },

    async createSubject(data) {
      try {
        const response = await api.post('/api/v1/subjects/', data)
        // Добавляем новый предмет в список (в начало или конец)
        this.subjects.push(response.data)
        console.log(data)
        return response.data
      } catch (err) {
        this.error = err.response?.data?.message || 'Ошибка создания предмета'
        console.log(err.response?.data?.message)
        throw err
      }
    },

    async updateSubject(id, data) {
      try {
        const response = await api.patch(`/api/v1/subjects/${id}`, data)
        // Обновляем предмет в списке
        const index = this.subjects.findIndex(s => s.id === id)
        if (index !== -1) {
          this.subjects[index] = { ...this.subjects[index], ...response.data }
        }
        return response.data
      } catch (err) {
        this.error = err.response?.data?.message || 'Ошибка обновления предмета'
        throw err
      }
    },

    async deleteSubject(id) {
      try {
        await api.delete(`/api/v1/subjects/${id}`)
        // Удаляем из списка
        this.subjects = this.subjects.filter(s => s.id !== id)
      } catch (err) {
        this.error = err.response?.data?.message || 'Ошибка удаления предмета'
        throw err
      }
    },
  },
})