<template>
  <div class="message" :class="message.role">
    <div class="message-content">{{ message.content }}</div>
    <div class="message-time">{{ formattedTime }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { formatMessageTime } from '@/services/dateFormatter'

const props = defineProps({
  message: { type: Object, required: true }
})

const formattedTime = computed(() => {
  return formatMessageTime(props.message.created_at, {showDate: true})
})
</script>

<style scoped>
.message {
  max-width: 85%;
  padding: 10px 14px;
  border-radius: 20px;
  word-wrap: break-word;
}
.message.user {
  align-self: flex-end;
  background: var(--main-color-b);
  color: white;
  border-bottom-right-radius: 4px;
}
.message.user .message-time {
  text-align: right;
}
.message.assistant {
  align-self: flex-start;
  background: #f0f0f0;
  color: #1a1a1a;
  border-bottom-left-radius: 4px;
}
.message-time {
  font-size: 10px;
  margin-top: 4px;
  opacity: 0.7;
}
</style>