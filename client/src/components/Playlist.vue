<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Playlists</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <div
        v-for="playlist in playlists"
        :key="playlist.id"
        class="bg-white rounded-lg shadow p-6 flex flex-col justify-between"
      >
        <div>
          <h3 class="text-lg font-semibold mb-2">{{ playlist.name }}</h3>
          <p class="text-gray-600 mb-4">{{ playlist.description }}</p>
        </div>
        <button
          class="mt-auto px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
          Select Playlist
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Playlist",
  props: {
    playlists: {
      type: Array,
      required: true,
    },
  },
};
</script>
