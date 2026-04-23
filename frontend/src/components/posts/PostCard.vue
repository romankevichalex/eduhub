<template>
  <div class="post-card" @click="$emit('click')">
    <div class="post-content">{{ post.content }}</div>
    <div class="post-meta">
      <span class="post-name">{{ post.last_name }} {{ post.first_name }} {{ post.middle_name }}</span>
      <span>{{ formattedTime }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { formatMessageTime } from '@/services/dateFormatter'

const props = defineProps({
  post: Object,
})

const formattedTime = computed(() => {
  return formatMessageTime(props.post.created_at, {showDate: true})
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
  white-space: pre-wrap;
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