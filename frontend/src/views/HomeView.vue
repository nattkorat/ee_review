<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Login from '@/components/auth/Login.vue'
import Register from '@/components/auth/Register.vue'
import Dashboard from '@/components/Dashboard.vue'

const isAuthenticated = ref(false)
const goRegister = ref(false)

onMounted(() => {
  // Check if the user is already authenticated
  const token = localStorage.getItem('authToken')
  if (token) {
    isAuthenticated.value = true
  }
})

</script>
<template>
  <div class="p-4">
    <div v-if="!isAuthenticated">
      <div v-if="!goRegister">
        <Login @login-success="isAuthenticated = true" />
        <p class="mt-4">Please log in to access the home page.</p>
        <button @click="goRegister = true" class="text-blue-500 hover:underline">
          Register
        </button>
      </div>
      <div v-else>
        <Register @register-success="isAuthenticated = true" />
        <p class="mt-4">Please register to access the home page.</p>
        <button @register-success="isAuthenticated = true" @click="goRegister = false" class="text-blue-500 hover:underline">
          Back to Login
        </button>
      </div>
    </div>
    <div v-else>
      <Dashboard />
    </div>
  </div>
</template>
