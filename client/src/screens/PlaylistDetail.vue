<template>
  <div class="bg-info">
    <div class="bg-white shadow-lg rounded-lg p-4">
      <h1 class="text-4xl font-bold text-primary text-center mb-4 mt-16">
        {{ playlist?.name || "Playlist Detail" }}
      </h1>
      <p class="text-dark leading-relaxed mb-4">
        {{ playlist?.description }}
      </p>

      <div class="flex justify-end space-x-2 mb-6">
        <button
          class="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600 transition"
          @click="openEditPlaylistForm"
        >
          Edit
        </button>
        <button
          class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition"
          @click="deletePlaylist"
        >
          Delete
        </button>
      </div>

      <div class="mt-6">
        <h2 class="text-2xl font-bold mb-4">Movies in this Playlist</h2>
        <div v-if="playlist?.movies?.length">
          <ul>
            <li
              v-for="movie in playlist.movies"
              :key="movie.id"
              class="mb-2 p-2 border rounded"
            >
              {{ movie.title }}
            </li>
          </ul>
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
const loading = computed(() => playlistStore.isLoading);
const playlist = ref(null);

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

const deletePlaylist = async () => {
  try {
    await playlistStore.deletePlaylist(playlist.value.id);
    router.push("/playlists");
  } catch (error) {
    console.error("Error deleting playlist:", error);
  }
};

onMounted(() => {
  fetchPlaylist();
});
</script>
