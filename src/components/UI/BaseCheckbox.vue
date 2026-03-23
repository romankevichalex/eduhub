<template>
  <label class="checkbox-label">
    <input
      type="checkbox"
      :checked="modelValue"
      @change="$emit('update:modelValue', $event.target.checked)"
      class="checkbox-input"
    />
    <span class="checkbox-text"><slot /></span>
  </label>
</template>

<script setup>
defineProps({
  modelValue: { type: Boolean, default: false }
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.checkbox-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
}

.checkbox-input {
  width: 18px;
  height: 18px;
  accent-color: var(--main-color-b);
  margin: 0;
}

.checkbox-text {
  font-size: 14px;
  color: var(--main-color-b);
}
</style>