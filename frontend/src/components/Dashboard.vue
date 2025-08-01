<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Logout from './auth/Logout.vue'
import ProjectList from './ProjectList.vue'

const token = ref(localStorage.getItem('authToken') || '')
const isAuthenticated = ref(!!token.value)
const user = ref('Guest')


const fetchUserData = async () => {
  try {
    const response = await axios.get('/api/v1/auth/me')
    if (response.status === 200) {
      // Assuming the user data is in response.data
      user.value = response.data.username || 'User'
    } else {
      console.error('Failed to fetch user data:', response.status)
      isAuthenticated.value = false
    }
  } catch (error) {
    console.error('Error fetching user data:', error)
    isAuthenticated.value = false
    localStorage.removeItem('authToken') // Clear token on error
    window.location.href = '/' // Redirect to login if error occurs
  }
}

onMounted(() => {
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    fetchUserData()
  } else {
    isAuthenticated.value = false
  }
})

</script>

<template>
  <div>
    <div v-if="isAuthenticated">
        <ProjectList/>
        <Logout />
    </div>
  </div>
</template>
