<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-lg">
      <!-- Logo -->
      <div class="flex justify-center">
        <div class="flex items-center space-x-2">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <span class="text-2xl font-bold text-gray-900">DaleelBot</span>
        </div>
      </div>
      
      <!-- Title -->
      <h2 class="mt-6 text-center text-3xl font-bold text-gray-900">
        Welcome to DaleelBot
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Create your account or 
        <router-link 
          to="/login" 
          class="font-medium text-blue-600 hover:text-blue-500"
        >
          sign in to your existing account
        </router-link>
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-lg">
      <div class="bg-white py-10 px-6 shadow-xl sm:rounded-lg sm:px-12 border border-gray-200">
        <form class="space-y-6" @submit.prevent="handleRegister">
          <!-- Username -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              Username
            </label>
            <div class="mt-1">
              <input
                id="username"
                name="username"
                type="text"
                autocomplete="username"
                required
                v-model="form.username"
                :disabled="loading"
                class="appearance-none block w-full px-4 py-3 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
                :class="{ 'opacity-50 cursor-not-allowed': loading }"
              />
            </div>
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              Email address
            </label>
            <div class="mt-1">
              <input
                id="email"
                name="email"
                type="email"
                autocomplete="email"
                required
                v-model="form.email"
                :disabled="loading"
                class="appearance-none block w-full px-4 py-3 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
                :class="{ 'opacity-50 cursor-not-allowed': loading }"
              />
            </div>
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <div class="mt-1">
              <input
                id="password"
                name="password"
                type="password"
                autocomplete="new-password"
                required
                v-model="form.password"
                :disabled="loading"
                class="appearance-none block w-full px-4 py-3 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
                :class="{ 'opacity-50 cursor-not-allowed': loading }"
              />
            </div>
          </div>

          <!-- Confirm Password -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">
              Confirm Password
            </label>
            <div class="mt-1">
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                autocomplete="new-password"
                required
                v-model="form.confirmPassword"
                :disabled="loading"
                class="appearance-none block w-full px-4 py-3 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
                :class="{ 'opacity-50 cursor-not-allowed': loading }"
              />
            </div>
          </div>

          <!-- Role -->
          <div>
            <label for="role" class="block text-sm font-medium text-gray-700">
              Role
            </label>
            <div class="mt-1">
              <select
                id="role"
                name="role"
                v-model="form.role"
                :disabled="loading"
                class="block w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
                :class="{ 'opacity-50 cursor-not-allowed': loading }"
              >
                <option value="user">User</option>
                <option value="domain_admin">Domain Admin</option>
                <option value="global_admin">Global Admin</option>
              </select>
            </div>
          </div>

          <!-- Terms and conditions -->
          <div class="flex items-center">
            <input
              id="terms"
              name="terms"
              type="checkbox"
              v-model="form.acceptTerms"
              required
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label for="terms" class="ml-2 block text-sm text-gray-900">
              I agree to the
              <a href="#" class="font-medium text-blue-600 hover:text-blue-500">
                Terms and Conditions
              </a>
            </label>
          </div>

          <!-- Error message -->
          <div v-if="error" class="rounded-md bg-red-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800">
                  {{ error }}
                </h3>
              </div>
            </div>
          </div>

          <!-- Validation errors -->
          <div v-if="validationErrors.length > 0" class="rounded-md bg-red-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800">
                  Please fix the following errors:
                </h3>
                <ul class="mt-2 text-sm text-red-700 list-disc pl-5">
                  <li v-for="error in validationErrors" :key="error">{{ error }}</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Submit button -->
          <div>
            <button
              type="submit"
              :disabled="loading || !isFormValid"
              class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                <svg
                  v-if="loading"
                  class="animate-spin h-5 w-5 text-blue-300"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <svg
                  v-else
                  class="h-5 w-5 text-blue-500 group-hover:text-blue-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z" />
                </svg>
              </span>
              {{ loading ? 'Creating account...' : 'Create account' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref<any>({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: 'user',
  acceptTerms: false,
})

const loading = computed(() => authStore.loading)
const error = computed(() => authStore.error)

const validationErrors = computed(() => {
  const errors: string[] = []
  
  if (form.value.username.length < 3) {
    errors.push('Username must be at least 3 characters long')
  }
  
  if (form.value.password.length < 8) {
    errors.push('Password must be at least 8 characters long')
  }
  
  if (form.value.password !== form.value.confirmPassword) {
    errors.push('Passwords do not match')
  }
  
  if (!form.value.acceptTerms) {
    errors.push('You must accept the terms and conditions')
  }
  
  return errors
})

const isFormValid = computed(() => {
  return (
    form.value.username.length >= 3 &&
    form.value.email.length > 0 &&
    form.value.password.length >= 8 &&
    form.value.password === form.value.confirmPassword &&
    form.value.acceptTerms
  )
})

const handleRegister = async () => {
  if (!isFormValid.value) {
    return
  }
  
  try {
    await authStore.register({
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      role: form.value.role,
    })
    
    // Redirect to dashboard
    router.push('/')
  } catch (err) {
    // Error is handled by the store
    console.error('Registration error:', err)
  }
}
</script>
