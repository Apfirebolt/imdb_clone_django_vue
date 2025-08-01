<template>
  <button
    @click="saveMovie"
    :disabled="isSaving"
    class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 transition-colors"
  >
    {{ isSaving ? "Saving..." : "Save Movie" }} <font-awesome-icon icon="save" class="ml-2" />
  </button>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["saveMovie"]);

const isSaving = ref(false);

async function saveMovie(movie) {
    isSaving.value = true;
    try {
        await emit("saveMovie", movie);
    } catch (error) {
        console.error("Error saving movie:", error);
    } finally {
        isSaving.value = false;
    }
}
</script>
