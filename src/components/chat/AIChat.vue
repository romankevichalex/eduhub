<template>
  <div class="ai-chat">
    <div class="messages-container" ref="messagesContainer">
      <div v-if="chatStore.loading && !chatStore.messages.length" class="status">
        Загрузка истории...
      </div>
      <div v-for="msg in chatStore.messages" :key="msg.id" class="message" :class="msg.role">
        <div class="message-content">{{ msg.content }}</div>
        <div class="message-time">{{ formatTime(msg.created_at) }}</div>
      </div>
      <div v-if="isWaiting" class="message assistant typing">
        <div class="message-content">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
      </div>
    </div>
    
    <div class="input-area">
      <textarea
        v-model="newMessage"
        @keydown.enter.prevent="send"
        placeholder="Напишите сообщение..."
        rows="2"
      ></textarea>
      <button @click="send" :disabled="!newMessage.trim() || chatStore.loading">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m5 12l-.604-5.437C4.223 5.007 5.825 3.864 7.24 4.535l11.944 5.658c1.525.722 1.525 2.892 0 3.614L7.24 19.466c-1.415.67-3.017-.472-2.844-2.028zm0 0h7" stroke-width="2"/></svg>
    </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { useChatStore } from '@/stores/chatStore'

const props = defineProps({
  subjectId: { type: Number, required: true }
})

const chatStore = useChatStore()
const newMessage = ref('')
const messagesContainer = ref(null)
const isWaiting = ref(false)

const formatTime = (iso) => {
  if (!iso) return ''
  return new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const send = async () => {
  if (!newMessage.value.trim() || chatStore.loading) return
  const msg = newMessage.value
  newMessage.value = ''
  isWaiting.value = true
  scrollToBottom()
  const ok = await chatStore.sendMessage(props.subjectId, msg)
  isWaiting.value = false
  if (ok) scrollToBottom()
  else alert(chatStore.error || 'Ошибка')
}

onMounted(() => {
  chatStore.fetchHistory(props.subjectId)
})

watch(() => chatStore.messages.length, () => scrollToBottom())
</script>

<style scoped>
.ai-chat {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  margin: 0;
  padding: 0;
  width: 100%;
  box-sizing: border-box;
}
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 12px; 
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  box-sizing: border-box;
}
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
.status {
  text-align: center;
  color: #666;
}
.input-area {
  display: flex;
  gap: 8px;
  padding: 12px; 
  border-top: 1px solid #eee;
  background: white;
  flex-shrink: 0;
  width: 100%;
  box-sizing: border-box;
}
.input-area textarea {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 27px;
  padding: 10px 12px;
  resize: none;
  font-family: inherit;
  font-size: 14px;
  width: 100%;
  box-sizing: border-box;
}
.input-area button {
  background: var(--main-color-b);
  color: white;
  border: none;
  border-radius: 27px;
  padding: 0 20px;
  cursor: pointer;
  white-space: nowrap;
}
.input-area button:disabled {
  opacity: 0.6;
}
.typing .message-content {
  display: flex;
  gap: 4px;
  align-items: center;
  padding: 8px 12px;
}

.dot {
  width: 8px;
  height: 8px;
  background-color: #888;
  border-radius: 50%;
  display: inline-block;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
</style>