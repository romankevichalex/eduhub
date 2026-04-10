<template>
  <button class="subject-card" @click="$emit('click')">
    <span class="subject-name">{{ name }}</span>
  </button>
</template>

<script setup>
defineProps({ name: String });
defineEmits(['click']);
</script>

<style scoped>
.subject-card {
  background: var(--main-color-b);
  border: none;
  border-radius: 27px;
  padding: 15px 15px 15px 15px;
  color: white;
  font-size: 17px;
  font-weight: 600;
  text-align: center;
  cursor: pointer;
  transition: transform 0.1s, box-shadow 0.2s;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  width: 100%;           
  min-height: 30px;
  display: block;
  align-items: center;
  justify-content: center;
}

.subject-card:active {
  transform: translateY(2px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.subject-name {
  word-break: normal;
  line-height: 1.2;
}
</style>