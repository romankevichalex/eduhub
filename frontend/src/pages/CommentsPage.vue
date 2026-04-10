<template>
  <div class="comments-page">
    <div class="comments-header">
      <button class="back-button" @click="goBack">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M15 18L9 12L15 6" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      <h1 class="comments-title">Комментарии</h1>
    </div>

    <div class="comments-list" v-if="!loading">
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
      />
      <div v-if="comments.length === 0" class="empty">Нет комментариев</div>
    </div>
    <div v-else class="loading">Загрузка...</div>

    <div class="add-comment">
      <textarea
        v-model="newComment"
        placeholder="Напишите комментарий..."
        rows="2"
      ></textarea>
      <button @click="submitComment" :disabled="!newComment.trim()">Отправить</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePostsStore } from '@/stores/postsStore'
import CommentItem from '@/components/posts/CommentItem.vue'

const route = useRoute()
const router = useRouter()
const postsStore = usePostsStore()

const postId = ref(route.params.postId)
const comments = ref([])
const loading = ref(false)
const newComment = ref('')

const goBack = () => {
  router.go(-1) // или router.push(`/subjects/${route.params.id}`)
}

const fetchComments = async () => {
  loading.value = true
  await postsStore.fetchComments(postId.value)
  comments.value = postsStore.comments[postId.value] || []
  loading.value = false
}

const submitComment = async () => {
  if (!newComment.value.trim()) return
  const success = await postsStore.addComment(postId.value, newComment.value)
  if (success) {
    newComment.value = ''
    // обновляем список комментариев
    comments.value = postsStore.comments[postId.value] || []
  } else {
    alert('Ошибка при отправке комментария')
  }
}

onMounted(() => {
  fetchComments()
})
</script>

<style scoped>
.comments-page {
  min-height: 100vh;
  background: white;
  display: flex;
  flex-direction: column;
}
.comments-header {
  background: var(--gradient);
  padding: 20px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.2);
}
.back-button {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
}
.comments-title {
  color: white;
  font-size: 22px;
  font-weight: 600;
  margin: 0;
}
.comments-list {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.empty, .loading {
  text-align: center;
  padding: 40px;
  color: #666;
}
.add-comment {
  padding: 16px;
  border-top: 1px solid #eee;
  background: white;
}
.add-comment textarea {
  width: 100%;
  border: 1px solid #ddd;
  border-radius: 27px;
  padding: 12px;
  font-size: 14px;
  resize: vertical;
  margin-bottom: 8px;
  box-sizing: border-box;
}
.add-comment button {
  background: var(--main-color-b);
  color: white;
  border: none;
  border-radius: 27px;
  padding: 10px 20px;
  font-size: 14px;
  cursor: pointer;
  width: 100%;
}
.add-comment button:disabled {
  opacity: 0.6;
}
</style>