<template>
  <div class="bg-info">
    <div class="bg-white shadow-lg rounded-lg p-4">
      <div
        class="flex flex-col md:flex-row md:items-center md:justify-between mb-6 mt-12 gap-4"
      >
        <!-- Title & Description Box -->
        <div class="bg-gray-100 rounded-lg p-4 flex-1">
          <h1 class="text-4xl font-bold text-primary mb-2">Dashboard</h1>

          <p class="text-dark leading-relaxed mb-4">
            Welcome to the Dashboard! Here, you can create playlists and manage
            your movie collection.
          </p>
        </div>
        <!-- Buttons Box -->
        <div
          class="bg-gray-50 rounded-lg p-4 flex flex-col md:flex-row items-center gap-2 md:ml-4"
        >
          <button
            @click="showPlaylistForm"
            class="bg-primary text-white px-4 py-2 rounded hover:bg-primary-dark transition mb-6"
          >
            Create Playlist <font-awesome-icon icon="plus" class="text-white" />
          </button>
          <router-link
            to="/users"
            class="bg-secondary text-white px-4 py-2 rounded hover:bg-secondary-dark transition mb-6"
          >
            Explore Users
            <font-awesome-icon icon="user-circle" class="text-white" />
          </router-link>
        </div>
      </div>

      <div class="mt-6">
        <h2 class="text-2xl font-bold mb-4">Your Playlists</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-if="!playlists.length"
            class="col-span-1 sm:col-span-2 md:col-span-3 bg-gray-100 rounded-lg p-6 text-center"
          >
            <p class="text-gray-600">
              No playlists available. Please create one.
            </p>
          </div>
          <div
            v-for="playlist in playlists"
            :key="playlist.id"
            class="bg-white border rounded-lg shadow p-4 flex flex-col"
          >
            <h3 class="text-xl font-semibold mb-2">{{ playlist.name }}</h3>
            <p class="text-gray-600 mb-2">{{ playlist.description }}</p>

            <div class="mt-auto flex justify-end space-x-2">
              <button
                @click="goToDetail(playlist.id)"
                class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition"
              >
                View Details <font-awesome-icon icon="eye" class="text-white" />
              </button>
              <button
                class="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600 transition"
                @click="openEditPlaylistForm(playlist)"
              >
                Edit <font-awesome-icon icon="edit" class="text-white" />
              </button>
              <button
                class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition"
                @click="deletePlaylist(playlist)"
              >
                Delete <font-awesome-icon icon="trash" class="text-white" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-6">
        <h2 class="text-2xl font-bold mb-4">Personal Messages</h2>
        <div
          class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl shadow-lg p-6"
        >
          <p class="text-gray-600 mb-4">
            Below are the recent personal messages.
          </p>
          <div v-if="!messages.length" class="text-center text-gray-500">
            No messages available.
          </div>
          <ul class="divide-y divide-gray-200">
            <li
              v-for="msg in messages"
              :key="msg.id"
              class="py-4 flex items-start space-x-4"
            >
              <div class="flex-shrink-0">
                <span
                  class="inline-flex items-center justify-center h-10 w-10 rounded-full bg-secondary text-primary"
                >
                  <font-awesome-icon icon="clipboard-list" />
                </span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between">
                  <p class="text-lg font-semibold text-blue-800">
                    From {{ msg.username }}
                  </p>
                  <span class="text-xs text-gray-400">
                    {{ formatDate(msg.timestamp) }}
                  </span>
                </div>
                <div class="mt-2">
                  <h3 class="text-lg font-semibold text-primary">
                    {{ msg.title }}
                  </h3>
                  <p class="text-sm text-gray-700">
                    {{ msg.message }}
                  </p>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <div class="mt-6">
        <h2 class="text-2xl font-bold mb-4">Audit Logs</h2>
        <div
          class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl shadow-lg p-6"
        >
          <p class="text-gray-600 mb-4">
            Below are the recent actions performed on your playlists.
          </p>
          <div v-if="!auditLogs.length" class="text-center text-gray-500">
            No audit logs available.
          </div>
          <ul class="divide-y divide-gray-200">
            <li
              v-for="log in auditLogs"
              :key="log.id"
              class="py-4 flex items-start space-x-4"
            >
              <div class="flex-shrink-0">
                <span
                  class="inline-flex items-center justify-center h-10 w-10 rounded-full bg-secondary text-primary"
                >
                  <font-awesome-icon icon="clipboard-list" />
                </span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between">
                  <p class="text-lg font-semibold text-blue-800">
                    {{ log.action }}
                  </p>
                  <span class="text-xs text-gray-400">
                    {{ formatDate(log.timestamp) }}
                  </span>
                </div>
                <pre
                  class="mt-1 text-sm text-gray-700 bg-gray-100 rounded p-2 whitespace-pre-wrap"
                >
                  {{ log.details }}
                </pre>
              </div>
            </li>
          </ul>
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
import dayjs from "dayjs";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import { onMounted, ref, computed } from "vue";
import { useMovieStore } from "../stores/movies";
import { useRoute, useRouter } from "vue-router";
import { useUserStore } from "../stores/users";
import { usePlaylistStore } from "../stores/playlist";
import PlaylistForm from "../components/PlaylistForm.vue";
import Loader from "../components/Loader.vue";

const movieStore = useMovieStore();
const userStore = useUserStore();
const playlistStore = usePlaylistStore();
const router = useRouter();
const isPlaylistFormVisible = ref(false);
const loading = computed(() => movieStore.isLoading);
const selectedTab = ref("topRated");
const selectedPlaylist = ref(null);
const playlists = computed(() => playlistStore.getPlaylists);
const auditLogs = computed(() => playlistStore.getAuditLogs);
const messages = computed(() => userStore.getMessages);

const formatDate = (date) => {
  return dayjs(date).format("MMMM D, YYYY");
};

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

const goToDetail = (playlistId) => {
  router.push({ name: "PlaylistDetail", params: { id: playlistId } });
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
  playlistStore.fetchAuditLogs();
  userStore.getMessagesAction();
});
</script>
