<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">
        {{ movie ? "Edit Movie Review" : "Add Movie Review" }}
    </h2>
    <MdEditor v-model="text" language="en-US" />

    <button
      class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
      @click="emit('addReview', text)"
    >
      Submit Review
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { MdEditor } from "md-editor-v3";

const props = defineProps({
  movie: {
    type: Object,
    required: false,
  },
});

const emit = defineEmits(["addReview"]);

const text = ref("# Write your review here...");

onMounted(() => {
  if (props.movie && props.movie.review) {
    text.value = props.movie.review;
  }
});
</script>
