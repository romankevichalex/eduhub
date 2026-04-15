<template>
  <div class="settings-page">
    <div class="top-bar-settings">
      <div class="top-bar-title">Настройки</div>
      <div class="top-bar-subtitle">Кафедра интеллектуальных систем</div>
    </div>

    <div class="settings-content">
      <div class="version-info">
        <p>Версия приложения: <strong>1.0.0</strong></p>
        <p class="copyright">© 2025 EduHub</p>
      </div>
    </div>

    <TabBar :activeTab="activeTab" @update:activeTab="handleTabChange" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import TabBar from '@/components/layout/TabBar.vue'

const router = useRouter()
const activeTab = ref('settings')

const handleTabChange = (tab) => {
  activeTab.value = tab
  if (tab === 'subjects') router.push('/subjects')
  else if (tab === 'settings') router.push('/settings')
  else if (tab === 'users') router.push('/admin/users')
}
</script>

<style scoped>
.settings-page {
  min-height: 100vh;
  background: white;
  display: flex;
  flex-direction: column;
  padding-bottom: 70px;
}
.top-bar-settings {
  background: var(--gradient);
  padding: 20px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.2);
}
.top-bar-title {
  font-size: 24px;
  font-weight: 600;
  color: white;
}
.top-bar-subtitle {
  font-size: 14px;
  color: rgba(255,255,255,0.8);
  margin-top: 4px;
}
.settings-content {
  flex: 1;
  padding: 24px 16px;
}
.version-info {
  background: #f8f9fa;
  border-radius: 27px;
  padding: 20px;
  text-align: center;
  color: #333;
}
.copyright {
  margin-top: 12px;
  font-size: 12px;
  color: #888;
}
</style>