<template>
  <div class="login-page">
    <div class="login-card">
      <h2 class="login-title">Вход</h2>

      <form @submit.prevent="handleLogin">
        <BaseInput
          v-model="email"
          type="email"
          placeholder="Электронная почта"
          class="input-field"
        />
        <BaseInput
          v-model="password"
          type="password"
          placeholder="Пароль"
          class="input-field"
        />

        <div class="options-row">
          <BaseCheckbox v-model="autoLogin">Автовход</BaseCheckbox>
          <router-link to="/forgot-password" class="forgot-link">
            Забыли пароль?
          </router-link>
        </div>

        <BaseButton full-width :disabled="loading" @click="handleLogin">
          {{ loading ? 'Вход...' : 'Войти' }}
        </BaseButton>

        <div v-if="error" class="error-message">{{ error }}</div>

        <div class="register-row">
          <span class="register-text">Нет аккаунта?</span>
          <router-link to="/register" class="register-link">
            Зарегистрируйтесь
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseCheckbox from '@/components/ui/BaseCheckbox.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const email = ref('')
const password = ref('')
const autoLogin = ref(false)
const loading = ref(false)
const error = ref('')
const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  const success = await authStore.login(email.value, password.value, autoLogin.value)
  loading.value = false
  if (success) {
    router.push('/subjects')
  } else {
    error.value = authStore.error || 'Неверный email или пароль'
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: var(--gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
}
.error-message {
  margin-top: 12px;
  color: red;
  font-size: 14px;
  text-align: center;
}
.login-card {
  background: white;
  border-radius: 27px;
  padding: 32px 24px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

.login-title {
  text-align: center;
  margin: 24px 0 36px 0;
  font-size: 28px;
  font-weight: 600;
  color: black;
}

.input-field {
  margin-bottom: 20px;
}

.options-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
}

.forgot-link {
  font-size: 14px;
  color: var(--main-color-b);
  opacity: 0.6;
  text-decoration: none;
}

.forgot-link:hover {
  text-decoration: underline;
}

.register-row {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
}

.register-text {
  color: gray;
  margin-right: 4px;
}

.register-link {
  color: var(--main-color-b);
  opacity: 0.6;
  text-decoration: none;
}

.register-link:hover {
  text-decoration: underline;
}
</style>