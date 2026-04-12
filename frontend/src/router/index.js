import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../pages/LoginPage.vue'
import SubjectsPage from '../pages/SubjectsPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import { useAuthStore } from '@/stores/authStore'
import SettingsPage from '../pages/SettingsPage.vue'
import SubjectPage from '@/pages/SubjectPage.vue'
import CommentsPage from '../pages/CommentsPage.vue'
import AdminUsersPage from '@/pages/AdminUsersPage.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginPage },
  { path: '/subjects', component: SubjectsPage, meta: { requiresAuth: true } },
  { path: '/subjects/:id', component: SubjectPage, meta: { requiresAuth: true }, props: true },
  { path: '/subjects/:id/comments/:postId', component: CommentsPage, meta: { requiresAuth: true } },
  { path: '/register', component: RegisterPage, },
  { path: '/settings', component: SettingsPage, meta: { requiresAuth: true } },
  { path: '/admin/users', component: AdminUsersPage, meta: { requiresAuth: true } },
  // ... другие
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.path === '/') {
    if (authStore.isAuthenticated) {
      next('/subjects')
    } else {
      next('/login')
    }
    return
  }
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
  if (to.path.startsWith('/admin') && authStore.user?.role !== 'admin') {
    next('/subjects')
  }
})

export default router