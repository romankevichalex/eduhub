<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <h3>{{ title }}</h3>
      <form @submit.prevent="save">
        <div class="field">
          <label>Название *</label>
          <input v-model="form.name" type="text" placeholder="Введите название" required />
        </div>
        <div class="field">
          <label>Код</label>
          <input v-model="form.code" type="text" placeholder="Введите код" />
        </div>
        <div class="field">
          <label>Описание</label>
          <textarea v-model="form.description" rows="3" placeholder="Введите описание"></textarea>
        </div>
        <div class="actions">
          <button type="button" class="cancel" @click="close">Отмена</button>
          <div v-if="mode === 'edit'" class="delete-group">
            <button
              v-if="!showDeleteConfirm"
              type="button"
              class="delete"
              @click="showDeleteConfirm = true"
            >
              Удалить
            </button>
            <button
              v-else
              type="button"
              class="confirm-delete"
              @click="deleteSubject"
            >
              Подтвердить
            </button>
          </div>
          <button type="submit" class="save">Сохранить</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch, computed, ref } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  mode: { type: String, default: 'create' },
  subjectData: { type: Object, default: null },
})

const emit = defineEmits(['close', 'save', 'delete'])

const form = reactive({
  name: '',
  code: '',
  description: '',
})

const showDeleteConfirm = ref(false)

watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal) {
      if (props.mode === 'edit' && props.subjectData) {
        form.name = props.subjectData.name || ''
        form.code = props.subjectData.code || ''
        form.description = props.subjectData.description || ''
      } else if (props.mode === 'create') {
        form.name = ''
        form.code = ''
        form.description = ''
      }
      showDeleteConfirm.value = false
    }
  },
  { immediate: true }
)

const title = computed(() =>
  props.mode === 'create' ? 'Создание предмета' : 'Редактирование предмета'
)

const save = () => {
  if (!form.name.trim()) {
    alert('Название обязательно')
    return
  }
  emit('save', { ...form })
}

const close = () => {
  showDeleteConfirm.value = false
  emit('close')
}

const deleteSubject = () => {
  emit('delete')
  showDeleteConfirm.value = false
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background: white;
  border-radius: 27px;
  padding: 24px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.modal-content h3 {
  margin: 0 0 16px 0;
  text-align: center;
}
.field {
  margin-bottom: 16px;
}
.field label {
  display: block;
  font-size: 14px;
  margin-bottom: 6px;
  color: #333;
}
.field input,
.field textarea {
  width: 100%;
  border: 1px solid #ddd;
  border-radius: 27px;
  padding: 10px 12px;
  font-size: 14px;
  box-sizing: border-box;
}
.actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
  flex-wrap: wrap;
}
.actions button {
  padding: 8px 16px;
  border-radius: 27px;
  border: none;
  cursor: pointer;
  font-size: 14px;
}
.cancel {
  background: #f0f0f0;
  color: #333;
}
.delete {
  background: #ff4d4d;
  color: white;
}
.save {
  background: var(--main-color-b);
  color: white;
}
.delete-group {
  display: flex;
  gap: 8px;
}
.confirm-delete {
  background: #ff4d4d;
  color: white;
}
</style>