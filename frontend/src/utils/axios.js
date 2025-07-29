// src/utils/axios.js
import axios from 'axios'
import router from '@/router'

const instance = axios.create({
  baseURL: '/',
})

// Request interceptor: Add token
instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor: Redirect on 401/403
instance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      localStorage.removeItem('authToken') // Optional: clear token
      router.push('/') // Redirect to home page for login
    }
    return Promise.reject(error)
  }
)

export default instance
