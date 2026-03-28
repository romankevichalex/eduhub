import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../pages/LoginPage.vue'
import SubjectsPage from '../pages/SubjectsPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginPage },
  { path: '/subjects', component: SubjectsPage },
  { path: '/register', component: RegisterPage },
  // ... другие
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router