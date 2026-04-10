<template>
  <div class="comment-item">
    <div class="comment-content">{{ comment.content }}</div>
    <div class="comment-meta">
      <span>{{ comment.last_name }} {{ comment.first_name}}</span>
      <span>{{ formattedDate }}</span>
    </div>
  </div>
</template>

<script setup>
import { Comment, computed } from 'vue'

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
.comment-item {
  background: var(--gray-message);
  border-radius: 27px;
  padding: 12px 16px;
}
.comment-content {
  font-size: 14px;
  line-height: 1.4;
  margin-bottom: 8px;
}
.comment-meta {
  font-size: 11px;
  color: #888;
  display: flex;
  justify-content: space-between;
}
</style>