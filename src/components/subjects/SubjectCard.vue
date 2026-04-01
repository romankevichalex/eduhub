<template>
  <button class="subject-card" @click="$emit('click')">
    {{ name }}
  </button>
</template>

<script setup>
defineProps({
  name: String
})
defineEmits(['click'])
</script>

<style scoped>
.subject-card {
  background: var(--main-color-b);
  border: none;
  border-radius: 27px;
  padding: 12px 20px;
  margin: 8px;
  color: white;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.1s, box-shadow 0.2s;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  /* Автоматическая ширина под контент */
  display: inline-block;
  width: auto;
}
.subject-card:active {
  transform: translateY(2px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
</style>