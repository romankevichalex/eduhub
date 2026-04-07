import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../pages/LoginPage.vue'
import SubjectsPage from '../pages/SubjectsPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import { useAuthStore } from '@/stores/authStore'
import SettingsPage from '../pages/SettingsPage.vue'
import SubjectPage from '@/pages/SubjectPage.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginPage },
  { path: '/subjects', component: SubjectsPage, meta: { requiresAuth: true } },
   { path: '/subjects/:id', component: SubjectPage, meta: { requiresAuth: true }, props: true },
  { path: '/register', component: RegisterPage, },
  { path: '/settings', component: SettingsPage, meta: { requiresAuth: true } },
  // ... другие
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router