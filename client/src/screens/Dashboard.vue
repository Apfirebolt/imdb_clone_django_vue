<template>
  <div class="bg-info flex items-center justify-center">
    <div class="bg-white shadow-lg rounded-lg p-4">
      <h1 class="text-4xl font-bold text-primary text-center mb-4 mt-16">
        Dashboard
      </h1>
      <p class="text-dark leading-relaxed mb-4">
        Welcome to the Dashboard! Here, you can create playlists and manage your
        movie collection.
      </p>

      <PlaylistForm v-if="isPlaylistFormVisible" @close="hidePlaylistForm" />
      <button
        @click="showPlaylistForm"
        class="bg-primary text-white px-4 py-2 rounded hover:bg-primary-dark transition mb-6"
      >
        Create Playlist
      </button>
    </div>

    <Loader v-if="loading" />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useMovieStore } from "../stores/movies";
import { usePlaylistStore } from "../stores/playlist";
import axios from "axios";
import PlaylistForm from "../components/PlaylistForm.vue";
import Loader from "../components/Loader.vue";

const movieStore = useMovieStore();
const playlistStore = usePlaylistStore();
const isPlaylistFormVisible = ref(false);
const loading = computed(() => movieStore.isLoading);
const selectedTab = ref("topRated");

const changeTab = (tab) => {
  selectedTab.value = tab;
};

const hidePlaylistForm = () => {
  isPlaylistFormVisible.value = false;
};

const showPlaylistForm = () => {
  isPlaylistFormVisible.value = true;
};

onMounted(() => {});
</script>
