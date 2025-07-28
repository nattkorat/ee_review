<script setup>
defineEmits(['upload']);
</script>

<template>
    <button class="btn rounded cursor-pointer p-2 bg-sky-500 text-white" @click="$emit('upload')">+ Upload Task</button>
</template>