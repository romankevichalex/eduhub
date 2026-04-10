<template>
  <button class="base-button" :class="{ 'full-width': fullWidth }" @click="$emit('click')">
    <slot />
  </button>
</template>

<script setup>
defineProps({
  fullWidth: { type: Boolean, default: false }
})

defineEmits(['click'])
</script>

<style scoped>
.base-button {
  background: linear-gradient(90deg, var(--main-color-b), var(--main-color-p));
  border: none;
  border-radius: 27px;
  padding: 14px 20px;
  font-size: 16px;
  font-weight: 500;
  color: white;
  cursor: pointer;
  transition: opacity 0.2s;
  text-align: center;
}

.base-button.full-width {
  width: 100%;
}

.base-button:hover {
  opacity: 0.9;
}
</style>