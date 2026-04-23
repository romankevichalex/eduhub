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

    <div class="comments-list" ref="commentsList" v-if="!loading">
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
      />
      <div v-if="comments.length === 0" class="empty">Нет комментариев</div>
    </div>
    <div v-else class="loading">Загрузка...</div>

    <div class="input-area">
      <textarea
        v-model="newComment"
        @keydown.enter.prevent="submitComment"
        placeholder="Напишите комментарий..."
        rows="2"
      ></textarea>
      <button @click="submitComment" :disabled="!newComment.trim() || sending">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
          <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m5 12l-.604-5.437C4.223 5.007 5.825 3.864 7.24 4.535l11.944 5.658c1.525.722 1.525 2.892 0 3.614L7.24 19.466c-1.415.67-3.017-.472-2.844-2.028zm0 0h7" stroke-width="2"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePostsStore } from '@/stores/postsStore'
import CommentItem from '@/components/posts/CommentItem.vue'

const route = useRoute()
const router = useRouter()
const postsStore = usePostsStore()

const postId = ref(route.params.postId)
const comments = ref([])
const loading = ref(false)
const sending = ref(false)
const newComment = ref('')
const commentsList = ref(null)

const goBack = () => {
  router.go(-1)
}

const scrollToBottom = () => {
  nextTick(() => {
    if (commentsList.value) {
      commentsList.value.scrollTop = commentsList.value.scrollHeight
    }
  })
}

const fetchComments = async () => {
  loading.value = true
  await postsStore.fetchComments(postId.value)
  comments.value = postsStore.comments[postId.value] || []
  loading.value = false
  scrollToBottom()
}

const submitComment = async () => {
  if (!newComment.value.trim() || sending.value) return
  sending.value = true
  const success = await postsStore.addComment(postId.value, newComment.value)
  if (success) {
    newComment.value = ''
    comments.value = postsStore.comments[postId.value] || []
    scrollToBottom()
  } else {
    alert(postsStore.error || 'Ошибка отправки комментария')
  }
  sending.value = false
}

onMounted(() => {
  fetchComments()
})

watch(() => comments.value.length, () => scrollToBottom())
</script>

<style scoped>
.comments-page {
  min-height: 100vh;
  background: white;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.comments-header {
  background: var(--gradient);
  padding: 20px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.2);
  flex-shrink: 0;
}

.back-button {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.comments-title {
  color: white;
  font-size: 22px;
  font-weight: 600;
  margin: 0;
}

.comments-list {
  flex: 1;
  overflow-y: auto;
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

.input-area {
  display: flex;
  gap: 8px;
  padding: 12px;
  border-top: 1px solid #eee;
  background: white;
  flex-shrink: 0;
}

.input-area textarea {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 27px;
  padding: 10px 12px;
  resize: none;
  font-family: inherit;
  font-size: 14px;
  box-sizing: border-box;
}

.input-area textarea:focus {
  outline: none;
  border-color: var(--main-color-b);
}

.input-area button {
  background: var(--main-color-b);
  color: white;
  border: none;
  border-radius: 27px;
  width: 48px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.2s;
}

.input-area button:disabled {
  opacity: 0.6;
}

.input-area button svg {
  stroke: white;
}
</style>