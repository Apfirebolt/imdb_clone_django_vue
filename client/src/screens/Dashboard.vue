<template>
  <div class="min-h-screen bg-[#f8fafc] text-[var(--color-dark)] font-body py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto space-y-10">

      <!-- Hero Header Section -->
      <section class="rounded-2xl border border-[var(--color-secondary)]/30 bg-white p-6 sm:p-8 shadow-xs">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          <div class="space-y-2 max-w-2xl">
            <span class="text-xs font-bold uppercase tracking-wider text-[var(--color-tertiary)] font-display">
              Control Panel
            </span>
            <h1 class="text-3xl sm:text-4xl font-bold font-heading text-[var(--color-dark)] tracking-tight m-0">
              Dashboard
            </h1>
            <p class="text-sm text-gray-600 leading-relaxed m-0">
              Manage your curated anime watch queues, review activity audits, and view messages from the community.
            </p>
          </div>

          <!-- Quick Action Controls -->
          <div class="flex flex-wrap items-center gap-3">
            <button
              @click="showPlaylistForm"
              class="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-[var(--color-primary)] hover:bg-[#4307af] text-white font-heading text-xs sm:text-sm font-semibold transition shadow-xs hover:shadow cursor-pointer"
            >
              <font-awesome-icon icon="plus" class="text-xs" />
              <span>Create Playlist</span>
            </button>
            <router-link
              to="/users"
              class="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-[var(--color-light)] hover:bg-gray-200/70 text-[var(--color-dark)] border border-[var(--color-secondary)]/30 font-heading text-xs sm:text-sm font-semibold transition cursor-pointer"
            >
              <font-awesome-icon icon="user-circle" class="text-sm text-gray-500" />
              <span>Explore Users</span>
            </router-link>
          </div>
        </div>
      </section>

      <!-- Playlists Grid -->
      <section class="space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-[var(--color-secondary)]/20">
          <div>
            <h2 class="text-xl sm:text-2xl font-bold font-heading text-[var(--color-dark)] m-0">
              Your Playlists
            </h2>
            <p class="text-xs text-gray-500 mt-0.5">
              Curated collections created by your profile
            </p>
          </div>
          <span v-if="playlists.length" class="text-xs font-semibold px-2.5 py-1 rounded-full bg-[var(--color-light)] border border-[var(--color-secondary)]/20 text-gray-600">
            {{ playlists.length }} {{ playlists.length === 1 ? 'Playlist' : 'Playlists' }}
          </span>
        </div>

        <!-- Empty State -->
        <div
          v-if="!playlists.length"
          class="rounded-2xl border-2 border-dashed border-[var(--color-secondary)]/40 bg-white p-12 text-center flex flex-col items-center justify-center gap-3"
        >
          <div class="w-12 h-12 rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)] flex items-center justify-center text-lg">
            <font-awesome-icon icon="clipboard-list" />
          </div>
          <div class="space-y-1">
            <h3 class="text-base font-semibold font-heading text-[var(--color-dark)] m-0">No playlists yet</h3>
            <p class="text-xs text-gray-500 max-w-sm m-0">
              Organize your shows into marathons, themes, or recommendations.
            </p>
          </div>
          <button
            @click="showPlaylistForm"
            class="mt-2 text-xs font-semibold text-[var(--color-primary)] hover:underline"
          >
            + Create your first playlist
          </button>
        </div>

        <!-- Playlists List -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          <div
            v-for="playlist in playlists"
            :key="playlist.id"
            class="group rounded-xl border border-[var(--color-secondary)]/30 bg-white p-5 flex flex-col justify-between hover:border-[var(--color-primary)]/40 hover:shadow-xs transition"
          >
            <div class="space-y-2">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-base font-bold font-heading text-[var(--color-dark)] group-hover:text-[var(--color-primary)] transition-colors line-clamp-1 m-0">
                  {{ playlist.name }}
                </h3>
                <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-[var(--color-light)] text-gray-600 border border-[var(--color-secondary)]/20">
                  Active
                </span>
              </div>
              <p class="text-xs text-gray-600 line-clamp-2 leading-relaxed m-0">
                {{ playlist.description || "No description provided." }}
              </p>
            </div>

            <!-- Card Controls -->
            <div class="mt-6 pt-4 border-t border-[var(--color-secondary)]/20 flex items-center justify-end gap-1.5">
              <button
                @click="goToDetail(playlist.id)"
                class="px-2.5 py-1.5 rounded-md text-xs font-semibold text-gray-700 hover:bg-[var(--color-light)] hover:text-[var(--color-dark)] transition inline-flex items-center gap-1.5 cursor-pointer"
                title="View details"
              >
                <font-awesome-icon icon="eye" class="text-gray-400" />
                <span>View</span>
              </button>
              <button
                @click="openEditPlaylistForm(playlist)"
                class="px-2.5 py-1.5 rounded-md text-xs font-semibold text-gray-700 hover:bg-[var(--color-light)] hover:text-[var(--color-dark)] transition inline-flex items-center gap-1.5 cursor-pointer"
                title="Edit playlist"
              >
                <font-awesome-icon icon="edit" class="text-gray-400" />
                <span>Edit</span>
              </button>
              <button
                @click="deletePlaylist(playlist)"
                class="px-2.5 py-1.5 rounded-md text-xs font-semibold text-[var(--color-danger)] hover:bg-red-50 transition inline-flex items-center gap-1.5 cursor-pointer"
                title="Delete playlist"
              >
                <font-awesome-icon icon="trash" class="text-xs" />
                <span>Delete</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Bottom Layout: Personal Messages & Audit Logs Side-by-Side -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">

        <!-- Personal Messages -->
        <section class="rounded-2xl border border-[var(--color-secondary)]/30 bg-white p-6 shadow-xs space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-[var(--color-secondary)]/20">
            <div>
              <h2 class="text-lg sm:text-xl font-bold font-heading text-[var(--color-dark)] m-0">
                Personal Messages
              </h2>
              <p class="text-xs text-gray-500 mt-0.5">Inbox notifications from fellow members</p>
            </div>
            <span v-if="messages.length" class="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-[var(--color-tertiary)]/10 text-[var(--color-tertiary)]">
              {{ messages.length }}
            </span>
          </div>

          <div v-if="!messages.length" class="py-8 text-center text-xs text-gray-500">
            No incoming messages available.
          </div>

          <ul v-else class="divide-y divide-[var(--color-secondary)]/20">
            <li
              v-for="msg in messages"
              :key="msg.id"
              class="py-3.5 first:pt-0 last:pb-0 flex items-start gap-3.5"
            >
              <div class="flex-shrink-0 w-8 h-8 rounded-full bg-[var(--color-light)] border border-[var(--color-secondary)]/30 text-[var(--color-primary)] flex items-center justify-center text-xs">
                <font-awesome-icon icon="clipboard-list" />
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between gap-2">
                  <span class="text-xs font-semibold text-[var(--color-dark)] truncate">
                    @{{ msg.username }}
                  </span>
                  <span class="text-[11px] text-gray-400 flex-shrink-0">
                    {{ formatDate(msg.timestamp) }}
                  </span>
                </div>
                <h3 class="text-xs font-bold text-[var(--color-primary)] mt-1 mb-0.5 truncate font-heading">
                  {{ msg.title }}
                </h3>
                <p class="text-xs text-gray-600 line-clamp-2 leading-relaxed m-0">
                  {{ msg.message }}
                </p>
              </div>
            </li>
          </ul>
        </section>

        <!-- Audit Logs -->
        <section class="rounded-2xl border border-[var(--color-secondary)]/30 bg-white p-6 shadow-xs space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-[var(--color-secondary)]/20">
            <div>
              <h2 class="text-lg sm:text-xl font-bold font-heading text-[var(--color-dark)] m-0">
                Audit Logs
              </h2>
              <p class="text-xs text-gray-500 mt-0.5">Recent account actions and playlist updates</p>
            </div>
          </div>

          <div v-if="!auditLogs.length" class="py-8 text-center text-xs text-gray-500">
            No recent activity recorded.
          </div>

          <ul v-else class="divide-y divide-[var(--color-secondary)]/20">
            <li
              v-for="log in auditLogs"
              :key="log.id"
              class="py-3.5 first:pt-0 last:pb-0 flex items-start gap-3.5"
            >
              <div class="flex-shrink-0 w-8 h-8 rounded-full bg-[var(--color-light)] border border-[var(--color-secondary)]/30 text-gray-500 flex items-center justify-center text-xs">
                <font-awesome-icon icon="clipboard-list" />
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between gap-2">
                  <span class="text-xs font-semibold text-[var(--color-dark)] font-heading">
                    {{ log.action }}
                  </span>
                  <span class="text-[11px] text-gray-400 flex-shrink-0">
                    {{ formatDate(log.timestamp) }}
                  </span>
                </div>
                <div
                  v-if="log.details"
                  class="mt-1 text-[11px] text-gray-600 bg-[var(--color-light)] border border-[var(--color-secondary)]/20 rounded p-2 font-mono whitespace-pre-wrap break-all"
                >
                  {{ log.details }}
                </div>
              </div>
            </li>
          </ul>
        </section>

      </div>
    </div>

    <!-- Loader -->
    <Loader v-if="loading" />

    <!-- HeadlessUI Modal for Playlist Creation/Editing -->
    <TransitionRoot appear :show="isPlaylistFormVisible" as="template">
      <Dialog as="div" @close="hidePlaylistForm" class="relative z-50 font-body">
        <TransitionChild
          as="template"
          enter="duration-200 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-150 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black/40 backdrop-blur-xs" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              enter="duration-200 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-150 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-lg transform overflow-hidden transition-all text-left">
                <PlaylistForm
                  :playlist="selectedPlaylist"
                  @create="createPlaylistUtil"
                  @edit="editPlaylistUtil"
                  @cancel="hidePlaylistForm"
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
} from "@headlessui/vue";
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useMovieStore } from "../stores/movies";
import { useUserStore } from "../stores/users";
import { usePlaylistStore } from "../stores/playlist";
import PlaylistForm from "../components/PlaylistForm.vue";
import Loader from "../components/Loader.vue";

const movieStore = useMovieStore();
const userStore = useUserStore();
const playlistStore = usePlaylistStore();
const router = useRouter();

const isPlaylistFormVisible = ref(false);
const selectedPlaylist = ref(null);

const loading = computed(() => movieStore.isLoading);
const playlists = computed(() => playlistStore.getPlaylists || []);
const auditLogs = computed(() => playlistStore.getAuditLogs || []);
const messages = computed(() => userStore.getMessages || []);

const formatDate = (date) => {
  if (!date) return "";
  return dayjs(date).format("MMM D, YYYY");
};

const hidePlaylistForm = () => {
  isPlaylistFormVisible.value = false;
  selectedPlaylist.value = null;
};

const showPlaylistForm = () => {
  selectedPlaylist.value = null;
  isPlaylistFormVisible.value = true;
};

const openEditPlaylistForm = (playlist) => {
  selectedPlaylist.value = playlist;
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
    await playlistStore.fetchPlaylists();
    hidePlaylistForm();
  } catch (error) {
    console.error("Error updating playlist:", error);
  }
};

const deletePlaylist = async (playlist) => {
  if (!confirm(`Are you sure you want to delete "${playlist.name}"?`)) return;
  try {
    await playlistStore.deletePlaylist(playlist.id);
    await playlistStore.fetchPlaylists();
  } catch (error) {
    console.error("Error deleting playlist:", error);
  }
};

onMounted(() => {
  playlistStore.fetchPlaylists();
  playlistStore.fetchAuditLogs();
  userStore.getMessagesAction();
});
</script>