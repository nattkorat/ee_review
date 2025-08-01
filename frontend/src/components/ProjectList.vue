<script setup>
import CreateProject from './CreateProject.vue';

import { ref, onMounted } from 'vue'
import axios from 'axios'
const projects = ref([])

const projectName = ref('')
const projectDescription = ref('')
const isCreate = ref(false)
const selectedProject = ref(null);
const showEditModal = ref(false);

const token = ref(localStorage.getItem('authToken') || '')
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))


const openEditModal = (project) => {
  selectedProject.value = { ...project };
  showEditModal.value = true;
};

const closeEditModal = () => {
  showEditModal.value = false;
  selectedProject.value = null;
};

const removeProject = (projectId) => {
  if (confirm('Are you sure you want to delete this project?')) {
    // call delete API here
    try {
        axios.delete(`/api/v1/projects/${projectId}`, {
            headers: {
                'Authorization': `Bearer ${token.value}`,
            }
        }).then(response => {
            if (response.status === 204) {
                // Remove the project from the list
                projects.value = projects.value.filter(p => p.id !== projectId);

            } else {
                console.error('Failed to delete project:', response.status);
            }
        }).catch(error => {
            console.error('Error deleting project:', error);
        });
    } catch (error) {
        
    }
  }
};

const updateProject = async () => {
  try {
    const response = await axios.put(`/api/v1/projects/${selectedProject.value.id}`, {
      name: selectedProject.value.name,
      description: selectedProject.value.description
    }, {
      headers: {
        'Authorization': `Bearer ${token.value}`,
      }
    });

    if (response.status === 200) {
      // Update the project in the list
      const index = projects.value.findIndex(p => p.id === selectedProject.value.id);
      if (index !== -1) {
        projects.value[index] = response.data;
      }
      closeEditModal();
    } else {
      console.error('Failed to update project:', response.status);
    }
  } catch (error) {
    console.error('Error updating project:', error);
  }
}

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

const downloadExport = async (project) => {
  try {
    const response = await axios.get(`/api/v1/projects/${project.id}/export`, {
      responseType: 'blob', // IMPORTANT
    });

    const blob = new Blob([response.data], { type: 'application/jsonl' });
    const url = window.URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${project.name}_reviews.jsonl`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (err) {
    console.error('Failed to download file:', err);
  }
};

</script>

<template>
    <div class="w-full">
      <div v-if="user && user.level == 0">
        <CreateProject @create="isCreate = true" />
      </div>
      <!-- hidden form for creating a new project -->
      <div
        v-if="isCreate"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 bg-opacity-40"
        >
        <!-- Modal Box -->
        <div class="bg-white p-6 rounded-xl shadow-xl w-150">
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
  
      <div v-else class="w-full grid md:grid-cols-1 sm:grid-cols-1 lg:grid-cols-3  gap-4 mt-4">
    <div
      v-for="project in projects"
      :key="project.id"
      class="relative block p-4 bg-white shadow hover:shadow-md transition rounded-xl border border-gray-200"
    >
      <!-- Three Dots Menu -->
      <div class="absolute top-2 right-2" v-if="user && user.level === 0">
        <div class="relative group">
          <button class="text-gray-500 hover:text-gray-700 text-xl">⋯</button>
          <div class="absolute right-0 mt-1 w-32 bg-white border border-gray-200 rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity z-10">
            <button
              @click="downloadExport(project)"
              class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Export
            </button>
            <button
              @click="openEditModal(project)"
              class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Edit
            </button>
            <button
              @click="removeProject(project.id)"
              class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
            >
              Remove
            </button>
          </div>
        </div>
      </div>

      <!-- Clickable content -->
      <router-link :to="`/projects/${project.id}`">
        <h2 class="text-lg font-semibold text-blue-600 truncate p-2">{{ project.name }}</h2>
        <p class="text-gray-600 mt-1 line-clamp-2 p-2">{{ project.description }}</p>
      </router-link>
    </div>
  </div>

  <!-- Edit Modal -->
  <div v-if="showEditModal" class="fixed inset-0 flex items-center justify-center bg-black/50 bg-opacity-40 z-50">
    <div class="bg-white p-6 rounded-xl shadow-xl w-full">
      <h2 class="text-lg font-bold mb-4">Edit Project</h2>
      <label class="block text-sm font-medium">Name</label>
      <input
        v-model="selectedProject.name"
        class="w-full p-2 border rounded mt-1 mb-3"
      />
      <label class="block text-sm font-medium">Description</label>
      <textarea
        v-model="selectedProject.description"
        class="w-full p-2 border rounded mt-1 mb-3"
      ></textarea>
      <div class="flex justify-end gap-2">
        <button
          @click="closeEditModal"
          class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
        >
          Cancel
        </button>
        <button
          @click="updateProject"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Save
        </button>
      </div>
    </div>
  </div>
    </div>
  </template>
  