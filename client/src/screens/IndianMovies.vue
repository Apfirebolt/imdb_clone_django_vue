<template>
  <div class="bg-info flex items-center justify-center">
    <div class="bg-white shadow-lg rounded-lg p-4">
      
      <div class="flex flex-col md:flex-row items-center justify-between mb-4 mt-16 gap-4">
        <div class="flex w-full gap-4">
          <div class="w-3/4 text-center md:text-left">
            <h1 class="text-4xl font-bold text-primary mb-2">
              Indian Movies
            </h1>
            <p class="text-dark leading-relaxed">
              Welcome to the Indian Movies section! Here, you can explore a wide variety of
              films from Tamil and Telugu cinema. Discover trending blockbusters, critically acclaimed films,
              and the most anticipated upcoming releases.
            </p>
          </div>
          <div class="w-1/4 flex justify-end items-start">
            <button
              @click="isPlaylistModalOpened = true"
              class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors"
            >
              Open Playlist <font-awesome-icon icon="eye" class="text-white" />
            </button>
          </div>
        </div>
      </div>

      <Loader v-if="loading" />

      <div v-else class="mb-6">
        <div class="flex flex-wrap border-b border-gray-200">
          <button
            @click="changeTab('trendingTamil')"
            :class="[
              'px-4 py-2 font-medium text-sm border-b-2 transition-colors',
              selectedTab === 'trendingTamil'
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700',
            ]"
          >
            Trending Tamil
          </button>
          <button
            @click="changeTab('trendingTelugu')"
            :class="[
              'px-4 py-2 font-medium text-sm border-b-2 transition-colors',
              selectedTab === 'trendingTelugu'
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700',
            ]"
          >
            Trending Telugu
          </button>
          <button
            @click="changeTab('topRatedTamil')"
            :class="[
              'px-4 py-2 font-medium text-sm border-b-2 transition-colors',
              selectedTab === 'topRatedTamil'
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700',
            ]"
          >
            Top Rated Tamil
          </button>
          <button
            @click="changeTab('topRatedTelugu')"
            :class="[
              'px-4 py-2 font-medium text-sm border-b-2 transition-colors',
              selectedTab === 'topRatedTelugu'
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700',
            ]"
          >
            Top Rated Telugu
          </button>
          <button
            @click="changeTab('topRated')"
            :class="[
              'px-4 py-2 font-medium text-sm border-b-2 transition-colors',
              selectedTab === 'topRated'
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700',
            ]"
          >
            Top Rated
          </button>
          <button
            @click="changeTab('anticipated')"
            :class="[
              'px-4 py-2 font-medium text-sm border-b-2 transition-colors',
              selectedTab === 'anticipated'
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700',
            ]"
          >
            Anticipated
          </button>
        </div>

        <div class="mt-4">
          <div
            v-if="selectedTab === 'trendingTamil'"
            class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
          >
            <div
              v-for="movie in trendingTamilMovies"
              :key="movie.id"
              class="bg-gray-50 p-4 rounded-lg shadow-md"
            >
              <img
                v-if="movie.primaryImage"
                :src="movie.primaryImage"
                :alt="movie.primaryTitle"
                class="w-full h-48 object-cover rounded-lg mb-3"
              />
              <h3 class="font-semibold text-lg mb-2">
                {{ movie.primaryTitle || movie.title }}
              </h3>
              <p class="text-sm text-gray-600 mb-2">
                {{ movie.releaseDate || movie.release_date }}
              </p>
              <p
                v-if="movie.description"
                class="text-sm text-gray-700 mb-2 line-clamp-3"
              >
                {{ movie.description }}
              </p>
              <div class="flex justify-between items-center">
                <SaveMovie
                  v-if="isAuthenticated"
                  @saveMovie="addMovieToPlaylist(movie)"
                />
                <span
                  v-if="movie.averageRating"
                  class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm"
                >
                  ⭐ {{ movie.averageRating }}
                </span>
                <span
                  v-if="movie.contentRating"
                  class="bg-gray-200 text-gray-800 px-2 py-1 rounded text-sm"
                >
                  {{ movie.contentRating }}
                </span>
              </div>
            </div>
          </div>

          <div
            v-if="selectedTab === 'trendingTelugu'"
            class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
          >
            <div
              v-for="movie in trendingTeluguMovies"
              :key="movie.id"
              class="bg-gray-50 p-4 rounded-lg shadow-md"
            >
              <img
                v-if="movie.primaryImage"
                :src="movie.primaryImage"
                :alt="movie.primaryTitle"
                class="w-full h-48 object-cover rounded-lg mb-3"
              />
              <h3 class="font-semibold text-lg mb-2">
                {{ movie.primaryTitle || movie.title }}
              </h3>
              <p class="text-sm text-gray-600 mb-2">
                {{ movie.releaseDate || movie.release_date }}
              </p>
              <p
                v-if="movie.description"
                class="text-sm text-gray-700 mb-2 line-clamp-3"
              >
                {{ movie.description }}
              </p>
              <div class="flex justify-between items-center">
                <SaveMovie
                  v-if="isAuthenticated"
                  @saveMovie="addMovieToPlaylist(movie)"
                />
                <span
                  v-if="movie.averageRating"
                  class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm"
                >
                  ⭐ {{ movie.averageRating }}
                </span>
                <span
                  v-if="movie.contentRating"
                  class="bg-gray-200 text-gray-800 px-2 py-1 rounded text-sm"
                >
                  {{ movie.contentRating }}
                </span>
              </div>
            </div>
          </div>

          <div
            v-if="selectedTab === 'topRatedTamil'"
            class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
          >
            <div
              v-for="movie in topRatedTamilMovies"
              :key="movie.id"
              class="bg-gray-50 p-4 rounded-lg shadow-md"
            >
              <img
                v-if="movie.primaryImage"
                :src="movie.primaryImage"
                :alt="movie.primaryTitle"
                class="w-full h-48 object-cover rounded-lg mb-3"
              />
              <h3 class="font-semibold text-lg mb-2">
                {{ movie.primaryTitle || movie.title }}
              </h3>
              <p class="text-sm text-gray-600 mb-2">
                {{ movie.releaseDate || movie.release_date }}
              </p>
              <p
                v-if="movie.description"
                class="text-sm text-gray-700 mb-2 line-clamp-3"
              >
                {{ movie.description }}
              </p>
              <div class="flex justify-between items-center">
                <SaveMovie
                  v-if="isAuthenticated"
                  @saveMovie="addMovieToPlaylist(movie)"
                />
                <span
                  v-if="movie.averageRating"
                  class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm"
                >
                  ⭐ {{ movie.averageRating }}
                </span>
                <span
                  v-if="movie.contentRating"
                  class="bg-gray-200 text-gray-800 px-2 py-1 rounded text-sm"
                >
                  {{ movie.contentRating }}
                </span>
              </div>
            </div>
          </div>

          <div
            v-if="selectedTab === 'topRatedTelugu'"
            class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
          >
            <div
              v-for="movie in topRatedTeluguMovies"
              :key="movie.id"
              class="bg-gray-50 p-4 rounded-lg shadow-md"
            >
              <img
                v-if="movie.primaryImage"
                :src="movie.primaryImage"
                :alt="movie.primaryTitle"
                class="w-full h-48 object-cover rounded-lg mb-3"
              />
              <h3 class="font-semibold text-lg mb-2">
                {{ movie.primaryTitle || movie.title }}
              </h3>
              <p class="text-sm text-gray-600 mb-2">
                {{ movie.releaseDate || movie.release_date }}
              </p>
              <p
                v-if="movie.description"
                class="text-sm text-gray-700 mb-2 line-clamp-3"
              >
                {{ movie.description }}
              </p>
              <div class="flex justify-between items-center">
                <SaveMovie
                  v-if="isAuthenticated"
                  @saveMovie="addMovieToPlaylist(movie)"
                />
                <span
                  v-if="movie.averageRating"
                  class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm"
                >
                  ⭐ {{ movie.averageRating }}
                </span>
                <span
                  v-if="movie.contentRating"
                  class="bg-gray-200 text-gray-800 px-2 py-1 rounded text-sm"
                >
                  {{ movie.contentRating }}
                </span>
              </div>
            </div>
          </div>

          <div
            v-if="selectedTab === 'topRated'"
            class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
          >
            <div
              v-for="movie in topRatedMovies"
              :key="movie.id"
              class="bg-gray-50 p-4 rounded-lg shadow-md"
            >
              <img
                v-if="movie.primaryImage"
                :src="movie.primaryImage"
                :alt="movie.primaryTitle"
                class="w-full h-48 object-cover rounded-lg mb-3"
              />
              <h3 class="font-semibold text-lg mb-2">
                {{ movie.primaryTitle || movie.title }}
              </h3>
              <p class="text-sm text-gray-600 mb-2">
                {{ movie.releaseDate || movie.release_date }}
              </p>
              <p
                v-if="movie.description"
                class="text-sm text-gray-700 mb-2 line-clamp-3"
              >
                {{ movie.description }}
              </p>
              <div class="flex justify-between items-center">
                <SaveMovie
                  v-if="isAuthenticated"
                  @saveMovie="addMovieToPlaylist(movie)"
                />
                <span
                  v-if="movie.averageRating"
                  class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm"
                >
                  ⭐ {{ movie.averageRating }}
                </span>
                <span
                  v-if="movie.contentRating"
                  class="bg-gray-200 text-gray-800 px-2 py-1 rounded text-sm"
                >
                  {{ movie.contentRating }}
                </span>
              </div>
            </div>
          </div>

          <div
            v-if="selectedTab === 'anticipated'"
            class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
          >
            <div
              v-for="movie in anticipatedMovies"
              :key="movie.id"
              class="bg-gray-50 p-4 rounded-lg shadow-md"
            >
              <img
                v-if="movie.primaryImage"
                :src="movie.primaryImage"
                :alt="movie.primaryTitle"
                class="w-full h-48 object-cover rounded-lg mb-3"
              />
              <h3 class="font-semibold text-lg mb-2">
                {{ movie.primaryTitle || movie.title }}
              </h3>
              <p class="text-sm text-gray-600 mb-2">
                {{ movie.releaseDate || movie.release_date }}
              </p>
              <p
                v-if="movie.description"
                class="text-sm text-gray-700 mb-2 line-clamp-3"
              >
                {{ movie.description }}
              </p>
              <div class="flex justify-between items-center">
                <SaveMovie
                  v-if="isAuthenticated"
                  @saveMovie="addMovieToPlaylist(movie)"
                />
                <span
                  v-if="movie.averageRating"
                  class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm"
                >
                  ⭐ {{ movie.averageRating }}
                </span>
                <span
                  v-if="movie.contentRating"
                  class="bg-gray-200 text-gray-800 px-2 py-1 rounded text-sm"
                >
                  {{ movie.contentRating }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <TransitionRoot appear :show="isPlaylistModalOpened" as="template">
      <Dialog
        as="div"
        class="relative z-50"
        @close="isPlaylistModalOpened = false"
      >
        <TransitionChild
          as="template"
          enter="ease-out duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="ease-in duration-200"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black bg-opacity-30" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div
            class="flex min-h-full items-center justify-center p-4 text-center"
          >
            <TransitionChild
              as="template"
              enter="ease-out duration-300"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="ease-in duration-200"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel
                class="w-full max-w-xxl transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
              >
                <Dialog.Title
                  as="h3"
                  class="text-lg font-medium leading-6 text-gray-900"
                >
                  Your Playlists
                </Dialog.Title>
                <div class="mt-4">
                  <Playlist
                    :playlists="playlists"
                    :selectedPlaylist="selectedPlaylist"
                    @choosePlaylist="selectPlaylist"
                  />
                </div>
                <div class="mt-6 flex justify-end">
                  <button
                    type="button"
                    class="inline-flex justify-center rounded-md border border-transparent bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary-dark focus:outline-none"
                    @click="isPlaylistModalOpened = false"
                  >
                    Close
                  </button>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useIndianMoviesStore } from "../stores/indian-movies";
import { usePlaylistStore } from "../stores/playlist";
import { useAuth } from "../stores/auth";
import SaveMovie from "../components/SaveMovie.vue";
import Playlist from "../components/Playlist.vue";
import Loader from "../components/Loader.vue";
import {
  Dialog,
  TransitionRoot,
  TransitionChild,
  DialogPanel,
} from "@headlessui/vue";

const movieStore = useIndianMoviesStore();
const playlistStore = usePlaylistStore();
const authStore = useAuth();
const isPlaylistModalOpened = ref(false);
const selectedPlaylist = ref(null);
const isAuthenticated = computed(() => authStore.isLoggedIn);
const playlists = computed(() => playlistStore.getPlaylists);
const trendingTamilMovies = computed(() => movieStore.getTrendingTamil);
const trendingTeluguMovies = computed(() => movieStore.getTrendingTelugu);
const topRatedTamilMovies = computed(() => movieStore.getTopRatedTamil);
const topRatedTeluguMovies = computed(() => movieStore.getTopRatedTelugu);
const topRatedMovies = computed(() => movieStore.getTopRatedIndianMovies);
const anticipatedMovies = computed(() => movieStore.getAnticipatedMovies);
const loading = computed(() => movieStore.isLoading);
const selectedTab = ref("trendingTamil");

const changeTab = (tab) => {
  selectedTab.value = tab;
};

const selectPlaylist = (playlist) => {
  selectedPlaylist.value = playlist;
};

const addMovieToPlaylist = async (movie) => {
  if (!selectedPlaylist.value) {
    alert("Please select a playlist first.");
    return;
  }
  await playlistStore.addMovieToPlaylist(selectedPlaylist.value.id, movie);
};

onMounted(() => {
  movieStore.getTrendingTamilAction();
  movieStore.getTrendingTeluguAction();
  movieStore.getTopRatedTamilAction();
  movieStore.getTopRatedTeluguAction();
  movieStore.getTopRatedIndianMoviesAction();
  movieStore.getAnticipatedMoviesAction();
  playlistStore.fetchPlaylists();
});
</script>
