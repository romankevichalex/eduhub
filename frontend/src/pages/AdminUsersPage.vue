<template>
  <div class="users-page">
    <div class="users-header">
      <h1 class="users-title">Управление пользователями</h1>
    </div>

    <!-- Фильтры -->
    <div class="filters">
      <BaseSelect
        v-model="filters.role"
        :options="roleOptions"
        placeholder="Все роли"
      />
      <BaseSelect
        v-model="filters.verified"
        :options="verifiedOptions"
        placeholder="Все статусы"
      />
    </div>

    <div class="users-list" v-if="!usersStore.loading">
      <div
        v-for="user in filteredUsers"
        :key="user.id"
        class="user-card"
      >
        <div class="user-info">
          <div class="user-name">{{ user.last_name }} {{ user.first_name }} {{ user.middle_name || '' }}</div>
          <div class="user-email">{{ user.email }}</div>
          <div class="user-meta">
            <span class="user-role" :class="user.role">{{ getRoleName(user.role) }}</span>
            <span class="user-verified" :class="{ verified: user.is_verified }">
              {{ user.is_verified ? 'Верифицирован' : 'Не верифицирован' }}
            </span>
          </div>
        </div>
        <div class="user-actions">
          <button
            v-if="!user.is_verified"
            class="verify-btn"
            @click="handleVerify(user.id)"
            :disabled="verifying === user.id"
          >
            {{ verifying === user.id ? '...' : 'Верифицировать' }}
          </button>
          <button class="delete-btn" @click="handleDelete(user.id)">Удалить</button>
        </div>
      </div>
      <div v-if="filteredUsers.length === 0" class="empty">Пользователи не найдены</div>
    </div>
    <div v-else class="loading">Загрузка...</div>

    <TabBar :activeTab="activeTab" @update:activeTab="handleTabChange" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUsersStore } from '@/stores/usersStore'
import TabBar from '@/components/layout/TabBar.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'

const router = useRouter()
const usersStore = useUsersStore()
const activeTab = ref('users')
const verifying = ref(null)

const filters = ref({
  role: '',
  verified: ''
})

const roleOptions = [
  { value: '', label: 'Все роли' },
  { value: 'student', label: 'Студент' },
  { value: 'teacher', label: 'Преподаватель' },
  { value: 'admin', label: 'Администратор' }
]

const verifiedOptions = [
  { value: '', label: 'Все статусы' },
  { value: 'verified', label: 'Верифицированы' },
  { value: 'not_verified', label: 'Не верифицированы' }
]

const filteredUsers = computed(() => {
  let result = [...usersStore.users]
  if (filters.value.role) {
    result = result.filter(u => u.role === filters.value.role)
  }
  if (filters.value.verified === 'verified') {
    result = result.filter(u => u.is_verified === true)
  } else if (filters.value.verified === 'not_verified') {
    result = result.filter(u => u.is_verified === false)
  }
  return result
})

const getRoleName = (role) => {
  const roles = { student: 'Студент', teacher: 'Преподаватель', admin: 'Администратор' }
  return roles[role] || role
}

const handleVerify = async (userId) => {
  verifying.value = userId
  const ok = await usersStore.verifyUser(userId)
  verifying.value = null
  if (!ok) alert(usersStore.error || 'Ошибка верификации')
}

const handleDelete = (userId) => {
  usersStore.deleteUser(userId)
}

const handleTabChange = (tab) => {
  activeTab.value = tab
  if (tab === 'subjects') router.push('/subjects')
  else if (tab === 'settings') router.push('/settings')
}

onMounted(() => {
  usersStore.fetchUsers()
})
</script>

<style scoped>
.users-page {
  min-height: 100vh;
  background: white;
  display: flex;
  flex-direction: column;
  padding-bottom: 70px;
}

.users-header {
  background: var(--gradient);
  padding: 20px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.2);
}

.users-title {
  color: white;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.filters {
  padding: 16px;
  display: flex;
  gap: 12px;
  background: white;
  border-bottom: 1px solid #eee;
}

.filters select {
  flex: 1;
  padding: 12px 16px;
  max-width: 100%;
  border-radius: 27px;
  border: 1px solid #ddd;
  background: white;
  font-size: 14px;
  font-family: inherit;
  color: #333;
  appearance: none;         
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 16px center;
  background-size: 16px;
  cursor: pointer;
}

/* Стиль для фокуса */
.filters select:focus {
  outline: none;
  border-color: var(--main-color-b);
  box-shadow: 0 0 0 2px rgba(var(--main-color-b-rgb), 0.2);
}

@media (max-width: 480px) {
  .filters {
    flex-direction: column;
  }
}

.users-list {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.user-card {
  background: var(--gray-1);
  border-radius: 27px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  max-width: 100%;
  margin-bottom: 4px;
}

.user-email {
  font-size: 14px;
  color: #555;
  margin-bottom: 6px;
  max-width: 100%;
}

.user-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
}

.user-role {
  background: #e9ecef;
  padding: 2px 8px;
  border-radius: 27px;
}
.user-role.student { background: #cfe2ff; color: #084298; }
.user-role.teacher { background: #d1e7dd; color: #0f5132; }
.user-role.admin { background: #f8d7da; color: #842029; }

.user-verified {
  padding: 2px 8px;
  border-radius: 27px;
  background: #fff3cd;
  color: #856404;
}
.user-verified.verified {
  background: #d1e7dd;
  color: #0f5132;
}

.user-actions {
  display: flex;
  gap: 8px;
}

.verify-btn, .delete-btn {
  padding: 8px 16px;
  border-radius: 27px;
  border: none;
  font-size: 14px;
  cursor: pointer;
}
.verify-btn {
  background: var(--main-color-b);
  color: white;
}
.delete-btn {
  background: #ff4d4d;
  color: white;
}
.loading, .empty {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>