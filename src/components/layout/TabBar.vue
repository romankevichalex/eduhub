<template>
  <div class="tab-bar">
    <button
      class="tab-btn"
      :class="{ active: activeTab === 'subjects' }"
      @click="setActive('subjects')"
    >
      <span class="tab-icon">📚</span>
    </button>
    <button
      class="tab-btn"
      :class="{ active: activeTab === 'settings' }"
      @click="setActive('settings')"
    >
      <span class="tab-icon">⚙️</span>
    </button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  activeTab: {
    type: String,
    default: 'subjects'
  }
})

const emit = defineEmits(['update:activeTab'])

const setActive = (tab) => {
  emit('update:activeTab', tab)
}
</script>

<style scoped>
.tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  background: white;
  border-top: 1px solid #eee;
  padding: 8px 0;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
}
.tab-btn {
  flex: 1;
  background: none;
  border: none;
  padding: 12px;
  border-radius: 27px;
  background: white;
  color: var(--main-color-b);
  transition: all 0.2s;
  cursor: pointer;
}
.tab-btn.active {
  background: linear-gradient(90deg, var(--main-color-b), var(--main-color-p));
  color: white;
}
.tab-icon {
  font-size: 24px;
}
</style>