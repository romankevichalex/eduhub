<template>
  <div class="post-card" @click="$emit('click')">
    <div class="post-content">{{ post.content }}</div>
    <div class="post-meta">
      <span class="post-name">{{ post.last_name }} {{ post.first_name }} {{ post.middle_name }}</span>
      <span>{{ formattedDate }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  post: Object,
})

const formattedDate = computed(() => {
  if (!props.post.created_at) return ''
  const date = new Date(props.post.created_at)
  return date.toLocaleDateString('ru-RU')
})

defineEmits(['click'])
</script>

<style scoped>
.post-card {
  background: var(--gray-message);
  border-radius: 27px;
  padding: 16px;
  cursor: pointer;
  transition: box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.post-card:active {
  transform: scale(0.99);
}
.post-content {
  font-size: 16px;
  line-height: 1.4;
  margin-bottom: 12px;
  color: #1a1a1a;
}
.post-name {
  font-size: 14px;
}
.post-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #888;
}
.comment-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>