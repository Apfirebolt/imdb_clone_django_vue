<template>
  <div class="bg-info">
    <div class="bg-white shadow-lg rounded-lg p-4">
      <h1 class="text-4xl font-bold text-primary text-center mb-4 mt-16">
        Dashboard
      </h1>
      <p class="text-dark leading-relaxed mb-4">
        Welcome to the Dashboard! Here, you can create playlists and manage your
        movie collection.
      </p>

      <PlaylistForm v-if="isPlaylistFormVisible" @close="hidePlaylistForm" @create="createPlaylistUtil" />
      <button
        @click="showPlaylistForm"
        class="bg-primary text-white px-4 py-2 rounded hover:bg-primary-dark transition mb-6"
      >
        Create Playlist
      </button>

      <div class="mt-6">
        <h2 class="text-2xl font-bold mb-4">Your Playlists</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
                v-for="playlist in playlists"
                :key="playlist.id"
                class="bg-white border rounded-lg shadow p-4 flex flex-col"
            >
                <h3 class="text-xl font-semibold mb-2">{{ playlist.name }}</h3>
                <p class="text-gray-600 mb-2">{{ playlist.description }}</p>

                <div class="mt-auto flex justify-end space-x-2">
                    <button
                        class="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600 transition"
                        @click="$emit('edit', playlist)"
                    >
                        Edit
                    </button>
                    <button
                        class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition"
                        @click="deletePlaylist(playlist)"
                    >
                        Delete
                    </button>
                </div>
            </div>
        </div>
      </div>
    </div>

    

    <Loader v-if="loading" />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useMovieStore } from "../stores/movies";
import { usePlaylistStore } from "../stores/playlist";
import PlaylistForm from "../components/PlaylistForm.vue";
import Loader from "../components/Loader.vue";

const movieStore = useMovieStore();
const playlistStore = usePlaylistStore();
const isPlaylistFormVisible = ref(false);
const loading = computed(() => movieStore.isLoading);
const selectedTab = ref("topRated");
const playlists = computed(() => playlistStore.getPlaylists);

const changeTab = (tab) => {
  selectedTab.value = tab;
};

const hidePlaylistForm = () => {
  isPlaylistFormVisible.value = false;
};

const showPlaylistForm = () => {
  isPlaylistFormVisible.value = true;
};

const createPlaylistUtil = async (playlistData) => {
  try {
    await playlistStore.createPlaylist(playlistData);
    await playlistStore.fetchPlaylists();
    hidePlaylistForm();
  } catch (error) {
    console.error("Error creating playlist:", error);
  }
};

const deletePlaylist = async (playlist) => {
  try {
    await playlistStore.deletePlaylist(playlist.id);
    await playlistStore.fetchPlaylists();
  } catch (error) {
    console.error("Error deleting playlist:", error);
  }
};

onMounted(() => {
    playlistStore.fetchPlaylists();
});
</script>
