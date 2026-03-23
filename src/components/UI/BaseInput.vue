<template>
  <input
    :type="type"
    :value="modelValue"
    :placeholder="placeholder"
    @input="$emit('update:modelValue', $event.target.value)"
    class="base-input"
  />
</template>

<script setup>
defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  type: { type: String, default: 'text' }
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.base-input {
  width: 100%;
  padding: 14px 16px;
  border-radius: 27px;
  border: 1px solid var(--gray-2);
  background: var(--gray-1);
  font-size: 16px;
  color: var(--gray-3);
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.base-input:focus {
  outline: none;
  border-color: var(--main-color-b);
}
</style>