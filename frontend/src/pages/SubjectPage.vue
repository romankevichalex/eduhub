<template>
  <div class="subject-page">
    <div class="subject-top">
      <div class="subject-header">
        <button class="back-button" @click="goBack">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M15 18L9 12L15 6" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <h1 class="subject-title">{{ subjectName }}</h1>
      </div>

      <div class="tabs">
        <button class="tab" :class="{ active: activeTab === 'posts' }" @click="activeTab = 'posts'">
          <svg width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7.09 2.75a4 4 0 0 0-4 4v6.208a4 4 0 0 0 4 4h.093v3.792a.5.5 0 0 0 .839.368l4.52-4.16h4.369a4 4 0 0 0 4-4V6.75a4 4 0 0 0-4-4z"/></svg>
        </button>
        <button class="tab" :class="{ active: activeTab === 'ai' }" @click="activeTab = 'ai'">
          <svg width="24" height="24" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="1.5"><path stroke-linecap="round" d="M17.5 17.5L22 22"/><path d="M20 11a9 9 0 1 0-18 0a9 9 0 0 0 18 0Z"/><path stroke-linecap="round" d="m6.5 14l1.842-5.526a.694.694 0 0 1 1.316 0L11.5 14m3-6v6m-7-2h3"/></g></svg>
        </button>
        <button class="tab" :class="{ active: activeTab === 'widgets' }" @click="activeTab = 'widgets'">
          <svg width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M5 3h13a3 3 0 0 1 3 3v13a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3V6a3 3 0 0 1 3-3m0 1a2 2 0 0 0-2 2v3h5V4zM3 19a2 2 0 0 0 2 2h3v-5H3zm5-9H3v5h5zm10 11a2 2 0 0 0 2-2v-3h-5v5zm2-11h-5v5h5zm0-4a2 2 0 0 0-2-2h-3v5h5zM9 4v5h5V4zm0 17h5v-5H9zm5-11H9v5h5z" stroke-width="0.5" stroke="currentColor"/></svg>
        </button>
      </div>
    </div>

    <div class="tab-content">
      <div v-if="activeTab === 'posts'" class="posts-list">
        <PostCard
          v-for="post in postsStore.posts"
          :key="post.id"
          :post="post"
          @click="goToComments(post.id)"
        />
        <div v-if="postsStore.loading" class="loading">Загрузка...</div>
        <div v-else-if="postsStore.posts.length === 0" class="empty">Пока нет постов</div>
      </div>

      <div v-else-if="activeTab === 'ai'" class="ai-chat-container">
        <AIChat :subjectId="Number(subjectId)" />
      </div>

      <div v-else-if="activeTab === 'widgets'" class="widgets-placeholder">
        <div class="widget-button">Виджет 1</div>
        <div class="widget-button">Виджет 2</div>
        <div class="widget-button">Виджет 3</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePostsStore } from '@/stores/postsStore'
import PostCard from '@/components/posts/PostCard.vue'
import AIChat from '@/components/chat/AIChat.vue'

const route = useRoute()
const router = useRouter()
const postsStore = usePostsStore()

const subjectId = ref(route.params.id)
const subjectName = ref(route.query.name || 'Предмет')
const activeTab = ref('posts')

const goBack = () => router.push('/subjects')
const goToComments = (postId) => router.push(`/subjects/${subjectId.value}/comments/${postId}`)

onMounted(() => {
  postsStore.fetchPosts(subjectId.value)
})
</script>

<style scoped>
.subject-page {
  min-height: 100vh;
  height: 100vh;            /* ← фиксированная высота как в CommentsPage */
  background: white;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.subject-top {
  background: var(--gradient);
  border-bottom: 1px solid rgba(255,255,255,0.2);
  padding-bottom: 12px;
  flex-shrink: 0;
}

.subject-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 16px 8px 16px;
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

.subject-title {
  color: white;
  font-size: 16px;          
  font-weight: 600;
  margin: 0;
}

.tabs {
  display: flex;
  justify-content: center;
  gap: 16px;
  padding: 0 16px;
}

.tab {
  background: rgba(255,255,255,0.2);
  border: none;
  border-radius: 27px;
  padding: 8px 20px;
  font-size: 15px;
  font-weight: 500;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 100px;
  text-align: center;
}

.tab.active {
  background: white;
  color: var(--main-color-b);
}

.tab-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.ai-chat-container {
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

.posts-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.loading,
.empty,
.widgets-placeholder {
  text-align: center;
  padding: 40px;
  color: #666;
}

.widgets-placeholder {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.widget-button {
  background: #f0f0f0;
  border-radius: 27px;
  padding: 14px;
  text-align: center;
  font-size: 16px;
  color: #333;
  cursor: pointer;
}

.widget-button:active {
  background: #e0e0e0;
}
</style>