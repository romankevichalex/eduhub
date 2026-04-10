<template>
  <div class="tab-bar">
    <button
      class="tab-btn"
      :class="{ active: activeTab === 'subjects' }"
      @click="setActive('subjects')"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        class="tab-icon"
      >
        <g fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M4 8c0-2.828 0-4.243.879-5.121C5.757 2 7.172 2 10 2h4c2.828 0 4.243 0 5.121.879C20 3.757 20 5.172 20 8v8c0 2.828 0 4.243-.879 5.121C18.243 22 16.828 22 14 22h-4c-2.828 0-4.243 0-5.121-.879C4 20.243 4 18.828 4 16z" />
          <path d="M19.898 16h-12c-.93 0-1.395 0-1.777.102A3 3 0 0 0 4 18.224" />
          <path stroke-linecap="round" d="M8 7h8m-8 3.5h5" />
        </g>
      </svg>
    </button>
    <div class="divider"></div>  
    <button
      class="tab-btn"
      :class="{ active: activeTab === 'settings' }"
      @click="setActive('settings')"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="32"
        height="32"
        viewBox="0 0 32 32"
        class="tab-icon"
      >
        <g fill="currentColor">
          <path d="M27 16.76v-1.53l1.92-1.68A2 2 0 0 0 29.3 11l-2.36-4a2 2 0 0 0-1.73-1a2 2 0 0 0-.64.1l-2.43.82a11 11 0 0 0-1.31-.75l-.51-2.52a2 2 0 0 0-2-1.61h-4.68a2 2 0 0 0-2 1.61l-.51 2.52a11.5 11.5 0 0 0-1.32.75l-2.38-.86A2 2 0 0 0 6.79 6a2 2 0 0 0-1.73 1L2.7 11a2 2 0 0 0 .41 2.51L5 15.24v1.53l-1.89 1.68A2 2 0 0 0 2.7 21l2.36 4a2 2 0 0 0 1.73 1a2 2 0 0 0 .64-.1l2.43-.82a11 11 0 0 0 1.31.75l.51 2.52a2 2 0 0 0 2 1.61h4.72a2 2 0 0 0 2-1.61l.51-2.52a11.5 11.5 0 0 0 1.32-.75l2.42.82a2 2 0 0 0 .64.1a2 2 0 0 0 1.73-1l2.28-4a2 2 0 0 0-.41-2.51ZM25.21 24l-3.43-1.16a8.9 8.9 0 0 1-2.71 1.57L18.36 28h-4.72l-.71-3.55a9.4 9.4 0 0 1-2.7-1.57L6.79 24l-2.36-4l2.72-2.4a8.9 8.9 0 0 1 0-3.13L4.43 12l2.36-4l3.43 1.16a8.9 8.9 0 0 1 2.71-1.57L13.64 4h4.72l.71 3.55a9.4 9.4 0 0 1 2.7 1.57L25.21 8l2.36 4l-2.72 2.4a8.9 8.9 0 0 1 0 3.13L27.57 20Z" />
          <path d="M16 22a6 6 0 1 1 6-6a5.94 5.94 0 0 1-6 6m0-10a3.91 3.91 0 0 0-4 4a3.91 3.91 0 0 0 4 4a3.91 3.91 0 0 0 4-4a3.91 3.91 0 0 0-4-4" />
        </g>
      </svg>
    </button>
  </div>
</template>

<script setup>

defineProps({
  activeTab: { type: String, default: 'subjects' }
})
const emit = defineEmits(['update:activeTab'])
const setActive = (tab) => emit('update:activeTab', tab)
</script>

<style scoped>
.tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: space-around;
  background: white;
  border-top: 2px solid var(--gray-2);   /* серая, более толстая граница */
  padding: 0;
  margin: 0;
}

.tab-btn {
  flex: 1;
  background: transparent;
  border: none;
  padding: 10px 0;
  cursor: pointer;
  transition: background 0.1s ease;
  border-radius: 0; 
  height: 100%; 
}

.tab-btn:active {
  background-color: var(--gray-3); 
}

.tab-icon {
  font-size: 26px;
  color: #8e8e93;
  transition: color 0.2s;
}

.tab-btn.active .tab-icon {
  color: var(--main-color-b);
  transform: scale(1.02);
}

.divider {
  width: 1px;
  height: 30px;
  background-color: var(--gray-3);
}
</style>