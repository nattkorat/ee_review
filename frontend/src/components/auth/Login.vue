<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const username = ref('')
const password = ref('')

const emit = defineEmits(['login-success'])

const login = async () => {
  try {
    const response = await axios.post('/api/v1/auth/login', new URLSearchParams({
      username: username.value,
      password: password.value,
    }))

    if (response.status === 200 && response.data.access_token) {
      // Store the token in local storage or Vuex store
      localStorage.setItem('authToken', response.data.access_token)

      // get user info
      const userResponse = await axios.get('/api/v1/auth/me', {
        headers: { 'Authorization': `Bearer ${response.data.access_token}` }
      })
      if (userResponse.status === 200) {
        localStorage.setItem('user', JSON.stringify(userResponse.data))
      } else {
        console.error('Failed to fetch user data:', userResponse.status)
      }

      emit('login-success')
    } else {
      console.log('Login failed:', response)
      alert('Login failed: ' + response.status)
    }
  } catch (error) {
    console.error('Login error:', error)
    alert('Username or password is incorrect.')
    password.value = '' // Clear password field on error
  }
}
</script>

<template>
  <div class="w-50">
    <h1 class="text-2xl font-semibold mb-4">Login</h1>
    <input
      v-model="username"
      placeholder="Username"
      class="input mb-2 w-full p-2 border rounded"
    />
    <input
      v-model="password"
      placeholder="Password"
      type="password"
      class="input mb-4 w-full p-2 border rounded"
    />
    <button @click="login" class="btn bg-blue-500 text-white px-4 py-2 mt-2 rounded cursor-pointer">
      Login
    </button>
  </div>
</template>
