<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from '@/utils/axios'; // Your Axios instance with auth interceptors

const route = useRoute();
const taskId = route.params.taskId;
const projectId = route.params.projectId;

const article = ref('');
const events = ref([]);
const comment = ref('');
const isLoading = ref(true);

const emptyEvent = () => ({
  id: Date.now(), // Temporary ID for Vue reactivity
  trigger: { text: '', approx_start: null },
  event_type: '',
  arguments: []
});

const fetchTask = async () => {
  try {
    const res = await axios.get(`/api/v1/projects/${projectId}/tasks/${taskId}`);
    article.value = res.data.article;
    console.log('Task loaded:', res.data.events);
    events.value = res.data.events ?? [];
  } catch (err) {
    console.error('Failed to load task:', err);
  } finally {
    isLoading.value = false;
  }
};

const addEvent = () => {
  events.value.push(emptyEvent());
};

const removeEvent = (index) => {
  events.value.splice(index, 1);
};

const addArgument = (event) => {
  event.arguments.push({ text: '', role: '' });
};

const removeArgument = (event, index) => {
  event.arguments.splice(index, 1);
};

const submitReview = async () => {
  try {
    const payload = {
      reviewed_events: events.value,
    };
    await axios.post(`/api/v1/projects/${projectId}/tasks/${taskId}/review`, payload);
    alert('Review submitted successfully!');
  } catch (err) {
    console.error('Failed to submit review:', err);
    alert('Error submitting review.');
  }
};

onMounted(fetchTask);
</script>

<template>
    <h1 class="text-3xl ml-4 underline"> Epidemic Event Extraction Evaluation</h1>
  <div class="flex flex-col md:flex-row gap-6 p-6 h-[calc(100vh-100px)]">
    
    <!-- Article Panel -->
    <div class="md:w-1/2 border p-4 rounded-xl bg-gray-50 shadow-sm overflow-y-auto max-h-full">
      <h2 class="text-xl font-semibold mb-4">Article</h2>
      <p class="whitespace-pre-line text-gray-800">{{ article }}</p>
    </div>

    <!-- Events Panel -->
    <div class="md:w-1/2 border p-4 rounded-xl bg-white shadow-sm overflow-y-auto max-h-full">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Events</h2>
        <button @click="addEvent" class="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600">
          + Add Event
        </button>
      </div>

      <div v-for="(event, index) in events" :key="event.id" class="border p-3 mb-3 rounded-lg bg-gray-100">
        <div class="flex justify-between gap-2">
          <div class="w-full">
            <label class="block text-sm font-medium">Trigger</label>
            <input v-model="event.trigger.text" class="w-full p-2 border rounded mt-1 mb-2" />

            <label class="block text-sm font-medium">Type</label>
            <input v-model="event.event_type" class="w-full p-2 border rounded mt-1 mb-2" />

            <label class="block text-sm font-medium">Arguments</label>
            <div v-for="(arg, argIdx) in event.arguments" :key="argIdx" class="ml-4 grid grid-cols-2 gap-2">
              <input v-model="arg.text" class="p-2 border rounded" placeholder="Argument text" />
              <input v-model="arg.role" class="p-2 border rounded" placeholder="Argument role" />
              <button @click="removeArgument(event, argIdx)" class="text-red-500 col-span-2 text-sm hover:underline text-right">
                ✖ Remove Argument
              </button>
            </div>
            <button @click="addArgument(event)"
                    class="ml-4 mt-2 px-2 py-1 bg-gray-200 rounded hover:bg-gray-300 text-sm">
              + Add Argument
            </button>
          </div>

          <button @click="removeEvent(index)" class="ml-2 mt-2 px-2 text-red-500 hover:text-red-700 text-lg">✖</button>
        </div>
      </div>
      <label for="">Comment (Optional)</label>
      <textarea class="p-2 border rounded w-full" v-model="comment"></textarea>

      <button @click="submitReview" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        Submit Review
      </button>
    </div>
  </div>
</template>
