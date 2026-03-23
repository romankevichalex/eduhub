import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../pages/LoginPage.vue'
// пока создадим заглушки для остальных страниц
import SubjectsPage from '../pages/SubjectsPage.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginPage },
  { path: '/subjects', component: SubjectsPage },
  // ... другие
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router