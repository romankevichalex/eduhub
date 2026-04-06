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
        console.error('fetchSubjects error:', err)
      } finally {
        this.loading = false
      }
    },
    
  },
})