<template>
  <section class="register-shell">
    <div class="register-card">
      <div class="register-copy">
        <p class="eyebrow">Create account</p>
        <h1>Join the cacao monitor workspace</h1>
        <p class="subtitle">
          Register a test user locally to preview the authentication flow.
        </p>
      </div>

      <form class="register-form" @submit.prevent="register">
        <label class="field">
          <span class="field-label">Full Name</span>
          <div class="input-group">
            <span class="icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false">
                <path
                  d="M12 12a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm0 2c-4.42 0-8 2.24-8 5v1h16v-1c0-2.76-3.58-5-8-5Z"
                />
              </svg>
            </span>
            <input
              v-model.trim="form.fullName"
              type="text"
              name="fullName"
              placeholder="Juan Dela Cruz"
              autocomplete="name"
              required
            >
          </div>
        </label>

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
              autocomplete="new-password"
              required
            >
          </div>
        </label>

        <label class="field">
          <span class="field-label">Confirm Password</span>
          <div class="input-group">
            <span class="icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false">
                <path
                  d="M17 8h-1V6a4 4 0 0 0-8 0v2H7a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2Zm-6 7.73V17a1 1 0 0 0 2 0v-1.27a2 2 0 1 0-2 0ZM10 8V6a2 2 0 0 1 4 0v2Z"
                />
              </svg>
            </span>
            <input
              v-model="form.confirmPassword"
              type="password"
              name="confirmPassword"
              placeholder="Repeat password"
              autocomplete="new-password"
              required
            >
          </div>
        </label>

        <p v-if="error" class="message error">{{ error }}</p>
        <p v-if="successMessage" class="message success">{{ successMessage }}</p>

        <button class="register-button" type="submit">Register</button>
      </form>

      <p class="switch-copy">
        Already have an account?
        <button class="link-button" type="button" @click="emit('switch-auth', 'Login')">
          Login
        </button>
      </p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { registerUser } from '../services/auth'

type RegisterForm = {
  fullName: string
  email: string
  password: string
  confirmPassword: string
}

const emit = defineEmits<{
  'register-success': []
  'switch-auth': [screen: 'Login' | 'Register']
}>()

const emptyForm = (): RegisterForm => ({
  fullName: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const form = ref<RegisterForm>(emptyForm())
const error = ref('')
const successMessage = ref('')
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const register = async () => {
  error.value = ''
  successMessage.value = ''

  if (!form.value.fullName) {
    error.value = 'Full name is required.'
    return
  }

  if (!emailPattern.test(form.value.email)) {
    error.value = 'Please enter a valid email address.'
    return
  }

  if (form.value.password.length < 6) {
    error.value = 'Password must be at least 6 characters long.'
    return
  }

  if (form.value.password !== form.value.confirmPassword) {
    error.value = 'Passwords do not match.'
    return
  }

  try {
    await registerUser({
      fullName: form.value.fullName,
      email: form.value.email,
      password: form.value.password,
      role: 'user'
    })

    successMessage.value = 'Registration successful. You can log in now.'
    form.value = emptyForm()
    emit('register-success')
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Registration failed.'
  }
}
</script>

<style scoped>
:global(body) {
  font-family: inherit;
}

:global(*) {
  box-sizing: border-box;
}

.register-shell {
  min-height: calc(100vh - 152px);
  display: grid;
  place-items: center;
  padding: 32px 16px;
}

.register-card {
  width: min(100%, 460px);
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid #f5dbe5;
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 24px 60px rgba(36, 48, 66, 0.1);
  backdrop-filter: blur(10px);
}

.register-copy {
  margin-bottom: 24px;
}

.eyebrow {
  margin: 0 0 10px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #d46d8a;
}

h1 {
  margin: 0;
  font-size: clamp(1.75rem, 4vw, 2.3rem);
  line-height: 1.1;
}

.subtitle {
  margin: 12px 0 0;
  color: #5d6b7d;
  line-height: 1.6;
}

.register-form {
  display: grid;
  gap: 16px;
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

.register-button {
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

.register-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 30px rgba(159, 217, 204, 0.28);
}

.register-button:active {
  transform: translateY(0);
}

.switch-copy {
  margin: 18px 0 0;
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
  .register-shell {
    padding: 20px 14px;
  }

  .register-card {
    padding: 22px;
    border-radius: 20px;
  }
}
</style>
