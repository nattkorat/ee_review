<script setup>

defineEmits(['create']);


</script>

<template>
    <button class="btn rounded cursor-pointer p-2 bg-gray-50" @click="$emit('create')">+ Creat Project</button>
</template>