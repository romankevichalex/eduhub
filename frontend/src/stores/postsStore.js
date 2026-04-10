import { defineStore } from 'pinia'
import api from '@/services/api'

export const usePostsStore = defineStore('posts', {
  state: () => ({
    posts: [],           // посты текущего предмета
    comments: {},        // объект: ключ postId -> массив комментариев
    loading: false,
    error: null,
  }),
  actions: {
    async fetchPosts(subjectId) {
      this.loading = true
      this.error = null
      try {
        const response = await api.get(`/api/v1/subjects/${subjectId}/posts`)
        this.posts = response.data
      } catch (err) {
        this.error = err.response?.data?.message || 'Ошибка загрузки постов'
        console.error(err)
      } finally {
        this.loading = false
      }
    },

    async fetchComments(postId) {
      if (this.comments[postId]) return // уже загружены
      try {
        const response = await api.get(`/api/v1/posts/${postId}/comments`)
        this.comments[postId] = response.data
      } catch (err) {
        console.error(err)
        this.comments[postId] = []
      }
    },

    async addComment(postId, content) {
      try {
        const response = await api.post(`/api/v1/posts/${postId}/comments`, { content })
        // добавляем новый комментарий в начало или конец списка
        if (!this.comments[postId]) this.comments[postId] = []
        this.comments[postId].push(response.data)
        return true
      } catch (err) {
        this.error = err.response?.data?.message || 'Ошибка отправки комментария'
        return false
      }
    },
  },
})