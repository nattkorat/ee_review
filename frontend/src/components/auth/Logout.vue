<script setup>
const logout = () => {
  // Clear the token from local storage
  localStorage.removeItem('authToken')
  // Redirect the user to the login page or home page
  window.location.href = '/'
}
</script>

<template>
  <button @click="logout" class="btn bg-blue-500 text-white px-4 py-2 mt-8 rounded cursor-pointer">Logout</button>
</template>
