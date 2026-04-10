<template>
  <div class="ai-chat">
    <div class="messages-container" ref="messagesContainer">
      <div v-if="chatStore.loading && !chatStore.messages.length" class="status">
        Загрузка истории...
      </div>
      <ChatMessage
        v-for="msg in chatStore.messages"
        :key="msg.id"
        :message="msg"
      />
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
        <svg width="24" height="24" viewBox="0 0 24 24">
          <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m5 12l-.604-5.437C4.223 5.007 5.825 3.864 7.24 4.535l11.944 5.658c1.525.722 1.525 2.892 0 3.614L7.24 19.466c-1.415.67-3.017-.472-2.844-2.028zm0 0h7" stroke-width="2"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { useChatStore } from '@/stores/chatStore'
import ChatMessage from './ChatMessage.vue'

const props = defineProps({
  subjectId: { type: Number, required: true }
})

const chatStore = useChatStore()
const newMessage = ref('')
const messagesContainer = ref(null)
const isWaiting = ref(false)

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
    // Дополнительный вызов для надёжности (как в рабочем CommentsPage)
    setTimeout(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }, 20)
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
  if (ok) {
    scrollToBottom()
  } else {
    alert(chatStore.error || 'Ошибка')
  }
}

onMounted(async () => {
  await chatStore.fetchHistory(props.subjectId)
  scrollToBottom()
})

// Watch с flush: 'post' для гарантии после обновления DOM
watch(() => chatStore.messages.length, () => scrollToBottom(), { flush: 'post' })
</script>

<style scoped>
.ai-chat {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;         /* как в CommentsPage */
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  box-sizing: border-box;
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

/* Анимация печати */
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