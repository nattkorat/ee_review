<script setup>
import { ref } from 'vue'
import axios from 'axios'
const username = ref('')
const password = ref('')
const emit = defineEmits(['register-success'])
const register = async () => {
  try {
    const response = await axios.post('/api/v1/auth/register', {
      username: username.value,
      password: password.value,
    })

    if (response.status) {
      alert('Registration successful!')
      // auto login to get token
      const loginResponse = await axios.post('/api/v1/auth/login', new URLSearchParams({
        username: username.value,
        password: password.value,
      }))
      if (loginResponse.status === 200 && loginResponse.data.access_token) {
        // Store the token in local storage or Vuex store
        localStorage.setItem('authToken', loginResponse.data.access_token)
      } else {
        alert('Login after registration failed: ' + loginResponse.status)
      }

      // Optionally, redirect to login or home page
      emit('register-success')
    } else {
      alert('Registration failed: ' + response.status)
    }
  } catch (error) {
    console.error('Registration error:', error)
    alert('An error occurred during registration.')
  }
}
</script>

<template>
  <div>
    <h1 class="text-2xl font-semibold mb-4">Register</h1>
    <input v-model="username" placeholder="Username" class="input mb-2 w-full p-2 border rounded" />
    <input
      v-model="password"
      placeholder="Password"
      type="password"
      class="input mb-4 w-full p-2 border rounded"
    />
    <button @click="register" class="btn bg-blue-500 text-white px-4 py-2 rounded">Register</button>
  </div>
</template>
