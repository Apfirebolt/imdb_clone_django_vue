<template>
  <main class="min-h-screen bg-[var(--color-light)] text-[var(--color-dark)] font-body flex items-center justify-center p-4 sm:p-6">
    <div class="w-full max-w-xl text-center space-y-6">
      
      <!-- Subtle Decorative Badge -->
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-white border border-[var(--color-secondary)]/30 text-[var(--color-tertiary)] shadow-xs">
        <span class="text-sm">✦</span>
        <span class="font-display tracking-wider uppercase text-[10px]">Lost in the Void</span>
      </div>

      <!-- Giant 404 with Gradient Accent -->
      <div class="relative flex items-center justify-center select-none">
        <span class="text-8xl sm:text-9xl font-black font-heading tracking-tighter text-[var(--color-primary)]/10 blur-[1px]">
          404
        </span>
        <span class="absolute text-7xl sm:text-8xl font-black font-heading tracking-tight text-[var(--color-dark)]">
          4<span class="text-[var(--color-primary)]">0</span>4
        </span>
      </div>

      <!-- Copy & Context -->
      <div class="space-y-2 max-w-md mx-auto">
        <h1 class="text-2xl sm:text-3xl font-bold font-heading text-[var(--color-dark)] tracking-tight m-0">
          Episode Not Found
        </h1>
        <p class="text-xs sm:text-sm text-gray-600 leading-relaxed m-0">
          The page or playlist you are looking for might have been moved, deleted, or ended up on another timeline.
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="pt-2 flex flex-wrap items-center justify-center gap-3 font-heading">
        <button
          type="button"
          @click="goBack"
          class="px-5 py-2.5 rounded-lg border border-[var(--color-secondary)]/40 bg-white hover:bg-gray-50 text-[var(--color-dark)] text-xs sm:text-sm font-semibold transition shadow-xs cursor-pointer inline-flex items-center gap-2"
        >
          <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          <span>Previous Page</span>
        </button>

        <router-link
          to="/"
          class="px-5 py-2.5 rounded-lg bg-[var(--color-primary)] hover:bg-[#4307af] text-white text-xs sm:text-sm font-semibold transition shadow-xs hover:shadow inline-flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          <span>Back to Lounge</span>
        </router-link>
      </div>

      <!-- Quick Helpful Links -->
      <div class="pt-6 border-t border-[var(--color-secondary)]/20 text-xs text-gray-500 flex items-center justify-center gap-4">
        <span>Need a suggestion?</span>
        <router-link to="/browse" class="text-[var(--color-tertiary)] hover:underline font-semibold">
          Browse Anime
        </router-link>
        <span>•</span>
        <router-link to="/dashboard" class="text-[var(--color-tertiary)] hover:underline font-semibold">
          Dashboard
        </router-link>
      </div>

    </div>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router'

defineOptions({
  name: 'NotFoundPage',
})

const router = useRouter()

const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/')
  }
}
</script>