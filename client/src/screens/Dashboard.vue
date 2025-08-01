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
                @click="openEditPlaylistForm(playlist)"
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
                <PlaylistForm
                  @create="createPlaylistUtil"
                  :playlist="selectedPlaylist"
                  @edit="editPlaylistUtil"
                />
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
  DialogTitle,
} from "@headlessui/vue";
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
const selectedPlaylist = ref(null);
const playlists = computed(() => playlistStore.getPlaylists);

const changeTab = (tab) => {
  selectedTab.value = tab;
};

const hidePlaylistForm = () => {
  isPlaylistFormVisible.value = false;
};

const showPlaylistForm = () => {
  selectedPlaylist.value = null; // Reset selected playlist
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

const editPlaylistUtil = async (playlistData) => {
  try {
    await playlistStore.updatePlaylist(selectedPlaylist.value.id, playlistData);
    hidePlaylistForm();
  } catch (error) {
    console.error("Error updating playlist:", error);
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

const openEditPlaylistForm = (playlist) => {
  selectedPlaylist.value = playlist;
  isPlaylistFormVisible.value = true;
};

onMounted(() => {
  playlistStore.fetchPlaylists();
});
</script>
