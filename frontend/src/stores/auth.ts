import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

const API_BASE_URL = '/api/v1'

export interface User {
  user_id: number
  username: string
  email?: string
  role: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(username: string, password: string) {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    const response = await axios.post(`${API_BASE_URL}/auth/login`, formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })

    const { access_token, user: userData } = response.data
    token.value = access_token
    user.value = userData
    localStorage.setItem('token', access_token)

    axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

    return response.data
  }

  async function register(username: string, password: string, email: string, role: string = 'teacher') {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, {
      username,
      password,
      email,
      role,
    })
    return response.data
  }

  async function fetchCurrentUser() {
    if (!token.value) return null

    try {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      const response = await axios.get(`${API_BASE_URL}/auth/me`)
      user.value = response.data.data
      return user.value
    } catch {
      logout()
      return null
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
  }

  // 初始化时恢复 token
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    fetchCurrentUser,
    logout,
  }
})
