<template>
  <div class="w-full max-w-lg mx-auto font-body">
    <form
      @submit.prevent="submitForm"
      class="rounded-2xl border border-[var(--color-secondary)]/30 bg-white p-6 sm:p-8 shadow-sm backdrop-blur-sm space-y-6"
    >
      <!-- Header -->
      <div class="space-y-1 pb-4 border-b border-[var(--color-secondary)]/20">
        <div class="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-[var(--color-tertiary)] font-display">
          <span>✦</span>
          <span>Collection Manager</span>
        </div>
        <h2 class="text-xl sm:text-2xl font-bold font-heading text-[var(--color-dark)] tracking-tight m-0">
          {{ isEditing ? 'Edit Playlist' : 'Create New Playlist' }}
        </h2>
        <p class="text-xs text-gray-500">
          {{ isEditing ? 'Update your curated collection details below.' : 'Organize your favorite series and watch queues into a themed group.' }}
        </p>
      </div>

      <!-- Form Fields -->
      <div class="space-y-4">
        <!-- Name Field -->
        <div>
          <label for="name" class="block text-xs font-semibold text-[var(--color-dark)] mb-1.5 font-heading">
            Playlist Name <span class="text-[var(--color-danger)]">*</span>
          </label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            required
            maxlength="80"
            placeholder="e.g. Cozy Slice of Life & Fantasy"
            class="w-full px-3.5 py-2.5 rounded-lg text-sm bg-[var(--color-light)] border border-[var(--color-secondary)]/40 text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition"
          />
          <div class="flex justify-between items-center mt-1 text-[11px] text-gray-500">
            <span>Give your collection a descriptive title</span>
            <span :class="form.name.length >= 80 ? 'text-[var(--color-danger)] font-semibold' : ''">
              {{ form.name.length }}/80
            </span>
          </div>
        </div>

        <!-- Description Field -->
        <div>
          <label for="description" class="block text-xs font-semibold text-[var(--color-dark)] mb-1.5 font-heading">
            Description <span class="text-[var(--color-danger)]">*</span>
          </label>
          <textarea
            id="description"
            v-model="form.description"
            rows="4"
            required
            maxlength="250"
            placeholder="What kind of anime belongs in this playlist? Add themes, mood notes, or watching guidelines..."
            class="w-full px-3.5 py-2.5 rounded-lg text-sm bg-[var(--color-light)] border border-[var(--color-secondary)]/40 text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition resize-y"
          ></textarea>
          <div class="flex justify-between items-center mt-1 text-[11px] text-gray-500">
            <span>Shown on the lounge public card</span>
            <span :class="form.description.length >= 250 ? 'text-[var(--color-danger)] font-semibold' : ''">
              {{ form.description.length }}/250
            </span>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="pt-2 flex items-center justify-end gap-3 border-t border-[var(--color-secondary)]/20">
        <button
          v-if="isEditing"
          type="button"
          @click="resetForm"
          class="px-4 py-2.5 text-xs font-semibold rounded-lg text-gray-600 hover:text-[var(--color-dark)] hover:bg-[var(--color-light)] border border-[var(--color-secondary)]/30 transition cursor-pointer font-heading"
        >
          Cancel
        </button>

        <button
          type="submit"
          class="px-5 py-2.5 rounded-lg bg-[var(--color-primary)] hover:bg-[#4307af] text-white text-xs sm:text-sm font-semibold transition shadow-sm hover:shadow flex items-center justify-center gap-2 cursor-pointer font-heading"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <span>{{ isEditing ? 'Save Changes' : 'Create Collection' }}</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, computed, watch } from "vue";

const emit = defineEmits(["create", "edit", "cancel"]);

const props = defineProps({
  playlist: {
    type: Object,
    default: () => ({}),
  },
});

const isEditing = computed(() => Boolean(props.playlist && props.playlist.id));

const form = reactive({
  name: "",
  description: "",
});

watch(
  () => props.playlist,
  (newVal) => {
    if (newVal && newVal.id) {
      form.name = newVal.name || "";
      form.description = newVal.description || "";
    } else {
      form.name = "";
      form.description = "";
    }
  },
  { immediate: true, deep: true }
);

function resetForm() {
  form.name = "";
  form.description = "";
  emit("cancel");
}

function submitForm() {
  const trimmedName = form.name.trim();
  const trimmedDesc = form.description.trim();

  if (!trimmedName || !trimmedDesc) return;

  if (isEditing.value) {
    emit("edit", {
      ...form,
      name: trimmedName,
      description: trimmedDesc,
      id: props.playlist.id,
    });
  } else {
    emit("create", {
      name: trimmedName,
      description: trimmedDesc,
    });
    form.name = "";
    form.description = "";
  }
}
</script>