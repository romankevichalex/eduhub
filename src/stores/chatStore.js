import { defineStore } from 'pinia'
import api from '@/services/api'

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchHistory(subjectId) {
      this.loading = true
      this.error = null
      try {
        const response = await api.get('/api/v1/chat/history', {
          params: { subject_id: subjectId }
        })
        this.messages = response.data.messages || []
      } catch (err) {
        this.error = err.response?.data?.message || 'Ошибка загрузки истории'
        console.error(err)
      } finally {
        this.loading = false
      }
    },

    async sendMessage(subjectId, message) {
      this.loading = true
      this.error = null

      const userMsg = {
        id: Date.now(),
        role: 'user',
        content: message,
        created_at: new Date().toISOString()
      }
      this.messages.push(userMsg)
      
      try {
        const response = await api.post('/api/v1/chat/messages', {
          subject_id: subjectId,
          message: message
        })

        this.messages.push(response.data)
        return true
      } catch (err) {
        this.error = err.response?.data?.message || 'Ошибка отправки'

        this.messages.pop()
        return false
      } finally {
        this.loading = false
      }
    },
    
    clearMessages() {
      this.messages = []
      this.error = null
    }
  }
})