<template>
  <div class="min-h-screen bg-[var(--color-light)] text-[var(--color-dark)] font-body py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto space-y-10">

      <!-- Hero Header Section -->
      <section class="rounded-2xl border border-[var(--color-secondary)]/30 bg-white p-6 sm:p-10 shadow-xs">
        <div class="max-w-3xl space-y-3">
          <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-[var(--color-tertiary)]/10 text-[var(--color-tertiary)] font-display tracking-wider uppercase">
            <span>✦</span>
            <span>Metadata & Directory Index</span>
          </div>

          <h1 class="text-3xl sm:text-4xl font-bold font-heading text-[var(--color-dark)] tracking-tight m-0">
            AnimeLounge Catalog Taxonomy
          </h1>

          <p class="text-sm sm:text-base text-gray-600 leading-relaxed m-0">
            Explore our comprehensive classification parameters. Filter anime, adaptations, and movies across formats, themes, spoken languages, and original studio origins.
          </p>

          <!-- Search / Filter Input -->
          <div class="pt-2 max-w-md">
            <div class="relative">
              <input
                v-model="filterQuery"
                type="text"
                placeholder="Filter tags, genres, or languages..."
                class="w-full pl-9 pr-3.5 py-2.5 rounded-lg text-xs sm:text-sm bg-[var(--color-light)] border border-[var(--color-secondary)]/40 text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition"
              />
              <svg class="w-4 h-4 absolute left-3 top-3 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
        </div>
      </section>

      <!-- Taxonomy Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-start">

        <!-- 1. Release Formats / Types -->
        <div class="rounded-xl border border-[var(--color-secondary)]/30 bg-white p-5 shadow-xs space-y-3">
          <div class="flex items-center justify-between pb-3 border-b border-[var(--color-secondary)]/20">
            <div>
              <h3 class="text-base font-bold font-heading text-[var(--color-dark)] m-0">Release Types</h3>
              <p class="text-[11px] text-gray-500 mt-0.5">Media distribution formats</p>
            </div>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[var(--color-light)] border border-[var(--color-secondary)]/20 text-gray-600">
              {{ filteredTypes.length }}
            </span>
          </div>

          <div v-if="!filteredTypes.length" class="text-xs text-gray-400 py-4 text-center">
            No types match your filter
          </div>

          <div v-else class="flex flex-wrap gap-1.5">
            <span
              v-for="type in filteredTypes"
              :key="type"
              class="text-xs font-medium px-2.5 py-1 rounded-md bg-[var(--color-light)] text-[var(--color-dark)] border border-[var(--color-secondary)]/30 hover:border-[var(--color-primary)] hover:text-[var(--color-primary)] transition cursor-default"
            >
              {{ type }}
            </span>
          </div>
        </div>

        <!-- 2. Genres (Takes prominent vertical height) -->
        <div class="rounded-xl border border-[var(--color-secondary)]/30 bg-white p-5 shadow-xs space-y-3 md:col-span-2 lg:col-span-2">
          <div class="flex items-center justify-between pb-3 border-b border-[var(--color-secondary)]/20">
            <div>
              <h3 class="text-base font-bold font-heading text-[var(--color-dark)] m-0">Genres & Themes</h3>
              <p class="text-[11px] text-gray-500 mt-0.5">Narrative categories & tropes</p>
            </div>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[var(--color-primary)]/10 text-[var(--color-primary)]">
              {{ filteredGenres.length }}
            </span>
          </div>

          <div v-if="!filteredGenres.length" class="text-xs text-gray-400 py-6 text-center">
            No genres match your filter
          </div>

          <div v-else class="max-h-60 overflow-y-auto pr-1">
            <div class="flex flex-wrap gap-1.5">
              <span
                v-for="genre in filteredGenres"
                :key="genre"
                class="text-xs font-medium px-2.5 py-1 rounded-md bg-[var(--color-light)] text-[var(--color-dark)] border border-[var(--color-secondary)]/20 hover:border-[var(--color-tertiary)] hover:text-[var(--color-tertiary)] transition cursor-pointer"
              >
                {{ genre }}
              </span>
            </div>
          </div>
        </div>

        <!-- 3. Spoken Languages -->
        <div class="rounded-xl border border-[var(--color-secondary)]/30 bg-white p-5 shadow-xs space-y-3">
          <div class="flex items-center justify-between pb-3 border-b border-[var(--color-secondary)]/20">
            <div>
              <h3 class="text-base font-bold font-heading text-[var(--color-dark)] m-0">Audio & Dubs</h3>
              <p class="text-[11px] text-gray-500 mt-0.5">Original audio & dubbed languages</p>
            </div>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[var(--color-light)] border border-[var(--color-secondary)]/20 text-gray-600">
              {{ filteredLanguages.length }}
            </span>
          </div>

          <div v-if="!filteredLanguages.length" class="text-xs text-gray-400 py-4 text-center">
            No languages match
          </div>

          <div v-else class="max-h-52 overflow-y-auto pr-1">
            <div class="flex flex-wrap gap-1.5">
              <span
                v-for="language in filteredLanguages"
                :key="language.id || language.name || language"
                class="text-xs font-medium px-2 py-1 rounded-md bg-[var(--color-light)] text-[var(--color-dark)] border border-[var(--color-secondary)]/20"
              >
                {{ language.name || language }}
              </span>
            </div>
          </div>
        </div>

        <!-- 4. Production Countries -->
        <div class="rounded-xl border border-[var(--color-secondary)]/30 bg-white p-5 shadow-xs space-y-3">
          <div class="flex items-center justify-between pb-3 border-b border-[var(--color-secondary)]/20">
            <div>
              <h3 class="text-base font-bold font-heading text-[var(--color-dark)] m-0">Countries</h3>
              <p class="text-[11px] text-gray-500 mt-0.5">Regions of production</p>
            </div>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[var(--color-light)] border border-[var(--color-secondary)]/20 text-gray-600">
              {{ filteredCountries.length }}
            </span>
          </div>

          <div v-if="!filteredCountries.length" class="text-xs text-gray-400 py-4 text-center">
            No countries match
          </div>

          <div v-else class="max-h-52 overflow-y-auto pr-1">
            <div class="flex flex-wrap gap-1.5">
              <span
                v-for="country in filteredCountries"
                :key="country.id || country.name || country"
                class="text-xs font-medium px-2 py-1 rounded-md bg-[var(--color-light)] text-[var(--color-dark)] border border-[var(--color-secondary)]/20"
              >
                {{ country.name || country }}
              </span>
            </div>
          </div>
        </div>

        <!-- 5. Country Codes -->
        <div class="rounded-xl border border-[var(--color-secondary)]/30 bg-white p-5 shadow-xs space-y-3">
          <div class="flex items-center justify-between pb-3 border-b border-[var(--color-secondary)]/20">
            <div>
              <h3 class="text-base font-bold font-heading text-[var(--color-dark)] m-0">Regional Codes</h3>
              <p class="text-[11px] text-gray-500 mt-0.5">ISO 3166 territory markers</p>
            </div>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[var(--color-light)] border border-[var(--color-secondary)]/20 text-gray-600">
              {{ filteredCountryCodes.length }}
            </span>
          </div>

          <div v-if="!filteredCountryCodes.length" class="text-xs text-gray-400 py-4 text-center">
            No codes match
          </div>

          <div v-else class="max-h-52 overflow-y-auto pr-1">
            <div class="flex flex-wrap gap-1.5">
              <span
                v-for="code in filteredCountryCodes"
                :key="code"
                class="text-[11px] font-mono font-semibold px-2 py-0.5 rounded bg-[var(--color-light)] text-[var(--color-primary)] border border-[var(--color-secondary)]/30"
              >
                {{ code }}
              </span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <Loader v-if="isLoading" />
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from "vue";
import { useConfigStore } from "../stores/config";
import Loader from "../components/Loader.vue";

const configStore = useConfigStore();
const filterQuery = ref("");

const isLoading = computed(() => configStore.isLoading);
const types = computed(() => configStore.getTypes || []);
const genres = computed(() => configStore.getGenres || []);
const countries = computed(() => configStore.getCountries || []);
const languages = computed(() => configStore.getLanguages || []);
const countryCodes = computed(() => configStore.getCountryCodes || []);

// Helper filter method
const matchFilter = (val) => {
  if (!filterQuery.value.trim()) return true;
  const q = filterQuery.value.toLowerCase().trim();
  const text = typeof val === "object" ? val.name || "" : String(val);
  return text.toLowerCase().includes(q);
};

const filteredTypes = computed(() => types.value.filter(matchFilter));
const filteredGenres = computed(() => genres.value.filter(matchFilter));
const filteredLanguages = computed(() => languages.value.filter(matchFilter));
const filteredCountries = computed(() => countries.value.filter(matchFilter));
const filteredCountryCodes = computed(() => countryCodes.value.filter(matchFilter));

onMounted(() => {
  configStore.getTypesAction();
  configStore.getGenresAction();
  configStore.getCountriesAction();
  configStore.getLanguagesAction();
  configStore.getCountryCodesAction();
});
</script>