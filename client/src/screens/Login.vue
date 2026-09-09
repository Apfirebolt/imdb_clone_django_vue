<template>
  <div class="min-h-screen bg-[var(--color-light)] text-[var(--color-dark)] font-body flex items-center justify-center p-4 sm:p-6 lg:p-8">
    <div class="bg-white shadow-xl rounded-2xl border border-[var(--color-secondary)]/30 overflow-hidden w-full max-w-4xl flex flex-col md:flex-row transition-all">
      
      <!-- Left Column - Form -->
      <div class="w-full md:w-1/2 p-6 sm:p-10 lg:p-12 flex flex-col justify-between">
        <div>
          <!-- Logo & Header -->
          <div class="mb-8">
            <router-link to="/" class="inline-flex items-center gap-1.5 font-heading text-xl font-bold text-[var(--color-dark)] mb-3">
              <span class="text-[var(--color-primary)] text-2xl leading-none">✦</span>
              <span>Movies <span class="text-[var(--color-primary)]">Lounge</span></span>
            </router-link>
            <h1 class="text-2xl sm:text-3xl font-bold font-heading text-[var(--color-dark)] tracking-tight m-0">
              Welcome Back
            </h1>
            <p class="text-xs sm:text-sm text-gray-500 mt-1">
              Sign in to manage playlists, rate shows, and join lounge debates.
            </p>
          </div>

          <!-- Error Alert Banner -->
          <div
            v-if="errorMessage"
            class="mb-6 p-3.5 rounded-lg bg-red-50 border border-[var(--color-danger)]/30 text-[var(--color-danger)] text-xs flex items-center gap-2"
          >
            <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ errorMessage }}</span>
          </div>

          <!-- Login Form -->
          <form @submit.prevent="handleLogin" class="space-y-4 sm:space-y-5">
            <div>
              <label
                for="email"
                class="block text-xs font-semibold text-[var(--color-dark)] mb-1.5 font-heading"
              >
                Email Address
              </label>
              <input
                id="email"
                v-model="email"
                type="text"
                autocomplete="email"
                required
                class="w-full px-3.5 py-2.5 bg-[var(--color-light)] border border-[var(--color-secondary)]/40 rounded-lg text-sm text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition"
                placeholder="you@example.com"
              />
            </div>

            <div>
              <div class="flex items-center justify-between mb-1.5">
                <label
                  for="password"
                  class="block text-xs font-semibold text-[var(--color-dark)] font-heading"
                >
                  Password
                </label>
                <a href="#" class="text-xs text-[var(--color-tertiary)] hover:underline font-medium">
                  Forgot password?
                </a>
              </div>
              <div class="relative">
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  autocomplete="current-password"
                  required
                  class="w-full pl-3.5 pr-10 py-2.5 bg-[var(--color-light)] border border-[var(--color-secondary)]/40 rounded-lg text-sm text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600 focus:outline-none"
                  tabindex="-1"
                >
                  <svg v-if="!showPassword" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18" />
                  </svg>
                </button>
              </div>
            </div>

            <div class="flex items-center justify-between text-xs">
              <label class="flex items-center gap-2 cursor-pointer text-gray-600 select-none">
                <input
                  id="remember"
                  v-model="rememberMe"
                  type="checkbox"
                  class="h-4 w-4 rounded border-[var(--color-secondary)]/50 text-[var(--color-primary)] focus:ring-[var(--color-primary)]"
                />
                <span>Remember me</span>
              </label>
            </div>

            <button
              type="submit"
              :disabled="userStore.isLoading"
              class="w-full mt-2 bg-[var(--color-primary)] hover:bg-[#4307af] text-white py-2.5 px-4 rounded-lg font-heading text-sm font-semibold shadow-sm hover:shadow transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 cursor-pointer"
            >
              <svg
                v-if="userStore.isLoading"
                class="animate-spin h-4 w-4 text-white"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
              </svg>
              <span>{{ userStore.isLoading ? 'Signing In...' : 'Sign In' }}</span>
            </button>
          </form>
        </div>

        <!-- Sign Up Link -->
        <div class="mt-8 pt-4 border-t border-[var(--color-secondary)]/20 text-center">
          <p class="text-xs text-gray-500">
            Don't have an account?
            <router-link
              to="/register"
              class="text-[var(--color-primary)] hover:underline font-semibold ml-1"
            >
              Create an account
            </router-link>
          </p>
        </div>
      </div>

      <!-- Right Column - Visual Hero -->
      <div class="hidden md:block md:w-1/2 relative bg-[var(--color-dark)] overflow-hidden">
        <img
          src="https://images.unsplash.com/photo-1578632767115-351597cf2477?fm=jpg&q=80&w=1200&auto=format&fit=crop"
          alt="Anime Lounge Atmosphere"
          class="w-full h-full object-cover opacity-80 mix-blend-overlay"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-[var(--color-dark)] via-[var(--color-dark)]/40 to-transparent flex flex-col justify-end p-8 text-white">
          <span class="text-xs font-bold uppercase tracking-widest text-[var(--color-accent-dark)] font-display">
            Curated Community
          </span>
          <h2 class="text-xl font-bold font-heading mt-1 mb-2 text-white">
            Discover. Discuss. Catalog.
          </h2>
          <p class="text-xs text-gray-300 font-body leading-relaxed max-w-xs">
            Join fellow enthusiasts creating custom playlists and rating seasonal releases.
          </p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../stores/auth.js";

const email = ref("");
const password = ref("");
const rememberMe = ref(false);
const showPassword = ref(false);
const errorMessage = ref("");

const router = useRouter();
const userStore = useAuth();

const handleLogin = async () => {
  errorMessage.value = "";

  try {
    // Passes username key for compatibility with Django REST framework
    await userStore.loginAction({
      email: email.value.trim(),
      password: password.value,
    });

    router.push("/dashboard");
  } catch (error) {
    errorMessage.value =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      "Invalid email or password. Please try again.";
  }
};
</script>