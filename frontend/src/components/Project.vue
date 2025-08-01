<script setup>
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import Upload from './Upload.vue';
import axios from '@/utils/axios';

const route = useRoute();
const projectId = ref(route.params.id);

const token = ref(localStorage.getItem('authToken') || '');
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'));
const projectName = ref('');
const tasks = ref([]);

const fileInput = ref(null);

// Filter and pagination state
const filterStatus = ref('all'); // 'all' | 'completed' | 'not_completed'
const currentPage = ref(1);
const pageSize = 10; // You can customize this
const totalPages = ref(1);

// Fetch project
const fetchProject = async () => {
  try {
    const response = await axios.get(`/api/v1/projects/${projectId.value}`, {
      headers: { 'Authorization': `Bearer ${token.value}` }
    });
    if (response.status === 200) {
      projectId.value = response.data.id;
      projectName.value = response.data.name;
    }
  } catch (error) {
    console.error('Error fetching project:', error);
  }
};

// Fetch tasks with filters & pagination
const fetchTasks = async () => {
  try {
    const skip = (currentPage.value - 1) * pageSize;

    const status =
      filterStatus.value === 'completed'
        ? true
        : filterStatus.value === 'not_completed'
        ? false
        : undefined;

    const params = {
      skip,
      limit: pageSize,
      ...(status !== undefined && { status }), // Only include if defined
    };

    const response = await axios.get(`/api/v1/projects/${projectId.value}/tasks`, {
      headers: { Authorization: `Bearer ${token.value}` },
      params,
    });

    if (response.status === 200) {
      tasks.value = response.data.tasks;
      totalPages.value = Math.ceil(response.data.total / pageSize);
    }
  } catch (error) {
    console.error('Error fetching tasks:', error);
  }
};


const triggerFileSelection = () => fileInput.value.click();

const handleFileChange = async (event) => {
  const file = event.target.files[0];
  if (!file || !file.name.endsWith('.jsonl')) {
    alert('Only .jsonl files are allowed.');
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post(`/api/v1/projects/${projectId.value}/tasks/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    alert('Upload successful!');
    console.log(response.data);
    fetchTasks(); // Refresh tasks
  } catch (error) {
    console.error('Upload failed:', error);
    alert('Failed to upload file.');
  }
};

onMounted(() => {
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`;
    fetchProject();
    fetchTasks();
  } else {
    console.error('No authentication token found');
  }
});

// Watchers to update when filters/pagination change
watch(filterStatus, () => {
  currentPage.value = 1;
  fetchTasks();
});
watch(currentPage, fetchTasks);
</script>


<template>
  <h1 class="text-3xl mb-8" v-if="projectId">{{ projectName }}</h1>
  <div v-if="user && user.level === 0">
    <Upload v-if="projectId" @upload="triggerFileSelection" />
  </div>
  <input
    type="file"
    ref="fileInput"
    class="hidden"
    @change="handleFileChange"
    accept=".jsonl"
    v-if="projectId"
  />

  <h2 class="text-xl text-gray-600" v-else>Loading project...</h2>
  <div v-if="!projectId" class="mt-4 text-gray-500">No project found.</div>

  <!-- Filter Dropdown -->
  <div class="mt-4 flex gap-4 items-center">
    <label class="text-gray-600">Filter:</label>
    <select v-model="filterStatus" class="border p-2 rounded">
      <option value="all">All</option>
      <option value="completed">Completed</option>
      <option value="not_completed">Not Completed</option>
    </select>
  </div>

  <!-- Tasks -->
  <div v-if="tasks.length > 0" class="mt-4 grid grid-cols-1">
    <ul>
      <li
        v-for="task in tasks"
        :key="task.id"
        class="mb-2 block p-4 bg-white shadow cursor-pointer hover:shadow-md transition rounded-xl border border-gray-200 justify-between"
      >
        <router-link
          :to="`/projects/${projectId}/tasks/${task.id}`"
          class="flex-1"
        >
          <it>{{ task.article }}</it>
        </router-link>
        <span
          :class="task.status ? 'text-green-500' : 'text-red-500'"
          class="ml-4"
        >
          {{ task.status ? 'Completed' : 'Not Completed' }}
        </span>
      </li>
    </ul>
  </div>
  <div v-else class="mt-4 text-gray-500">No tasks available for this filter.</div>

  <!-- Pagination -->
  <div v-if="totalPages >= 1" class="mt-6 flex justify-center gap-4">
    <button
      @click="currentPage--"
      :disabled="currentPage === 1"
      class="px-4 py-2 border rounded disabled:opacity-50 cursor-pointer"
    >
      Prev
    </button>
    <span class="self-center">Page {{ currentPage }} of {{ totalPages }}</span>
    <button
      @click="currentPage++"
      :disabled="currentPage === totalPages"
      class="px-4 py-2 border rounded disabled:opacity-50 cursor-pointer"
    >
      Next
    </button>
  </div>
</template>
