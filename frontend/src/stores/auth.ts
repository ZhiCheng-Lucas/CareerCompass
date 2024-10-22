import { defineStore } from 'pinia'
import { login as apiLogin, register as apiRegister } from '@/services/api'

interface User {
  username: string
  skills: string[]
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  loading: boolean
  error: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoading: (state) => state.loading,
    authError: (state) => state.error
  },

  actions: {
    async login(username: string, password: string) {
      this.loading = true
      this.error = null
      
      try {
        const response = await apiLogin(username, password)
        this.user = response
        this.isAuthenticated = true
      } catch (error: any) {
        this.error = error.response?.data?.detail || 'An error occurred during login'
        throw error
      } finally {
        this.loading = false
      }
    },

    async register(username: string, password: string) {
      this.loading = true
      this.error = null
      
      try {
        await apiRegister(username, password)
        // Auto login after successful registration
        await this.login(username, password)
      } catch (error: any) {
        this.error = error.response?.data?.detail || 'An error occurred during registration'
        throw error
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.user = null
      this.isAuthenticated = false
      this.error = null
    }
  }
})