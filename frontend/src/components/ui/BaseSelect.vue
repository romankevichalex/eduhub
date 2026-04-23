<template>
  <div class="base-select" @click="toggle" ref="selectRef">
    <div class="selected-value">
      {{ selectedLabel || placeholder }}
    </div>
    <div class="arrow" :class="{ open: isOpen }">▼</div>
    <div v-if="isOpen" class="dropdown">
      <div
        v-for="option in options"
        :key="option.value"
        class="option"
        :class="{ selected: option.value === modelValue }"
        @click.stop="selectOption(option)"
      >
        {{ option.label }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  options: { type: Array, required: true }, // [{ value, label }]
  placeholder: { type: String, default: 'Выберите...' }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const selectRef = ref(null)

const selectedLabel = computed(() => {
  const found = props.options.find(opt => opt.value === props.modelValue)
  return found ? found.label : ''
})

const toggle = () => {
  isOpen.value = !isOpen.value
}

const selectOption = (option) => {
  emit('update:modelValue', option.value)
  isOpen.value = false
}

const handleClickOutside = (event) => {
  if (selectRef.value && !selectRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.base-select {
  position: relative;
  flex: 1;
  padding: 12px 16px;
  border-radius: 27px;
  border: 1px solid #ddd;
  background: white;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  user-select: none;
}

.selected-value {
  color: #333;
}

.arrow {
  font-size: 12px;
  transition: transform 0.2s;
  color: #666;
}
.arrow.open {
  transform: rotate(180deg);
}

.dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: white;
  border-radius: 20px;
  border: 1px solid #ddd;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  z-index: 100;
  max-height: 200px;
  overflow-y: auto;
}

.option {
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.1s;
}
.option:hover {
  background: #f0f0f0;
}
.option.selected {
  background: var(--main-color-b);
  color: white;
}
</style>