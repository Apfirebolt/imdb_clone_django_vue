<template>
  <div class="w-full max-w-4xl mx-auto">
    <div class="rounded-2xl border border-[var(--color-secondary)]/30 bg-white p-6 sm:p-8 shadow-sm">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-5 mb-5 border-b border-[var(--color-secondary)]/20">
        <div>
          <span class="text-xs font-bold uppercase tracking-wider text-[var(--color-tertiary)] font-display">
            {{ isEditing ? 'Community Feedback' : 'New Critique' }}
          </span>
          <h2 class="text-2xl font-bold font-heading text-[var(--color-dark)] tracking-tight mt-0.5 mb-0">
            {{ isEditing ? 'Edit Movie Review' : 'Add Movie Review' }}
          </h2>
          <p v-if="movie?.title" class="text-xs text-gray-500 mt-1 font-body">
            Reviewing: <span class="font-semibold text-[var(--color-dark)]">{{ movie.title }}</span>
          </p>
        </div>

        <!-- Word & Character stats -->
        <div class="flex items-center gap-3 text-xs text-gray-500 font-body bg-[var(--color-light)] px-3 py-1.5 rounded-lg border border-[var(--color-secondary)]/20 self-start sm:self-auto">
          <span><strong class="text-[var(--color-dark)]">{{ wordCount }}</strong> words</span>
          <span class="text-gray-300">|</span>
          <span><strong class="text-[var(--color-dark)]">{{ text.length }}</strong> characters</span>
        </div>
      </div>

      <!-- Markdown Editor Wrapper -->
      <div class="custom-editor-wrapper rounded-xl overflow-hidden border border-[var(--color-secondary)]/40 focus-within:border-[var(--color-primary)] transition">
        <MdEditor
          v-model="text"
          language="en-US"
          :toolbars="[
            'bold',
            'italic',
            'underline',
            'strikeThrough',
            '-',
            'title',
            'quote',
            'unorderedList',
            'orderedList',
            '-',
            'link',
            'image',
            'code',
            'table',
            '-',
            'preview',
            'fullscreen'
          ]"
          preview-theme="default"
          class="min-h-[360px]"
        />
      </div>

      <!-- Action Footer -->
      <div class="mt-6 flex items-center justify-between gap-3 pt-4 border-t border-[var(--color-secondary)]/20">
        <button
          v-if="isEditing"
          type="button"
          @click="resetToOriginal"
          class="px-4 py-2 text-xs sm:text-sm font-semibold text-gray-600 hover:text-[var(--color-dark)] hover:bg-[var(--color-light)] rounded-lg transition"
        >
          Reset Changes
        </button>
        <span v-else class="text-xs text-gray-400 italic">Supports full Markdown syntax</span>

        <button
          type="button"
          :disabled="!isValid"
          @click="handleSubmit"
          class="px-5 py-2.5 bg-[var(--color-primary)] hover:bg-[#4307af] disabled:opacity-50 disabled:cursor-not-allowed text-white font-heading text-xs sm:text-sm font-semibold rounded-lg shadow-sm hover:shadow transition flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <span>{{ isEditing ? 'Update Review' : 'Submit Review' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { MdEditor } from "md-editor-v3";
import "md-editor-v3/lib/style.css";

const props = defineProps({
  movie: {
    type: Object,
    required: false,
    default: null,
  },
});

const emit = defineEmits(["addReview", "updateReview"]);

const defaultPlaceholder = "# Write your review here...\n\nShare your thoughts on the plot, character arcs, and animation quality!";
const text = ref(defaultPlaceholder);

const isEditing = computed(() => Boolean(props.movie && props.movie.review));

const wordCount = computed(() => {
  const clean = text.value.trim();
  return clean ? clean.split(/\s+/).length : 0;
});

const isValid = computed(() => {
  const clean = text.value.trim();
  return clean.length > 0 && clean !== defaultPlaceholder;
});

// Reactively keep in sync if props change asynchronously
watch(
  () => props.movie,
  (newMovie) => {
    if (newMovie && newMovie.review) {
      text.value = newMovie.review;
    } else {
      text.value = defaultPlaceholder;
    }
  },
  { immediate: true }
);

function resetToOriginal() {
  text.value = props.movie?.review || defaultPlaceholder;
}

function handleSubmit() {
  if (!isValid.value) return;

  if (isEditing.value) {
    emit("updateReview", { text: text.value, movieId: props.movie?.id });
  } else {
    emit("addReview", text.value);
  }
}
</script>

<style scoped>
/* Theme overrides for md-editor-v3 */
.custom-editor-wrapper :deep(.md-editor) {
  border: none;
  font-family: var(--font-body), sans-serif;
}

.custom-editor-wrapper :deep(.md-editor-toolbar-wrapper) {
  background-color: var(--color-light);
  border-bottom: 1px solid rgba(182, 176, 159, 0.2);
}

.custom-editor-wrapper :deep(.md-editor-btn:hover) {
  background-color: rgba(84, 9, 218, 0.1);
  color: var(--color-primary);
}
</style>