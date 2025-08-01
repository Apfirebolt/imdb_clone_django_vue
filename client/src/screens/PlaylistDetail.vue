<template>
  <div class="bg-info">
    <div class="bg-white shadow-lg rounded-lg p-4">
      <div
        class="flex flex-col md:flex-row md:items-center md:justify-between mb-6 mt-12 gap-4"
      >
        <!-- Title & Description Box -->
        <div class="bg-gray-100 rounded-lg p-4 flex-1">
          <h1 class="text-4xl font-bold text-primary mb-2">
            {{ playlist?.name || "Playlist Detail" }}
          </h1>
          <p class="text-dark leading-relaxed">
            {{ playlist?.description }}
          </p>
        </div>
        <!-- Buttons Box -->
        <div
          class="bg-gray-50 rounded-lg p-4 flex flex-col md:flex-row items-center gap-2 md:ml-4"
        >
          <button
            class="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600 transition w-full md:w-auto"
            @click="openEditPlaylistForm"
          >
            Edit
          </button>
          <button
            class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition w-full md:w-auto"
            @click="deletePlaylist"
          >
            Delete
          </button>
        </div>
      </div>

      <div class="mt-6">
        <h2 class="text-2xl font-bold mb-4">Movies in this Playlist</h2>
        <div v-if="playlist?.movies?.length">
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            <div
              v-for="movie in playlist.movies"
              :key="movie.id"
              class="bg-white rounded shadow p-4 flex flex-col items-center"
            >
              <img
                v-if="movie.primary_image"
                :src="movie.primary_image"
                :alt="movie.title"
                class="w-32 h-48 object-cover rounded mb-3"
              />
              <div class="text-center">
                <h3 class="text-lg font-semibold mb-1">{{ movie.title }}</h3>
                <p class="text-gray-600 text-sm mb-2 line-clamp-3">
                  {{ movie.description }}
                </p>
                <span
                  class="inline-block bg-blue-100 text-blue-800 mx-2 text-xs px-2 py-1 rounded mb-1"
                  v-for="genre in movie.genres"
                  :key="genre"
                >
                  {{ genre }}
                </span>
                <div class="text-xs text-gray-500 mt-2">
                  Released: {{ movie.release_date }}
                </div>
                <button
                  class="mt-2 bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600 transition"
                  @click="removeMovie(movie.id)"
                >
                  Remove Movie
                </button>
              </div>
            </div>
          </div>
        </div>
        <div v-else>
          <p class="text-gray-600">No movies in this playlist.</p>
        </div>
      </div>
    </div>

    <Loader v-if="loading" />
    <TransitionRoot appear :show="isPlaylistFormVisible" as="template">
      <Dialog as="div" @close="hidePlaylistForm" class="relative z-10">
        <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black/25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div
            class="flex min-h-full items-center justify-center p-4 text-center"
          >
            <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel
                class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
              >
                <PlaylistForm :playlist="playlist" @edit="editPlaylistUtil" />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
} from "@headlessui/vue";
import { onMounted, ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { usePlaylistStore } from "../stores/playlist";
import PlaylistForm from "../components/PlaylistForm.vue";
import Loader from "../components/Loader.vue";

const route = useRoute();
const router = useRouter();
const playlistStore = usePlaylistStore();
const isPlaylistFormVisible = ref(false);
const playlist = computed(() => playlistStore.getPlaylist);
const loading = computed(() => playlistStore.isLoading);

const fetchPlaylist = async () => {
  try {
    await playlistStore.fetchPlaylists();
    playlist.value = playlistStore.getPlaylists.find(
      (p) => p.id === Number(route.params.id)
    );
  } catch (error) {
    console.error("Error fetching playlist:", error);
  }
};

const hidePlaylistForm = () => {
  isPlaylistFormVisible.value = false;
};

const openEditPlaylistForm = () => {
  isPlaylistFormVisible.value = true;
};

const editPlaylistUtil = async (playlistData) => {
  try {
    await playlistStore.updatePlaylist(playlist.value.id, playlistData);
    await fetchPlaylist();
    hidePlaylistForm();
  } catch (error) {
    console.error("Error updating playlist:", error);
  }
};

const removeMovie = async (movieId) => {
  try {
    await playlistStore.removeMovieFromPlaylist(playlist.value.id, movieId);
    await getPlaylistById();
  } catch (error) {
    console.error("Error removing movie from playlist:", error);
  }
};

const deletePlaylist = async () => {
  try {
    await playlistStore.deletePlaylist(playlist.value.id);
    router.push("/playlists");
  } catch (error) {
    console.error("Error deleting playlist:", error);
  }
};

const getPlaylistById = async () => {
  try {
    const id = Number(route.params.id);
    await playlistStore.getPlaylistById(id);
  } catch (error) {
    console.error("Error fetching playlist by ID:", error);
  }
};

onMounted(() => {
  getPlaylistById();
});
</script>
