<template>
  <div class="min-h-screen bg-[var(--color-light)] text-[var(--color-dark)] font-body py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto space-y-8">
      
      <!-- Back Navigation & Action Bar -->
      <div class="flex items-center justify-between">
        <router-link
          to="/users"
          class="inline-flex items-center gap-2 text-xs font-semibold text-gray-600 hover:text-[var(--color-dark)] transition font-heading"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          <span>Back to Member Directory</span>
        </router-link>

        <span
          v-if="user"
          class="text-[11px] font-semibold uppercase tracking-wider px-2.5 py-0.5 rounded-full border"
          :class="isUserLocked
            ? 'bg-amber-50 text-amber-700 border-amber-200'
            : 'bg-emerald-50 text-emerald-700 border-emerald-200'"
        >
          {{ isUserLocked ? 'Private Account' : 'Active Public Account' }}
        </span>
      </div>

      <!-- Main Profile Card -->
      <section
        v-if="user"
        class="rounded-2xl border border-[var(--color-secondary)]/30 bg-white shadow-xs overflow-hidden"
      >
        <!-- Top Banner / Accent Strip -->
        <div class="h-28 bg-gradient-to-r from-[var(--color-primary)] via-[#6b16ea] to-[var(--color-ter)] relative"></div>

        <div class="px-6 sm:px-8 pb-8 pt-0 relative">
          <!-- Avatar + Actions Row -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4 -mt-14 mb-6">
            <div class="flex items-end gap-4">
              <div class="w-24 h-24 sm:w-28 sm:h-28 rounded-2xl border-4 border-white bg-gradient-to-tr from-[var(--color-primary)] to-[var(--color-ter)] text-white flex items-center justify-center font-heading font-bold text-3xl shadow-sm overflow-hidden shrink-0">
                <img
                  v-if="user.profile_picture"
                  :src="user.profile_picture"
                  :alt="user.username"
                  class="w-full h-full object-cover"
                />
                <span v-else>{{ userInitials }}</span>
              </div>

              <div class="space-y-0.5 pb-1">
                <h1 class="text-2xl sm:text-3xl font-bold font-heading text-[var(--color-dark)] tracking-tight m-0">
                  {{ user.username }}
                </h1>
                <p v-if="user.first_name || user.last_name" class="text-xs sm:text-sm text-gray-500 m-0">
                  {{ user.first_name }} {{ user.last_name }}
                </p>
              </div>
            </div>

            <!-- Direct Action Button -->
            <div class="self-start sm:self-end">
              <button
                v-if="!isUserLocked"
                type="button"
                @click="openMessageForm(user)"
                class="px-5 py-2 rounded-lg bg-[var(--color-primary)] hover:bg-[#4307af] text-white text-xs sm:text-sm font-semibold font-heading shadow-xs hover:shadow transition flex items-center gap-2 cursor-pointer"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                <span>Send Message</span>
              </button>
            </div>
          </div>

          <!-- Metadata Summary Strip -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 p-4 rounded-xl bg-[var(--color-light)] border border-[var(--color-secondary)]/20 text-xs">
            <div>
              <span class="text-gray-500 block">Email Address</span>
              <span class="font-semibold text-[var(--color-dark)] truncate block mt-0.5">{{ user.email }}</span>
            </div>
            <div>
              <span class="text-gray-500 block">Lounge Member Since</span>
              <span class="font-semibold text-[var(--color-dark)] block mt-0.5">{{ formatDate(user.date_joined) }}</span>
            </div>
            <div>
              <span class="text-gray-500 block">Profile Visibility</span>
              <span class="font-semibold block mt-0.5" :class="isUserLocked ? 'text-amber-700' : 'text-emerald-700'">
                {{ isUserLocked ? 'Private Mode' : 'Public Directory' }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Private Profile Notice -->
      <div
        v-if="user && isUserLocked"
        class="rounded-2xl border border-amber-200 bg-amber-50/70 p-8 text-center space-y-3"
      >
        <div class="w-12 h-12 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center mx-auto text-xl">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <h3 class="text-base font-bold font-heading text-amber-900 m-0">
          This Profile is Locked
        </h3>
        <p class="text-xs text-amber-800/80 max-w-md mx-auto leading-relaxed m-0">
          {{ user.username }} has set their account to private mode. Their curated watchlists and direct messages are restricted.
        </p>
      </div>

      <!-- Public Playlists Section -->
      <section
        v-if="user && !isUserLocked"
        class="space-y-4"
      >
        <div class="flex items-center justify-between pb-3 border-b border-[var(--color-secondary)]/20">
          <div>
            <h2 class="text-xl font-bold font-heading text-[var(--color-dark)] m-0">
              Curated Playlists
            </h2>
            <p class="text-xs text-gray-500 mt-0.5">
              Public anime watch queues created by {{ user.username }}
            </p>
          </div>
          <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-white border border-[var(--color-secondary)]/30 text-gray-600">
            {{ userPlaylists.length }} {{ userPlaylists.length === 1 ? 'Collection' : 'Collections' }}
          </span>
        </div>

        <!-- Empty Playlists -->
        <div
          v-if="!userPlaylists.length"
          class="rounded-2xl border-2 border-dashed border-[var(--color-secondary)]/40 bg-white p-10 text-center space-y-2"
        >
          <p class="text-xs text-gray-500 m-0">
            This user has not published any public playlists yet.
          </p>
        </div>

        <!-- Playlists Grid -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div
            v-for="playlist in userPlaylists"
            :key="playlist.id"
            class="group rounded-xl border border-[var(--color-secondary)]/30 bg-white p-5 flex flex-col justify-between hover:border-[var(--color-primary)]/50 hover:shadow-sm transition"
          >
            <div class="space-y-2">
              <div class="flex items-start justify-between gap-2">
                <h3 class="text-base font-bold font-heading text-[var(--color-dark)] group-hover:text-[var(--color-primary)] transition truncate m-0">
                  {{ playlist.name }}
                </h3>
                <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-[var(--color-light)] text-gray-600 border border-[var(--color-secondary)]/20 shrink-0">
                  Queue
                </span>
              </div>
              <p class="text-xs text-gray-600 line-clamp-2 leading-relaxed m-0">
                {{ playlist.description || "No description provided for this collection." }}
              </p>
            </div>

            <div class="mt-6 pt-3.5 border-t border-[var(--color-secondary)]/20 flex items-center justify-between">
              <span class="text-[11px] text-gray-500">
                {{ playlist.items_count || playlist.anime?.length || 0 }} Titles
              </span>
              <router-link
                :to="`/playlists/${playlist.id}`"
                class="text-xs font-semibold text-[var(--color-primary)] hover:underline inline-flex items-center gap-1 font-heading"
              >
                <span>View Playlist</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </router-link>
            </div>
          </div>
        </div>
      </section>

      <!-- Not Found Fallback -->
      <div
        v-if="!user && !loading"
        class="rounded-2xl border border-[var(--color-secondary)]/30 bg-white p-12 text-center space-y-4 shadow-xs"
      >
        <div class="w-12 h-12 rounded-full bg-gray-100 text-gray-400 flex items-center justify-center mx-auto text-xl">
          ✦
        </div>
        <h2 class="text-xl font-bold font-heading text-[var(--color-dark)] m-0">User Not Found</h2>
        <p class="text-xs text-gray-500 max-w-sm mx-auto m-0">
          The member profile you are trying to view does not exist or has been deactivated.
        </p>
        <router-link
          to="/users"
          class="inline-block mt-2 px-4 py-2 rounded-lg bg-[var(--color-primary)] text-white text-xs font-semibold font-heading hover:bg-[#4307af] transition"
        >
          Return to Directory
        </router-link>
      </div>

    </div>

    <Loader v-if="loading" />

    <!-- Headless UI Modal for Direct Messaging -->
    <TransitionRoot appear :show="isMessageFormOpen" as="template">
      <Dialog as="div" @close="closeMessageForm" class="relative z-50 font-body">
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
              <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all border border-[var(--color-secondary)]/30">
                <MessageForm
                  v-if="isMessageFormOpen"
                  :message="message"
                  @send="sendMessage"
                  @close="closeMessageForm"
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
import { onMounted, ref, computed, watch } from "vue";
import { useRoute } from "vue-router";
import { useUserStore } from "../stores/users";
import { usePlaylistStore } from "../stores/playlist";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
} from "@headlessui/vue";
import MessageForm from "../components/MessageForm.vue";
import Loader from "../components/Loader.vue";

const route = useRoute();
const userStore = useUserStore();
const playlistStore = usePlaylistStore();

const userPlaylists = ref([]);
const isMessageFormOpen = ref(false);
const selectedUser = ref(null);
const message = ref("");

const loading = computed(() => userStore.isLoading);
const user = computed(() => userStore.getUser);
const isUserLocked = computed(() => Boolean(user.value?.is_locked));

const userInitials = computed(() => {
  if (!user.value) return "AL";
  if (user.value.first_name && user.value.last_name) {
    return `${user.value.first_name[0]}${user.value.last_name[0]}`.toUpperCase();
  }
  return (user.value.username?.slice(0, 2) || "AL").toUpperCase();
});

const formatDate = (val) => {
  if (!val) return "Recent Member";
  return new Date(val).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

const closeMessageForm = () => {
  isMessageFormOpen.value = false;
};

watch(
  user,
  async (newUser) => {
    if (newUser && !newUser.is_locked) {
      userPlaylists.value = [];
      try {
        const playlists = await playlistStore.getUserPlaylists(newUser.id);
        userPlaylists.value = playlists || [];
      } catch (err) {
        console.error("Error loading user playlists:", err);
      }
    }
  },
  { immediate: true }
);

const sendMessage = (messageData) => {
  const payload = {
    title: messageData.title,
    message: messageData.message,
    recipient: selectedUser.value.id,
  };
  userStore.sendMessageAction(payload);
  closeMessageForm();
};

const openMessageForm = (targetUser) => {
  selectedUser.value = targetUser;
  isMessageFormOpen.value = true;
  message.value = `Send message to @${targetUser.username}`;
};

onMounted(async () => {
  const userId = route.params.id;
  if (userId) {
    await userStore.getUserById(userId);
  }
});
</script>