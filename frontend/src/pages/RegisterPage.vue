<template>
  <div class="register-page">
    <div class="register-card">
      <h2 class="register-title">Регистрация</h2>

      <form @submit.prevent="handleRegister">
        <BaseInput
          v-model="form.email"
          type="email"
          placeholder="Электронная почта"
          class="input-field"
        />
        <BaseInput
          v-model="form.firstName"
          placeholder="Имя"
          class="input-field"
        />
        <BaseInput
          v-model="form.lastName"
          placeholder="Фамилия"
          class="input-field"
        />
        <BaseInput
          v-model="form.patronymic"
          placeholder="Отчество"
          class="input-field"
        />
        <BaseInput
          v-model="form.password"
          type="password"
          placeholder="Пароль"
          class="input-field"
        />
        <BaseInput
          v-model="passwordConfirm"
          type="password"
          placeholder="Повторите пароль"
          class="input-field"
        />

        <div class="role-selector">
          <span class="role-label">Роль</span>
          <div class="role-buttons">
            <button
              type="button"
              class="role-btn"
              :class="{ active: form.role === 'student' }"
              @click="form.role = 'student'"
            >
              Студент
            </button>
            <button
              type="button"
              class="role-btn"
              :class="{ active: form.role === 'teacher' }"
              @click="form.role = 'teacher'"
            >
              Преподаватель
            </button>
          </div>
        </div>

        <BaseButton full-width :disabled="loading" @click="handleRegister">
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </BaseButton>

        <div v-if="error" class="error-message">{{ error }}</div>

        <div class="login-row">
          <span class="login-text">Уже есть аккаунт?</span>
          <router-link to="/login" class="login-link">
            Войдите
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const form = reactive({
  email: '',
  firstName: '',
  lastName: '',
  patronymic: '',   // новое поле
  password: '',
  role: 'student', // по умолчанию
})
const passwordConfirm = ref('')
const loading = ref(false)
const error = ref('')
const router = useRouter()
const authStore = useAuthStore()

const handleRegister = async () => {
  // Валидация
  if (!form.email || !form.firstName || !form.lastName || !form.password || !passwordConfirm.value || !form.patronymic) {
    error.value = 'Заполните все поля'
    return
  }
  if (form.password !== passwordConfirm.value) {
    error.value = 'Пароли не совпадают'
    return
  }
  if(form.firstName.length > 60 || form.middle_name.length > 60 || form.lastName.length > 60 || form.email.length > 256) {
    error.value = 'Слишком длинное имя, фамилия, отчество или почта!'
    return
  }
  if (!form.role) {
    error.value = 'Выберите роль'
    return
  }

  loading.value = true
  error.value = ''

  const registerData = { //преобразования для бэка
    email: form.email,
    first_name: form.firstName,
    last_name: form.lastName,
    middle_name: form.patronymic,
    password: form.password,
    role: form.role,
  }

  const success = await authStore.register(registerData)
  loading.value = false
  if (success) {
    // После успешной регистрации можно автоматически войти или перенаправить на страницу входа
    // Сейчас перенаправим на логин с сообщением
    router.push({ path: '/login', query: { registered: 'true' } })
  } else {
    error.value = authStore.error || 'Ошибка регистрации'
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: var(--gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
}

.register-card {
  background: white;
  border-radius: 27px;
  padding: 32px 24px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

.register-title {
  text-align: center;
  margin: 0 0 24px 0;
  font-size: 28px;
  font-weight: 600;
  color: black;
}

.input-field {
  margin-bottom: 20px;
}

.role-selector {
  margin-bottom: 24px;
}

.role-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.role-buttons {
  display: flex;
  gap: 12px;
}

.role-btn {
  flex: 1;
  padding: 12px;
  border-radius: 27px;
  border: 1px solid var(--main-color-b);
  background: white;
  color: var(--main-color-b);
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.role-btn.active {
  background: linear-gradient(90deg, var(--main-color-b), var(--main-color-p));
  border: none;
  color: white;
}

.error-message {
  margin-top: 12px;
  color: red;
  font-size: 14px;
  text-align: center;
}

.login-row {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
}

.login-text {
  color: gray;
  margin-right: 4px;
}

.login-link {
  color: var(--main-color-b);
  opacity: 0.6;
  text-decoration: none;
}

.login-link:hover {
  text-decoration: underline;
}
</style>