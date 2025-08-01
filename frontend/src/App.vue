<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goDashboard = () => {
  router.push('/')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 w-full ">
    <nav class="w-full bg-white shadow p-4 flex justify-between items-center fixed top-0 left-0 z-10">
      <h1 class="text-xl font-semibold text-blue-600 cursor-pointer" @click="goDashboard">Epidemic Event Extraction Evaluation</h1>
      <div class="space-x-4">
        <button @click="goDashboard" class="text-gray-700 hover:text-blue-600">Dashboard</button>
      </div>
    </nav>
    <div class="pt-16"> <!-- Add padding to prevent content from being hidden behind the fixed nav -->
      <!-- 🔄 Dynamic Views -->
      <div class="w-full p-6">
        <router-view />
      </div>
    </div>
  </div>
</template>
