<template>
  <div class="subjects-page">
    <TopBar />

    <div class="subjects-container" v-if="!subjectsStore.loading">
      <div class="column">
        <SubjectCard
          v-for="subject in oddSubjects"
          :key="subject.id"
          :name="subject.name"
          @click="goToSubject(subject.id, subject.name)"
        />
      </div>
      
      <div class="column">
        <SubjectCard
          v-for="subject in evenSubjects"
          :key="subject.id"
          :name="subject.name"
          @click="goToSubject(subject.id, subject.name)"
        />
      </div>
    </div>
    <div v-else class="loading">Загрузка...</div>
    <div v-if="subjectsStore.error" class="error">{{ subjectsStore.error }}</div>

    <TabBar :activeTab="activeTab" @update:activeTab="handleTabChange" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useSubjectsStore } from '@/stores/subjectsStore'
import TopBar from '@/components/layout/TopBar.vue'
import TabBar from '@/components/layout/TabBar.vue'
import SubjectCard from '@/components/subjects/SubjectCard.vue'

const router = useRouter()
const activeTab = ref('subjects')
const subjectsStore = useSubjectsStore()

const evenSubjects = computed(() => subjectsStore.subjects.filter((_, idx) => idx % 2 === 0))
const oddSubjects = computed(() => subjectsStore.subjects.filter((_, idx) => idx % 2 === 1))

const goToSubject = (id, name) => {
  router.push({ path: `/subjects/${id}`, query: { name } })
}

const handleTabChange = (tab) => {
  activeTab.value = tab
  if (tab === 'settings') {
    router.push('/settings')
  }
}

onMounted(() => {
  subjectsStore.fetchSubjects()
})
</script>

<style scoped>

.subjects-page {
  min-height: 100vh;
  background: white;
  display: bock;
  flex-direction: column;
  padding-bottom: 70px;
}
.column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.subjects-container {
  flex: 1;
  padding: 16px;
  display: flex;
  gap: 12px;
  align-items: flex-start;
}
.loading, .error {
  text-align: center;
  margin-top: 40px;
  color: #666;
}
.error {
  color: red;
}
</style>
