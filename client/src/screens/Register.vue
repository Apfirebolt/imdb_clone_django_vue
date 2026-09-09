<template>
  <div class="min-h-screen bg-[var(--color-light)] text-[var(--color-dark)] font-body flex items-center justify-center p-4 sm:p-6 lg:p-8">
    <div class="bg-white shadow-xl rounded-2xl border border-[var(--color-secondary)]/30 overflow-hidden w-full max-w-5xl flex flex-col lg:flex-row transition-all">
      
      <!-- Left Column - Form -->
      <div class="w-full lg:w-7/12 p-6 sm:p-10 lg:p-12 flex flex-col justify-between">
        <div>
          <!-- Brand / Header -->
          <div class="mb-8">
            <router-link to="/" class="inline-flex items-center gap-1.5 font-heading text-xl font-bold text-[var(--color-dark)] mb-3">
              <span class="text-[var(--color-primary)] text-2xl leading-none">✦</span>
              <span>Movies <span class="text-[var(--color-primary)]">Lounge</span></span>
            </router-link>
            <h1 class="text-2xl sm:text-3xl font-bold font-heading text-[var(--color-dark)] tracking-tight m-0">
              Create an Account
            </h1>
            <p class="text-xs sm:text-sm text-gray-500 mt-1">
              Join the lounge to curate custom playlists, rate episodes, and join community discussions.
            </p>
          </div>

          <!-- Error Feedback Banner -->
          <div
            v-if="validationError"
            class="mb-6 p-3.5 rounded-lg bg-red-50 border border-[var(--color-danger)]/30 text-[var(--color-danger)] text-xs flex items-center gap-2"
          >
            <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <span>{{ validationError }}</span>
          </div>

          <!-- Register Form -->
          <form @submit.prevent="handleRegister" class="space-y-4 sm:space-y-5">
            <!-- First & Last Name Fields Row -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label for="firstName" class="block text-xs font-semibold text-[var(--color-dark)] mb-1.5 font-heading">
                  First Name <span class="text-[var(--color-danger)]">*</span>
                </label>
                <input
                  id="firstName"
                  v-model="firstName"
                  type="text"
                  required
                  placeholder="Edward"
                  class="w-full px-3.5 py-2.5 bg-[var(--color-light)] border border-[var(--color-secondary)]/40 rounded-lg text-sm text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition"
                />
              </div>

              <div>
                <label for="lastName" class="block text-xs font-semibold text-[var(--color-dark)] mb-1.5 font-heading">
                  Last Name <span class="text-[var(--color-danger)]">*</span>
                </label>
                <input
                  id="lastName"
                  v-model="lastName"
                  type="text"
                  required
                  placeholder="Elric"
                  class="w-full px-3.5 py-2.5 bg-[var(--color-light)] border border-[var(--color-secondary)]/40 rounded-lg text-sm text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition"
                />
              </div>
            </div>

            <!-- Username & Email Fields Row -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label for="username" class="block text-xs font-semibold text-[var(--color-dark)] mb-1.5 font-heading">
                  Username <span class="text-[var(--color-danger)]">*</span>
                </label>
                <input
                  id="username"
                  v-model="username"
                  type="text"
                  required
                  autocomplete="username"
                  placeholder="fullmetal_alchemist"
                  class="w-full px-3.5 py-2.5 bg-[var(--color-light)] border border-[var(--color-secondary)]/40 rounded-lg text-sm text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition"
                />
              </div>

              <div>
                <label for="email" class="block text-xs font-semibold text-[var(--color-dark)] mb-1.5 font-heading">
                  Email Address <span class="text-[var(--color-danger)]">*</span>
                </label>
                <input
                  id="email"
                  v-model="email"
                  type="email"
                  required
                  autocomplete="email"
                  placeholder="edward@alounge.io"
                  class="w-full px-3.5 py-2.5 bg-[var(--color-light)] border border-[var(--color-secondary)]/40 rounded-lg text-sm text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition"
                />
              </div>
            </div>

            <!-- Password & Confirm Password Fields Row -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label for="password" class="block text-xs font-semibold text-[var(--color-dark)] mb-1.5 font-heading">
                  Password <span class="text-[var(--color-danger)]">*</span>
                </label>
                <div class="relative">
                  <input
                    id="password"
                    v-model="password"
                    :type="showPassword ? 'text' : 'password'"
                    required
                    autocomplete="new-password"
                    placeholder="••••••••"
                    class="w-full pl-3.5 pr-10 py-2.5 bg-[var(--color-light)] border border-[var(--color-secondary)]/40 rounded-lg text-sm text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition"
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

              <div>
                <label for="confirmPassword" class="block text-xs font-semibold text-[var(--color-dark)] mb-1.5 font-heading">
                  Confirm Password <span class="text-[var(--color-danger)]">*</span>
                </label>
                <input
                  id="confirmPassword"
                  v-model="confirmPassword"
                  type="password"
                  required
                  autocomplete="new-password"
                  placeholder="••••••••"
                  class="w-full px-3.5 py-2.5 bg-[var(--color-light)] border border-[var(--color-secondary)]/40 rounded-lg text-sm text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition"
                  :class="{ 'border-[var(--color-danger)] focus:border-[var(--color-danger)] focus:ring-[var(--color-danger)]': passwordMismatch }"
                />
              </div>
            </div>

            <!-- Terms and Conditions -->
            <div class="flex items-start pt-1">
              <input
                id="agreeTerms"
                v-model="agreeTerms"
                type="checkbox"
                required
                class="mt-0.5 h-4 w-4 rounded border-[var(--color-secondary)]/50 text-[var(--color-primary)] focus:ring-[var(--color-primary)] cursor-pointer"
              />
              <label for="agreeTerms" class="ml-2.5 block text-xs text-gray-600 select-none cursor-pointer">
                I agree to the
                <a href="#" class="text-[var(--color-primary)] hover:underline font-semibold">Terms of Service</a>
                and
                <a href="#" class="text-[var(--color-primary)] hover:underline font-semibold">Privacy Policy</a>.
              </label>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              :disabled="auth.isLoading"
              class="w-full mt-2 bg-[var(--color-primary)] hover:bg-[#4307af] text-white py-2.5 px-4 rounded-lg font-heading text-sm font-semibold shadow-sm hover:shadow transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 cursor-pointer"
            >
              <svg
                v-if="auth.isLoading"
                class="animate-spin h-4 w-4 text-white"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
              </svg>
              <span>{{ auth.isLoading ? 'Creating Account...' : 'Create Account' }}</span>
            </button>
          </form>
        </div>

        <!-- Sign In Redirect Footer -->
        <div class="mt-8 pt-4 border-t border-[var(--color-secondary)]/20 text-center">
          <p class="text-xs text-gray-500">
            Already have an account?
            <router-link
              to="/login"
              class="text-[var(--color-primary)] hover:underline font-semibold ml-1"
            >
              Sign in instead
            </router-link>
          </p>
        </div>
      </div>

      <!-- Right Column - Visual Hero (Responsive: visible on desktop) -->
      <div class="hidden lg:block lg:w-5/12 relative bg-[var(--color-dark)] overflow-hidden">
        <img
          src="https://images.unsplash.com/photo-1578632767115-351597cf2477?fm=jpg&q=80&w=1200&auto=format&fit=crop"
          alt="Anime Lounge Aesthetic"
          class="w-full h-full object-cover opacity-75 mix-blend-overlay"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-[var(--color-dark)] via-[var(--color-dark)]/50 to-transparent flex flex-col justify-end p-10 text-white">
          <span class="text-xs font-bold uppercase tracking-widest text-[var(--color-accent-dark)] font-display">
            Start Exploring
          </span>
          <h2 class="text-2xl font-bold font-heading mt-1.5 mb-2 text-white">
            Your Personalized Movie List
          </h2>
          <p class="text-xs text-gray-300 font-body leading-relaxed max-w-sm">
            Save what you're watching, publish your reviews, and discover seasonal hidden gems curated by the community.
          </p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../stores/auth.js";

const router = useRouter();
const auth = useAuth();

const firstName = ref("");
const lastName = ref("");
const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const agreeTerms = ref(false);
const showPassword = ref(false);
const validationError = ref("");

const passwordMismatch = computed(() => {
  return confirmPassword.value.length > 0 && password.value !== confirmPassword.value;
});

const handleRegister = async () => {
  validationError.value = "";

  if (password.value !== confirmPassword.value) {
    validationError.value = "Passwords do not match. Please verify both fields.";
    return;
  }

  if (password.value.length < 8) {
    validationError.value = "Password must be at least 8 characters long.";
    return;
  }

  try {
    // Matches Django's User model parameters
    await auth.registerAction({
      username: username.value.trim(),
      email: email.value.trim(),
      password: password.value,
      firstName: firstName.value.trim(),
      lastName: lastName.value.trim(),
    });

    // Navigate to login after registration
    router.push("/login");
  } catch (error) {
    validationError.value =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      "Unable to create account. Please check your information and try again.";
  }
};
</script>