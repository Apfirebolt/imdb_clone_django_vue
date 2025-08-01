<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Playlists</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <div
        v-for="playlist in playlists"
        :key="playlist.id"
        :class="[
          'bg-white rounded-lg shadow p-6 flex flex-col justify-between',
          selectedPlaylist && playlist.id === selectedPlaylist.id
            ? 'border-4 border-blue-600'
            : '',
        ]"
      >
        <div>
          <h3 class="text-lg font-semibold mb-2">{{ playlist.name }}</h3>
          <p class="text-gray-600 mb-4">{{ playlist.description }}</p>
        </div>
        <button
          @click="handleSelect(playlist)"
          class="mt-auto px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
          Select Playlist
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineEmits, defineProps } from "vue";

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

function handleSelect(playlist) {
  emit("choosePlaylist", playlist);
}
</script>
