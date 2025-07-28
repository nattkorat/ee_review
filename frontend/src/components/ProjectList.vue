<script setup>
import CreateProject from './CreateProject.vue';

import { ref, onMounted } from 'vue'
import axios from 'axios'
const projects = ref([])

const projectName = ref('')
const projectDescription = ref('')
const isCreate = ref(false)

const token = ref(localStorage.getItem('authToken') || '')

const getProjects = async () => axios.get('/api/v1/projects', {
    headers: {
        'Authorization': `Bearer ${token.value}`
    }
}).then(response => {
    if (response.status === 200) {
        projects.value = response.data || []
    } else {
        console.error('Failed to fetch projects:', response.status)
    }
}).catch(error => {
    console.error('Error fetching projects:', error)
})

onMounted(() => {
    if (token.value) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
        getProjects()
    } else {
        console.error('No authentication token found')
    }
})

const createProject = async () => {
    try {
        const response = await axios.post('/api/v1/projects', {
            name: projectName.value,
            description: projectDescription.value
        }, 
        {
            headers: {
                'Authorization': `Bearer ${token.value}`,
            }
        })

        if (response.status === 201) {
            // console.log('Project created successfully:', response.data)
            projects.value.push(response.data)
            isCreate.value = false // Close the modal
        } else {
            console.error('Failed to create project:', response.status)
        }
    } catch (error) {
        console.error('Error creating project:', error)
    }
}

</script>

<template>
    <div>
      <CreateProject @create="isCreate = true" />
      <!-- hidden form for creating a new project -->
      <div
        v-if="isCreate"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 bg-opacity-40"
        >
        <!-- Modal Box -->
        <div class="bg-white p-6 rounded-xl shadow-xl w-full max-w-md">
            <h3 class="text-xl font-semibold mb-4 text-center">Create New Project</h3>

            <div class="flex flex-col gap-4">
            <!-- Project Name -->
            <input
                type="text"
                v-model="projectName"
                placeholder="Project Name"
                class="px-4 py-2 border rounded"
            />

            <!-- Project Description -->
            <textarea
                v-model="projectDescription"
                placeholder="Project Description"
                rows="4"
                class="px-4 py-2 border rounded resize-none"
            ></textarea>

            <!-- Buttons Row -->
            <div class="flex justify-end gap-2">
                <button
                class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                @click="createProject"
                >
                Create
                </button>
                <button
                @click="isCreate = false"
                class="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                >
                Cancel
                </button>
            </div>
            </div>
        </div>
     </div>


      <div v-if="projects.length === 0" class="text-gray-500 mt-4">No projects available.</div>
  
      <div v-else class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        <router-link
          v-for="project in projects"
          :key="project.id"
          :to="`/projects/${project.id}`"
          class="block p-4 bg-white shadow hover:shadow-md transition rounded-xl border border-gray-200"
          @click="console.log(`Navigating to project ${project.id}`)"
        >
          <h2 class="text-lg font-semibold text-blue-600 truncate p-2">{{ project.name }}</h2>
          <p class="text-gray-600 mt-1 line-clamp-2 p-2">{{ project.description }}</p>
        </router-link>
      </div>
    </div>
  </template>
  