<template>
  <div class="comment-message" :class="{ 'my-comment': isMyComment }">
    <div class="comment-content">{{ comment.content }}</div>
    <div class="comment-meta">
      <span v-if="!isMyComment" class="comment-author">
        {{ comment.last_name }} {{ comment.first_name }}
      </span>
      <span class="comment-time">{{ formattedTime }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { formatMessageTime } from '@/services/dateFormatter'

const props = defineProps({
  comment: Object
})

const authStore = useAuthStore()

// Определяем, принадлежит ли комментарий текущему пользователю
const isMyComment = computed(() => {
  return authStore.user?.id === props.comment.author_id
})

// Возвращаем полный формат даты и времени, как было изначально
const formattedTime = computed(() => {
  return formatMessageTime(props.comment.created_at, {showDate: true})
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

/* Стили для своих комментариев — как у .message.user в AI-чате */
.comment-message.my-comment {
  align-self: flex-end;
  background: var(--main-color-b);
  color: white;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 4px;
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

/* Для своих комментариев время справа, имя скрыто */
.comment-message.my-comment .comment-meta {
  justify-content: flex-end;
  color: rgba(255, 255, 255, 0.7);
}

.comment-author {
  font-weight: 500;
}
</style>