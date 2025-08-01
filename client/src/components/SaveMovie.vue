<template>
  <button
    @click="saveMovie"
    :disabled="isSaving"
    class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 transition-colors"
  >
    {{ isSaving ? "Saving..." : "Save Movie" }}
  </button>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  movieId: {
    type: [String, Number],
    required: true,
  },
});

const emit = defineEmits(["saved"]);

const isSaving = ref(false);

async function saveMovie() {
  isSaving.value = true;
  try {
    await fetch(`/api/movies/${props.movieId}/save/`, {
      method: "POST",
    });
    emit("saved");
  } catch (error) {
    alert("Failed to save movie.");
  } finally {
    isSaving.value = false;
  }
}
</script>
