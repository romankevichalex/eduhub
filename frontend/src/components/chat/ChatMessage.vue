<template>
  <div class="message" :class="message.role">
    <div class="message-content">{{ message.content }}</div>
    <div class="message-time">{{ formatTime(message.created_at) }}</div>
  </div>
</template>

<script setup>
defineProps({
  message: { type: Object, required: true }
})

const formatTime = (iso) => {
  if (!iso) return ''
  return new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
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
.message.assistant {
  align-self: flex-start;
  background: #f0f0f0;
  color: #333;
  border-bottom-left-radius: 4px;
}
.message-time {
  font-size: 10px;
  margin-top: 4px;
  opacity: 0.7;
}
</style>