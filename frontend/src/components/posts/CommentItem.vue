<template>
  <div class="comment-message">
    <div class="comment-content">{{ comment.content }}</div>
    <div class="comment-meta">
      <span class="comment-author">{{ comment.last_name }} {{ comment.first_name }}</span>
      <span class="comment-time">{{ formattedDate }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  comment: Object
})

const formattedDate = computed(() => {
  if (!props.comment.created_at) return ''
  const date = new Date(props.comment.created_at)
  return date.toLocaleDateString('ru-RU') + ' ' + date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
})
</script>

<style scoped>
.comment-message {
  max-width: 85%;
  align-self: flex-start;
  background: #f0f0f0;
  border-radius: 20px;
  border-bottom-left-radius: 4px;
  padding: 10px 14px;
  word-wrap: break-word;
}

.comment-content {
  font-size: 14px;
  line-height: 1.4;
}

.comment-meta {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #666;
  margin-top: 6px;
  gap: 8px;
}

.comment-author {
  font-weight: 500;
}
</style>