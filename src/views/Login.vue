<template>
  <section class="login-shell">
    <div class="login-card">
      <div class="login-image-wrap">
        <img class="login-image" :src="cacaoImage" alt="Cacao beans" />
      </div>

      <div class="login-copy">
        <p class="eyebrow">Welcome back</p>
      </div>

      <form class="login-form" @submit.prevent="login">
        <label class="field">
          <span class="field-label">Email</span>
          <div class="input-group">
            <span class="icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false">
                <path
                  d="M4 6h16a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2Zm0 2v.2l8 5.34 8-5.34V8l-8 5.33L4 8Z"
                />
              </svg>
            </span>
            <input
              v-model.trim="form.email"
              type="email"
              name="email"
              placeholder="name@example.com"
              autocomplete="email"
              required
            >
          </div>
        </label>

        <label class="field">
          <span class="field-label">Password</span>
          <div class="input-group">
            <span class="icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false">
                <path
                  d="M17 8h-1V6a4 4 0 0 0-8 0v2H7a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2Zm-6 7.73V17a1 1 0 0 0 2 0v-1.27a2 2 0 1 0-2 0ZM10 8V6a2 2 0 0 1 4 0v2Z"
                />
              </svg>
            </span>
            <input
              v-model="form.password"
              type="password"
              name="password"
              placeholder="Enter password"
              autocomplete="current-password"
              required
            >
          </div>
        </label>

        <p v-if="error" class="message error">{{ error }}</p>
        <p v-if="successMessage" class="message success">{{ successMessage }}</p>

        <button class="login-button" type="submit">Login</button>
      </form>

      <p class="switch-copy">
        Need an account?
        <button class="link-button" type="button" @click="emit('switch-auth', 'Register')">
          Register
        </button>
      </p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { fetchCurrentUser, loginUser, toFrontendAuthUser } from '../services/auth'

const cacaoImage = new URL('../../cacao (2).png', import.meta.url).href

type LoginForm = {
  email: string
  password: string
}

const emit = defineEmits<{
  'login-success': [user: { fullName: string; email: string; role: 'Admin' | 'Viewer' }]
  'switch-auth': [screen: 'Login' | 'Register']
}>()

const form = ref<LoginForm>({
  email: '',
  password: ''
})

const error = ref('')
const successMessage = ref('')

const login = async () => {
  error.value = ''
  successMessage.value = ''

  try {
    const tokens = await loginUser({
      email: form.value.email,
      password: form.value.password
    })
    const currentUser = await fetchCurrentUser(tokens.access_token)
    const frontendUser = toFrontendAuthUser(currentUser)

    localStorage.setItem('accessToken', tokens.access_token)
    localStorage.setItem('refreshToken', tokens.refresh_token)
    successMessage.value = `Welcome back, ${frontendUser.fullName}.`
    emit('login-success', frontendUser)
    form.value = { email: '', password: '' }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Invalid email or password.'
  }
}
</script>

<style scoped>
:global(body) {
  font-family: 'Inter', 'Poppins', 'Roboto', sans-serif;
}

.login-shell {
  min-height: calc(100vh - 152px);
  display: grid;
  place-items: center;
  padding: 32px 16px;
  background:
    radial-gradient(circle at top left, #ffe3ec 0, transparent 28%),
    radial-gradient(circle at bottom right, #dff7f2 0, transparent 32%),
    #fffdfd;
}

.login-card {
  width: min(100%, 460px);
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid #f5dbe5;
  border-radius: 28px;
  overflow: hidden;
  box-shadow: 0 28px 70px rgba(36, 48, 66, 0.12);
  backdrop-filter: blur(10px);
}

.login-image-wrap {
  position: relative;
  background:
    linear-gradient(180deg, rgba(255, 234, 239, 0.86), rgba(223, 247, 242, 0.76)),
    #fff7f8;
  padding: 20px;
}

.login-image {
  display: block;
  width: 100%;
  height: 300px;
  object-fit: cover;
  object-position: center center;
  border-radius: 22px;
  background: #fff8f2;
}

.login-copy {
  padding: 18px 28px 6px;
  display: flex;
  justify-content: center;
  margin-bottom: 18px;
}

.eyebrow {
  margin: 0;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #d46d8a;
  text-align: center;
}

.login-form {
  display: grid;
  gap: 16px;
  padding: 0 28px;
}

.field {
  display: grid;
  gap: 8px;
}

.field-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #435066;
}

.input-group {
  position: relative;
}

.icon {
  position: absolute;
  top: 50%;
  left: 16px;
  width: 20px;
  height: 20px;
  color: #7b88a0;
  transform: translateY(-50%);
}

.icon svg {
  width: 100%;
  height: 100%;
  display: block;
  fill: currentColor;
}

input {
  width: 100%;
  min-height: 52px;
  border: 1px solid #e6dce2;
  border-radius: 16px;
  padding: 0 16px 0 48px;
  background: #fff;
  font-size: 1rem;
  color: #243042;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

input::placeholder {
  color: #9aa6b6;
}

input:focus {
  border-color: #d9a6b8;
  box-shadow: 0 0 0 4px rgba(233, 189, 204, 0.35);
}

.message {
  margin: 0;
  border-radius: 14px;
  padding: 12px 14px;
  font-size: 0.95rem;
}

.error {
  background: #fff1f3;
  color: #b33f5a;
}

.success {
  background: #edf9f5;
  color: #2b7a62;
}

.login-button {
  min-height: 52px;
  border: 0;
  border-radius: 16px;
  background: linear-gradient(135deg, #f3a6ba, #9fd9cc);
  color: #1f2937;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.login-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 30px rgba(159, 217, 204, 0.28);
}

.login-button:active {
  transform: translateY(0);
}

.switch-copy {
  margin: 18px 0 0;
  padding: 0 28px 28px;
  text-align: center;
  color: #6d7a8e;
}

.link-button {
  padding: 0;
  border: 0;
  background: transparent;
  color: #c45d7c;
  font-weight: 700;
  cursor: pointer;
}

@media (max-width: 640px) {
  .login-shell {
    padding: 20px 14px;
  }

  .login-card {
    border-radius: 24px;
  }

  .login-image-wrap {
    padding: 16px;
  }

  .login-image {
    height: 240px;
    border-radius: 18px;
  }

  .login-copy,
  .login-form,
  .switch-copy {
    padding-left: 22px;
    padding-right: 22px;
  }

  .switch-copy {
    padding-bottom: 22px;
  }
}
</style>
