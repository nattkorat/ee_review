<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import Upload from './Upload.vue';
const route = useRoute();
const projectId = ref(route.params.id);

import axios from 'axios';

const token = ref(localStorage.getItem('authToken') || '');
const projectName = ref('');
const tasks = ref([]);

const fileInput = ref(null);

const fetchProject = async () => {
  try {
    const response = await axios.get(`/api/v1/projects/${projectId.value}`, {
      headers: {
        'Authorization': `Bearer ${token.value}`
      }
    });
    if (response.status === 200) {
        projectId.value = response.data.id; // Assuming the project data has an 'id' field
        projectName.value = response.data.name; // Assuming the project data has a 'name' field 
    } else {
      console.error('Failed to fetch project:', response.status);
    }
  } catch (error) {
    console.error('Error fetching project:', error);
  }
};

const fetchTasks = async () => {
  try {
    const response = await axios.get(`/api/v1/projects/${projectId.value}/tasks`, {
      headers: {
        'Authorization': `Bearer ${token.value}`
      }
    });
    if (response.status === 200) {
      tasks.value = response.data || [];
    } else {
      console.error('Failed to fetch tasks:', response.status);
    }
  } catch (error) {
    console.error('Error fetching tasks:', error);
  }
};

const triggerFileSelection = () => {
  fileInput.value.click()
}

const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.name.endsWith('.jsonl')) {
    alert('Only .jsonl files are allowed.')
    return
  }

  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await axios.post('/api/upload-task', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    alert('Upload successful!')
    console.log(response.data)
  } catch (error) {
    console.error('Upload failed:', error)
    alert('Failed to upload file.')
  }
}

onMounted(() => {
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`;
    fetchProject();
    fetchTasks();
  } else {
    console.error('No authentication token found');
  }
});

</script>

<template>
   <h1 class="text-3xl mb-8" v-if="projectId">{{ projectName }}</h1>
    <Upload v-if="projectId" @upload="triggerFileSelection" />
      <input type="file" 
             ref="fileInput"
             class="hidden" 
             id="fileInput" 
             @change="handleFileChange" 
             accept=".jsonl" 
             v-if="projectId"
      />
    <h2 class="text-xl text-gray-600" v-else>Loading project...</h2>
      <div v-if="!projectId" class="mt-4 text-gray-500">No project found.</div>
      
    <div v-if="tasks.length > 0" class="mt-4 grid grid-cols-1">
          <ul>
                <li v-for="task in tasks" :key="task.id" 
                class="mb-2 block p-4 bg-white shadow cursor-pointer hover:shadow-md transition rounded-xl border border-gray-200 justify-between">
                 <router-link :to="`/projects/${projectId}/tasks/${task.id}`" class="flex-1">
                   <strong class="truncate">{{ task.article }}</strong>
                 </router-link>
                 <span :class="task.status ? 'text-green-500' : 'text-red-500'">
                   {{ task.completed ? 'Completed' : 'Not Completed' }}
                 </span>
                </li>
          </ul>
     </div>
     <div v-else class="mt-4 text-gray-500">No tasks available for this project.</div>
</template>