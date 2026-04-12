<template>
  <div class="subjects-page">
    <TopBar />

    <div class="subjects-container" v-if="!subjectsStore.loading">
      <div class="column">
        <SubjectCard
          v-for="subject in oddSubjects"
          :key="subject.id"
          :name="subject.name"
          @click="handleSubjectClick(subject)"
        />
      </div>
      <div class="column">
        <SubjectCard
          v-for="subject in evenSubjects"
          :key="subject.id"
          :name="subject.name"
          @click="handleSubjectClick(subject)"
        />
      </div>
    </div>
    <div v-else class="loading">Загрузка...</div>
    <div v-if="subjectsStore.error" class="error">{{ subjectsStore.error }}</div>

    <!-- Плавающие кнопки для администратора -->
    <div v-if="isAdmin" class="fab-container">
      <button v-if="editMode" class="fab fab-left" @click="openCreateModal">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 5v14M5 12h14" stroke="white" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
      <button class="fab fab-right" @click="toggleEditMode">
        <svg v-if="!editMode" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M17 3l4 4-7 7H10v-4l7-7z M4 20h16" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M18 6L6 18M6 6l12 12" stroke="white" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
    </div>

    <!-- Модальное окно для создания/редактирования -->
    <SubjectFormModal
      :isOpen="modalOpen"
      :mode="modalMode"
      :subjectData="selectedSubject"
      @close="closeModal"
      @save="handleSave"
      @delete="handleDelete"
    />
    <TabBar :activeTab="activeTab" @update:activeTab="handleTabChange" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSubjectsStore } from '@/stores/subjectsStore'
import { useAuthStore } from '@/stores/authStore'
import TopBar from '@/components/layout/TopBar.vue'
import TabBar from '@/components/layout/TabBar.vue'
import SubjectCard from '@/components/subjects/SubjectCard.vue'
import SubjectFormModal from '@/components/subjects/SubjectFormModal.vue'

const router = useRouter()
const subjectsStore = useSubjectsStore()
const authStore = useAuthStore()
const activeTab = ref('subjects')
const editMode = ref(false)
const modalOpen = ref(false)
const modalMode = ref('create') // 'create' или 'edit'
const selectedSubject = ref(null)

const isAdmin = computed(() => authStore.user?.role === 'admin')

const evenSubjects = computed(() => subjectsStore.subjects.filter((_, idx) => idx % 2 === 0))
const oddSubjects = computed(() => subjectsStore.subjects.filter((_, idx) => idx % 2 === 1))

const toggleEditMode = () => {
  editMode.value = !editMode.value
}

const handleSubjectClick = (subject) => {
  if (editMode.value) {
    // Открываем форму редактирования
    openEditModal(subject)
  } else {
    // Обычный переход на страницу предмета
    router.push({ path: `/subjects/${subject.id}`, query: { name: subject.name } })
  }
}

const openCreateModal = () => {
  modalMode.value = 'create'
  selectedSubject.value = null
  modalOpen.value = true
}

const handleTabChange = (tab) => {
  activeTab.value = tab
  if (tab === 'settings') {
    router.push('/settings')
  }
}

const openEditModal = async (subject) => {
  modalMode.value = 'edit'
  // Получаем полные данные предмета (на случай, если в списке не хватает полей)
  try {
    const fullSubject = await subjectsStore.fetchSubjectById(subject.id)
    selectedSubject.value = fullSubject
    modalOpen.value = true
  } catch (err) {
    alert('Не удалось загрузить данные предмета')
  }
}

const closeModal = () => {
  modalOpen.value = false
  selectedSubject.value = null
}

const handleSave = async (formData) => {
  try {
    if (modalMode.value === 'create') {
      await subjectsStore.createSubject(formData)
    } else if (modalMode.value === 'edit' && selectedSubject.value) {
      await subjectsStore.updateSubject(selectedSubject.value.id, formData)
    }
    // Обновляем список предметов
    await subjectsStore.fetchSubjects()
    closeModal()
  } catch (err) {
    alert(subjectsStore.error || 'Ошибка сохранения')
  }
}

const handleDelete = async () => {
  if (!selectedSubject.value) return
  try {
    await subjectsStore.deleteSubject(selectedSubject.value.id)
    await subjectsStore.fetchSubjects()
    closeModal()
  } catch (err) {
    alert(subjectsStore.error || 'Ошибка удаления')
  }
}

onMounted(() => {
  if (!authStore.user) {
    authStore.fetchMe()
  }
  if (authStore.user?.role === 'admin') {
    subjectsStore.fetchAllSubjects()
  } else {
    subjectsStore.fetchSubjects()
  }
})
</script>

<style scoped>
.subjects-page {
  min-height: 100vh;
  background: white;
  display: flex;
  flex-direction: column;
  padding-bottom: 70px;
}
.subjects-container {
  flex: 1;
  padding: 16px;
  display: flex;
  gap: 12px;
  align-items: flex-start;
}
.column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.loading, .error {
  text-align: center;
  margin-top: 40px;
  color: #666;
}
.error {
  color: red;
}

/* Плавающие кнопки */
.fab-container {
  position: fixed;
  bottom: 130px;  /* чуть выше таб-бара */
  right: 20px;
  left: 20px;
  pointer-events: none;
  z-index: 90;
}
.fab {
  position: absolute;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--main-color-b);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  transition: 0.2s;
  pointer-events: auto;
}
.fab:active {
  transform: scale(0.95);
}
.fab-right {
  right: 0;
}
.fab-left {
  left: 0;
}
</style>