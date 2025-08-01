<script setup>
import { ref, onMounted, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from '@/utils/axios';

const route = useRoute();
const router = useRouter();
const taskId = route.params.taskId;
const projectId = route.params.projectId;

const article = ref('');
const events = ref([]);
const comment = ref('');
const isLoading = ref(true);

const EVENT_TEMPLATES = {
  Infect: ['infected', 'disease', 'place', 'time', 'value', 'information-source'],
  Spread: ['population', 'disease', 'place', 'time', 'value', 'information-source', 'trend'],
  Symptom: ['person', 'symptom', 'disease', 'place', 'time', 'duration', 'information-source'],
  Prevent: ['agent', 'disease', 'means', 'information-source', 'target', 'effectiveness'],
  Control: ['authority', 'disease', 'means', 'place', 'time', 'information-source', 'subject', 'effectiveness'],
  Cure: ['cured', 'disease', 'means', 'place', 'time', 'value', 'facility', 'information-source', 'effectiveness', 'duration'],
  Death: ['dead', 'disease', 'place', 'time', 'value', 'information-source', 'trend'],
};

const  getArgumentsTemplate = (type) => {
  return (EVENT_TEMPLATES[type] || []).map(role => ({
    role,
    text: '',
    incorrect: false,
    correction: '',
    comment: ''
  }));
}

function normalizeEvent(raw = {}) {
  const argsMap = {};
  (raw.arguments ?? []).forEach(arg => {
    argsMap[arg.role] = {
      text: arg.text,
      incorrect: false,
      correction: '',
      comment: ''
    };
  });

  const fullArgs = (EVENT_TEMPLATES[raw.event_type] || []).map(role => ({
    role,
    ...argsMap[role] || {
      text: '',
      incorrect: false,
      correction: '',
      comment: ''
    }
  }));

  return {
    id: raw.id ?? Date.now(),
    event_type: raw.event_type ?? '',
    event_type_incorrect: false,
    event_type_comment: '',
    trigger: {
      text: raw.trigger?.text ?? '',
      incorrect: false,
      comment: '',
      correction: ''
    },
    arguments: fullArgs
  };
}

// Watch when event type changes and re-initialize argument slots
function setupEventTypeWatchers() {
  events.value.forEach((event, index) => {
    watchEffect(() => {
      if (!event.event_type) return;
      const expectedRoles = EVENT_TEMPLATES[event.event_type];
      const filledRoles = new Set(event.arguments.map(arg => arg.role));
      const newArgs = [];

      for (const role of expectedRoles) {
        if (!filledRoles.has(role)) {
          newArgs.push({
            role,
            text: '',
            incorrect: false,
            correction: '',
            comment: ''
          });
        }
      }
      event.arguments.push(...newArgs);
    });
  });
}

const fetchTask = async () => {
  try {
    const res = await axios.get(`/api/v1/projects/${projectId}/tasks/${taskId}`);
    article.value = res.data.article;
    events.value = (res.data.events ?? []).map(event => normalizeEvent(event));
  } catch (err) {
    console.error('Failed to load task:', err);
  } finally {
    isLoading.value = false;
  }
};

const addEvent = () => {
  const newEvent = normalizeEvent({});
  events.value.push(newEvent);
  setupEventTypeWatchers();
};

const removeEvent = (index) => {
  events.value.splice(index, 1);
};

const submitReview = async () => {
  try {
    const payload = {
      events: JSON.stringify(events.value),
      comment: comment.value,
    };
    console.log('Submitting review:', payload);
    await axios.post(`/api/v1/projects/${projectId}/tasks/${taskId}/review`, payload);
    alert('Review submitted successfully!');
    router.push(`/projects/${projectId}`);
  } catch (err) {
    console.error('Failed to submit review:', err);
    alert('Error submitting review.');
  }
};

onMounted(fetchTask);
</script>

<template>
  <div class="flex flex-col md:flex-row gap-6 p-6 h-[calc(100vh-100px)]">
    <!-- Article Panel -->
    <div class="md:w-1/2 border p-4 rounded-xl bg-gray-50 shadow-sm overflow-y-auto max-h-full">
      <h2 class="text-xl font-semibold mb-4">Article</h2>
      <p class="whitespace-pre-line text-gray-800">{{ article }}</p>
    </div>

    <!-- Review Panel -->
    <div class="md:w-1/2 border p-4 rounded-xl bg-white shadow-sm overflow-y-auto max-h-full">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Events</h2>
      </div>

      <!-- Each Event -->
      <div v-for="(event, index) in events" :key="event.id" class="border p-3 mb-4 rounded-lg bg-gray-100">
        <!-- Trigger -->
        <label class="block text-sm font-medium">Trigger</label>
        <div class="flex gap-2 items-center mb-1">
          <input v-model="event.trigger.text" class="w-full p-2 border rounded" />
          <label class="text-xs flex items-center gap-1 text-gray-500">
            <input type="checkbox" v-model="event.trigger.incorrect" /> Incorrect
          </label>
        </div>
        <div v-if="event.trigger.incorrect" class="mb-2">
          <input v-model="event.trigger.correction" class="w-full p-2 border rounded mb-1" placeholder="Corrected trigger text" />
          <textarea v-model="event.trigger.comment" class="w-full p-2 border rounded text-sm" placeholder="Comment on trigger..." />
        </div>

        <!-- Event Type -->
        <label class="block text-sm font-medium mt-2">Event Type</label>
        <div class="flex gap-2 items-center mb-1">
          <select v-model="event.event_type" class="w-full p-2 border rounded">
            <option disabled value="">Select type</option>
            <option v-for="type in Object.keys(EVENT_TEMPLATES)" :key="type" :value="type">{{ type }}</option>
          </select>
          <label class="text-xs flex items-center gap-1 text-gray-500">
            <input type="checkbox" v-model="event.event_type_incorrect" /> Incorrect
          </label>
        </div>
        <div v-if="event.event_type_incorrect" class="mb-2">
          <textarea v-model="event.event_type_comment" class="w-full p-2 border rounded text-sm" placeholder="Comment on event type..." />
        </div>

        <!-- Arguments -->
        <label class="block text-sm font-medium mt-2">Arguments</label>
        <div v-for="(arg, argIdx) in event.arguments" :key="argIdx" class="ml-8 mb-2">
          <div class="flex gap-2 items-center">
            <label for="arg" class="w-40">{{ arg.role }}</label>
            <input v-model="arg.text"
                   class="w-full p-2 border rounded" />
            <label class="text-xs flex items-center gap-1 text-gray-500">
              <input type="checkbox" v-model="arg.incorrect" /> Incorrect
            </label>
          </div>
          <div v-if="arg.incorrect" class="mt-1 space-y-1">
            <input v-model="arg.correction" class="w-full p-2 border rounded" placeholder="Corrected value" />
            <textarea v-model="arg.comment" class="w-full p-2 border rounded text-sm" placeholder="Comment on argument..." />
          </div>
        </div>

        <!-- Remove -->
        <button @click="removeEvent(index)" class="mt-2 text-red-500 hover:text-red-700 text-sm">✖ Remove Event</button>
      </div>

      <button @click="addEvent" class="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600">
          + Add Event
        </button>

      <!-- Global Comment -->
      <label class="block text-sm font-medium mt-4">General Comment (Optional)</label>
      <textarea v-model="comment" class="w-full p-2 border rounded" />

      <!-- Submit -->
      <button @click="submitReview" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        Submit Review
      </button>
    </div>
  </div>
</template>
