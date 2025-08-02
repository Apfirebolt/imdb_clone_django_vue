<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Editor</h2>
    <MdEditor v-model="text" language="en-US" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { MdEditor } from 'md-editor-v3';

const text = ref('# Hello Editor');

</script>
