<template>
  <div class="w-full space-y-6">
    <!-- Section Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-4 border-b border-[var(--border)]">
      <div>
        <h2 class="text-2xl font-bold font-heading text-[var(--text-h)] tracking-tight">
          Your Playlists
        </h2>
        <p class="text-xs text-[var(--text)] mt-0.5">
          Curate, organize, and stream your custom anime queues.
        </p>
      </div>
      
      <div v-if="playlists.length" class="text-xs font-medium text-[var(--text)]">
        Showing <span class="text-[var(--text-h)] font-semibold">{{ playlists.length }}</span> {{ playlists.length === 1 ? 'collection' : 'collections' }}
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-if="!playlists.length"
      class="rounded-2xl border-2 border-dashed border-[var(--border)] bg-[var(--code-bg)]/30 p-12 text-center flex flex-col items-center justify-center gap-3"
    >
      <div class="w-12 h-12 rounded-full bg-brand-primary/10 text-brand-primary flex items-center justify-center text-xl">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      </div>
      <div class="space-y-1">
        <h3 class="text-base font-semibold font-heading text-[var(--text-h)]">No playlists found</h3>
        <p class="text-xs text-[var(--text)] max-w-sm">
          You haven't compiled any anime into playlists yet. Create one to keep track of marathons and recommendations.
        </p>
      </div>
    </div>

    <!-- Grid of Playlists -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <div
        v-for="playlist in playlists"
        :key="playlist.id"
        @click="handleSelect(playlist)"
        :class="[
          'group relative flex flex-col justify-between rounded-xl border p-5 transition-all duration-200 cursor-pointer text-left',
          isSelected(playlist)
            ? 'border-brand-primary bg-brand-primary/5 ring-2 ring-brand-primary/20 shadow-md'
            : 'border-[var(--border)] bg-[var(--code-bg)]/30 hover:border-brand-primary/40 hover:bg-[var(--code-bg)]/60 hover:shadow-sm'
        ]"
      >
        <!-- Top Row: Icon + Selection Badge -->
        <div class="flex items-start justify-between gap-3 mb-4">
          <div class="w-10 h-10 rounded-lg bg-[var(--bg)] border border-[var(--border)] flex items-center justify-center text-brand-primary shadow-xs group-hover:border-brand-primary/40 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
            </svg>
          </div>

          <!-- Active Indicator Pill -->
          <span
            v-if="isSelected(playlist)"
            class="inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded-full bg-brand-primary text-white"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
            </svg>
            Active
          </span>
          <span
            v-else
            class="text-[11px] font-medium text-[var(--text)] opacity-0 group-hover:opacity-100 transition-opacity"
          >
            Click to select
          </span>
        </div>

        <!-- Content Info -->
        <div class="space-y-1.5 flex-1">
          <h3 class="font-heading font-semibold text-base text-[var(--text-h)] group-hover:text-brand-primary transition-colors line-clamp-1">
            {{ playlist.name }}
          </h3>
          <p class="text-xs text-[var(--text)] line-clamp-2 leading-relaxed">
            {{ playlist.description || 'No description provided for this collection.' }}
          </p>
        </div>

        <!-- Bottom Action / Meta -->
        <div class="mt-5 pt-3.5 border-t border-[var(--border)]/70 flex items-center justify-between">
          <span class="text-[11px] text-[var(--text)] flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-brand-secondary"></span>
            {{ playlist.itemCount ?? (playlist.anime?.length ?? 0) }} Titles
          </span>

          <button
            type="button"
            class="text-xs font-semibold px-3 py-1.5 rounded-lg transition-all"
            :class="[
              isSelected(playlist)
                ? 'bg-brand-primary text-white shadow-xs'
                : 'text-brand-primary hover:bg-brand-primary/10'
            ]"
            @click.stop="handleSelect(playlist)"
          >
            {{ isSelected(playlist) ? 'Selected' : 'Select' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  playlists: {
    type: Array,
    required: true,
  },
  selectedPlaylist: {
    type: Object,
    required: false,
    default: null,
  },
});

const emit = defineEmits(["choosePlaylist"]);

function isSelected(playlist) {
  return props.selectedPlaylist && playlist.id === props.selectedPlaylist.id;
}

function handleSelect(playlist) {
  emit("choosePlaylist", playlist);
}
</script>