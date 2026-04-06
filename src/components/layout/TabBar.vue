<template>
  <div class="tab-bar">
    <button
      class="tab-btn"
      :class="{ active: activeTab === 'subjects' }"
      @click="setActive('subjects')"
    >
    </button>
    <button
      class="tab-btn"
      :class="{ active: activeTab === 'settings' }"
      @click="setActive('settings')"
    >
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
  background: white;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  border-top: 1px solid #f0f0f0;
  padding: 8px 0;
}
.tab-btn {
  flex: 1;
  background: transparent;
  border: none;
  padding: 10px 0;
  cursor: pointer;
  transition: all 0.2s;
}
.tab-icon {
  font-size: 26px;
  color: #8e8e93; 
}
.tab-btn.active .tab-icon {
  color: var(--main-color-b); 
  text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.tab-btn.active .tab-icon {
  transform: scale(1.05);
}
</style>