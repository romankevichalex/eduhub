<template>
  <div class="subjects-page">
    <TopBar />

    <div class="subjects-container">
      <SubjectCard
        v-for="subject in subjects"
        :key="subject.id"
        :name="subject.name"
        @click="goToSubject(subject.id)"
      />
    </div>

    <TabBar :activeTab="activeTab" @update:activeTab="handleTabChange" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import TopBar from '@/components/layout/TopBar.vue'
import TabBar from '@/components/layout/TabBar.vue'
import SubjectCard from '@/components/subjects/SubjectCard.vue'

const router = useRouter()
const activeTab = ref('subjects')

// Мок-данные предметов – потом заменим на получение из API
const subjects = ref([
  { id: 1, name: 'Математика' },
  { id: 2, name: 'Физика' },
  { id: 3, name: 'Программирование' },
  { id: 4, name: 'Базы данных' },
  { id: 5, name: 'Английский язык' },
  { id: 6, name: 'История' }
])

const goToSubject = (id) => {
  router.push(`/subjects/${id}`)
}

const handleTabChange = (tab) => {
  activeTab.value = tab
  if (tab === 'settings') {
    router.push('/settings')
  }
}
</script>

<style scoped>
.subjects-page {
  min-height: 100vh;
  background: white;
  display: flex;
  flex-direction: column;
  padding-bottom: 70px; /* чтобы контент не перекрывался таб-баром */
}

.subjects-container {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  gap: 8px;
}
</style>