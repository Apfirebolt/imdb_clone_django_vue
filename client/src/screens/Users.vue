<template>
  <div class="min-h-screen bg-[var(--color-light)] text-[var(--color-dark)] font-body py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto space-y-8">

      <!-- Header & Directory Hero -->
      <section class="rounded-2xl border border-[var(--color-secondary)]/30 bg-white p-6 sm:p-8 shadow-xs">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          <div class="space-y-1.5 max-w-2xl">
            <span class="text-xs font-bold uppercase tracking-wider text-[var(--color-tertiary)] font-display">
              Community Roster
            </span>
            <h1 class="text-3xl sm:text-4xl font-bold font-heading text-[var(--color-dark)] tracking-tight m-0">
              Explore Users
            </h1>
            <p class="text-xs sm:text-sm text-gray-600 leading-relaxed m-0">
              Browse community members, view their curated anime playlists, and inspect review histories.
            </p>
          </div>

          <!-- Search & Count Bar -->
          <div class="flex flex-col sm:flex-row sm:items-center gap-3 w-full lg:w-auto">
            <div class="relative w-full sm:w-72">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by username or email..."
                class="w-full pl-9 pr-3.5 py-2 rounded-lg text-xs sm:text-sm bg-[var(--color-light)] border border-[var(--color-secondary)]/40 text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition"
              />
              <svg class="w-4 h-4 absolute left-3 top-2.5 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>

            <div class="text-xs font-semibold px-3 py-2 rounded-lg bg-[var(--color-light)] border border-[var(--color-secondary)]/30 text-gray-600 whitespace-nowrap self-start sm:self-auto">
              {{ filteredUsers.length }} {{ filteredUsers.length === 1 ? 'member' : 'members' }}
            </div>
          </div>
        </div>
      </section>

      <!-- Users Grid -->
      <section class="space-y-4">
        <!-- Empty State -->
        <div
          v-if="!filteredUsers.length"
          class="rounded-2xl border-2 border-dashed border-[var(--color-secondary)]/40 bg-white p-12 text-center flex flex-col items-center justify-center gap-3"
        >
          <div class="w-12 h-12 rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)] flex items-center justify-center text-xl">
            <font-awesome-icon icon="user-circle" />
          </div>
          <div class="space-y-1">
            <h3 class="text-base font-semibold font-heading text-[var(--color-dark)] m-0">
              {{ searchQuery ? 'No matching members found' : 'No users registered yet' }}
            </h3>
            <p class="text-xs text-gray-500 max-w-sm m-0">
              {{ searchQuery ? `Try searching for a different keyword than "${searchQuery}".` : 'As soon as people join AnimeLounge, their public profiles will appear here.' }}
            </p>
          </div>
          <button
            v-if="searchQuery"
            type="button"
            @click="searchQuery = ''"
            class="text-xs font-semibold text-[var(--color-primary)] hover:underline mt-2 cursor-pointer"
          >
            Clear search filter
          </button>
        </div>

        <!-- User Cards -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
          <div
            v-for="user in filteredUsers"
            :key="user.id"
            class="group rounded-xl border border-[var(--color-secondary)]/30 bg-white p-5 flex flex-col justify-between hover:border-[var(--color-primary)]/50 hover:shadow-md transition-all duration-200"
          >
            <!-- Card Body -->
            <div class="flex flex-col items-center text-center space-y-3">
              <!-- Avatar with Monogram Fallback -->
              <div class="relative">
                <div class="w-16 h-16 rounded-full bg-gradient-to-tr from-[var(--color-primary)] to-[var(--color-tertiary)] text-white flex items-center justify-center font-heading font-bold text-xl shadow-xs group-hover:scale-105 transition-transform">
                  {{ getInitials(user) }}
                </div>
                <!-- Online / Member Status Dot -->
                <span
                  class="absolute bottom-0 right-0 w-4 h-4 rounded-full bg-[var(--color-success)] border-2 border-white"
                  title="Active Member"
                ></span>
              </div>

              <!-- Names & Email -->
              <div class="space-y-1 w-full px-1">
                <div class="flex items-center justify-center gap-1">
                  <h3 class="font-heading font-bold text-base text-[var(--color-dark)] group-hover:text-[var(--color-primary)] transition-colors truncate m-0">
                    {{ user.username }}
                  </h3>
                </div>
                <p class="text-xs text-gray-500 truncate m-0">
                  {{ user.email }}
                </p>
              </div>

              <!-- Metadata Badge -->
              <div class="pt-1">
                <span class="inline-flex items-center gap-1 text-[10px] font-semibold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-[var(--color-light)] text-gray-600 border border-[var(--color-secondary)]/20">
                  <span>✦</span>
                  <span>Otaku</span>
                </span>
              </div>
            </div>

            <!-- Action Link -->
            <div class="mt-6 pt-4 border-t border-[var(--color-secondary)]/20 flex items-center justify-center">
              <button
                type="button"
                @click="goToUserDetail(user.id)"
                class="w-full py-2 px-3 rounded-lg bg-[var(--color-light)] hover:bg-[var(--color-primary)] hover:text-white text-[var(--color-dark)] text-xs font-semibold font-heading transition-all duration-150 flex items-center justify-center gap-2 cursor-pointer group-hover:border-transparent border border-[var(--color-secondary)]/30"
              >
                <span>View Profile</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </section>

    </div>

    <Loader v-if="loading" />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores/users";
import Loader from "../components/Loader.vue";

const userStore = useUserStore();
const router = useRouter();
const searchQuery = ref("");

const users = computed(() => userStore.getUsers || []);
const loading = computed(() => userStore.isLoading);

// Reactive search filter across username and email
const filteredUsers = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  if (!query) return users.value;
  return users.value.filter(
    (u) =>
      u.username?.toLowerCase().includes(query) ||
      u.email?.toLowerCase().includes(query)
  );
});

// Generate initials (e.g., "sp" for "spike_spiegel")
const getInitials = (user) => {
  if (user.firstName && user.lastName) {
    return `${user.firstName[0]}${user.lastName[0]}`.toUpperCase();
  }
  if (user.username) {
    return user.username.slice(0, 2).toUpperCase();
  }
  return "AL";
};

const goToUserDetail = (userId) => {
  router.push({ name: "UserDetail", params: { id: userId } });
};

onMounted(() => {
  userStore.fetchUsers();
});
</script>