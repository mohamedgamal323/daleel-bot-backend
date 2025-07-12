import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<any>(null)
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'global_admin' || user.value?.role === 'domain_admin')

  // Actions
  const login = async (credentials: any): Promise<void> => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Login failed')
      }

      const loginData = await response.json()
      
      token.value = loginData.access_token
      localStorage.setItem('auth_token', loginData.access_token)
      
      // Use the user data from the login response
      if (loginData.user) {
        user.value = {
          id: loginData.user.id,
          username: loginData.user.username,
          email: loginData.user.email,
          role: loginData.user.role,
          is_active: loginData.user.is_active,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = async (): Promise<void> => {
    try {
      await fetch('/api/v1/auth/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token.value}`
        }
      })
    } catch (err) {
      console.warn('Logout API call failed:', err)
    }
    
    user.value = null
    token.value = null
    localStorage.removeItem('auth_token')
  }

  const register = async (userData: any): Promise<void> => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Registration failed')
      }

      const loginData = await response.json()
      
      token.value = loginData.access_token
      localStorage.setItem('auth_token', loginData.access_token)
      
      // Use the user data from the registration response
      if (loginData.user) {
        user.value = {
          id: loginData.user.id,
          username: loginData.user.username,
          email: loginData.user.email,
          role: loginData.user.role,
          is_active: loginData.user.is_active,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Registration failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const init = async (): Promise<void> => {
    console.log('Auth store init called')
    console.log('Token from localStorage:', token.value)
    console.log('Is authenticated:', isAuthenticated.value)
    
    if (token.value) {
      console.log('User has token, considered authenticated')
    } else {
      console.log('No token found, user not authenticated')
    }
  }

  return {
    // State
    user,
    token,
    loading,
    error,
    
    // Getters
    isAuthenticated,
    isAdmin,
    
    // Actions
    login,
    logout,
    register,
    init,
  }
})
