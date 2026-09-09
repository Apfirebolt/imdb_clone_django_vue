<template>
  <div class="min-h-screen bg-[var(--color-light)] text-[var(--color-dark)] font-body py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-5xl mx-auto space-y-8">

      <!-- Header Section -->
      <section class="rounded-2xl border border-[var(--color-secondary)]/30 bg-white p-6 sm:p-8 shadow-xs">
        <div class="space-y-1.5 max-w-2xl">
          <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-[var(--color-tertiary)]/10 text-[var(--color-tertiary)] font-display tracking-wider uppercase">
            <span>✦</span>
            <span>Account Center</span>
          </div>
          <h1 class="text-3xl sm:text-4xl font-bold font-heading text-[var(--color-dark)] tracking-tight m-0">
            Account Profile
          </h1>
          <p class="text-xs sm:text-sm text-gray-600 leading-relaxed m-0">
            Customize your lounge identity, manage security credentials, and control public profile visibility.
          </p>
        </div>
      </section>

      <!-- Main Form -->
      <form @submit.prevent="editProfileUtil" class="space-y-8">
        
        <!-- Top Section: Avatar & Privacy Settings -->
        <section class="rounded-2xl border border-[var(--color-secondary)]/30 bg-white p-6 sm:p-8 shadow-xs">
          <h2 class="text-lg font-bold font-heading text-[var(--color-dark)] pb-4 border-b border-[var(--color-secondary)]/20 m-0">
            Avatar & Lounge Privacy
          </h2>

          <div class="mt-6 flex flex-col md:flex-row items-center md:items-start gap-8">
            <!-- Avatar Display -->
            <div class="flex flex-col items-center gap-3">
              <div class="relative group">
                <div class="w-32 h-32 rounded-full overflow-hidden border-2 border-[var(--color-secondary)]/40 bg-[var(--color-light)] flex items-center justify-center shadow-xs">
                  <img
                    v-if="profile_picture_preview"
                    :src="profile_picture_preview"
                    alt="Profile Avatar"
                    class="w-full h-full object-cover"
                  />
                  <div
                    v-else
                    class="w-full h-full bg-gradient-to-tr from-[var(--color-primary)] to-[var(--color-tertiary)] text-white flex items-center justify-center font-heading font-bold text-3xl"
                  >
                    {{ getInitials }}
                  </div>
                </div>

                <label
                  for="profile_picture"
                  class="absolute bottom-1 right-1 bg-[var(--color-primary)] hover:bg-[#4307af] text-white p-2.5 rounded-full shadow-md cursor-pointer transition"
                  title="Upload profile picture"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <input
                    id="profile_picture"
                    type="file"
                    accept="image/*"
                    @change="onProfilePictureChange"
                    class="hidden"
                  />
                </label>
              </div>

              <div class="text-center">
                <p class="text-xs text-gray-500 m-0">PNG, JPG or WebP up to 5MB</p>
                <button
                  v-if="profile_picture_preview"
                  type="button"
                  @click="removeAvatar"
                  class="text-[11px] font-semibold text-[var(--color-danger)] hover:underline mt-1 cursor-pointer"
                >
                  Remove picture
                </button>
              </div>
            </div>

            <!-- Privacy Toggle Box -->
            <div class="flex-1 w-full space-y-4">
              <div class="p-4 rounded-xl bg-[var(--color-light)] border border-[var(--color-secondary)]/30 flex items-start justify-between gap-4">
                <div class="space-y-1">
                  <span class="text-xs font-bold font-heading text-[var(--color-dark)] block">
                    Lock Profile (Private Account)
                  </span>
                  <p class="text-xs text-gray-500 leading-relaxed m-0">
                    When active, your public watch queues, favorites, and review tallies will be hidden from the community roster.
                  </p>
                </div>

                <label class="relative inline-flex items-center cursor-pointer shrink-0 mt-1">
                  <input
                    id="is_locked"
                    type="checkbox"
                    v-model="is_locked"
                    class="sr-only peer"
                  />
                  <div class="w-11 h-6 bg-gray-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[var(--color-primary)]"></div>
                </label>
              </div>

              <div class="p-3.5 rounded-lg border border-[var(--color-tertiary)]/20 bg-[var(--color-tertiary)]/5 text-xs text-gray-600 flex items-center gap-2.5">
                <span class="text-[var(--color-tertiary)] font-bold text-sm">ⓘ</span>
                <span>Your username and avatar are always shown on your personal comments in discussion threads.</span>
              </div>
            </div>
          </div>
        </section>

        <!-- Bottom Section: Profile Details & Password -->
        <section class="rounded-2xl border border-[var(--color-secondary)]/30 bg-white p-6 sm:p-8 shadow-xs space-y-6">
          <h2 class="text-lg font-bold font-heading text-[var(--color-dark)] pb-4 border-b border-[var(--color-secondary)]/20 m-0">
            Personal Information
          </h2>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div>
              <label for="first_name" class="block text-xs font-semibold text-[var(--color-dark)] mb-1.5 font-heading">
                First Name
              </label>
              <input
                id="first_name"
                v-model="first_name"
                type="text"
                placeholder="Edward"
                class="w-full px-3.5 py-2.5 bg-[var(--color-light)] border border-[var(--color-secondary)]/40 rounded-lg text-sm text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition"
              />
            </div>

            <div>
              <label for="last_name" class="block text-xs font-semibold text-[var(--color-dark)] mb-1.5 font-heading">
                Last Name
              </label>
              <input
                id="last_name"
                v-model="last_name"
                type="text"
                placeholder="Elric"
                class="w-full px-3.5 py-2.5 bg-[var(--color-light)] border border-[var(--color-secondary)]/40 rounded-lg text-sm text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition"
              />
            </div>

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
                placeholder="spike_spiegel"
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

            <div class="sm:col-span-2">
              <div class="flex items-center justify-between mb-1.5">
                <label for="password" class="block text-xs font-semibold text-[var(--color-dark)] font-heading">
                  New Password
                </label>
                <span class="text-[11px] text-gray-500">Leave blank to keep current password</span>
              </div>
              <div class="relative">
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  autocomplete="new-password"
                  placeholder="••••••••"
                  class="w-full pl-3.5 pr-10 py-2.5 bg-[var(--color-light)] border border-[var(--color-secondary)]/40 rounded-lg text-sm text-[var(--color-dark)] placeholder:text-gray-400 focus:outline-none focus:bg-white focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600 focus:outline-none cursor-pointer"
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
          </div>

          <!-- Actions -->
          <div class="pt-4 border-t border-[var(--color-secondary)]/20 flex items-center justify-end gap-3">
            <button
              type="submit"
              :disabled="loading"
              class="px-6 py-2.5 rounded-lg bg-[var(--color-primary)] hover:bg-[#4307af] text-white text-xs sm:text-sm font-semibold font-heading shadow-xs hover:shadow transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 cursor-pointer"
            >
              <svg
                v-if="loading"
                class="animate-spin h-4 w-4 text-white"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
              </svg>
              <span>{{ loading ? 'Saving Changes...' : 'Update Profile' }}</span>
            </button>
          </div>
        </section>

      </form>
    </div>

    <Loader v-if="loading" />
  </div>
</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue";
import { useAuth } from "../stores/auth";
import { toast } from "vue3-toastify";
import Loader from "../components/Loader.vue";

const authStore = useAuth();
const email = ref("");
const username = ref("");
const password = ref("");
const first_name = ref("");
const last_name = ref("");
const profile_picture = ref(null);
const is_locked = ref(false);
const profile_picture_preview = ref(null);
const showPassword = ref(false);

const loading = computed(() => authStore.isLoading);
const profile = computed(() => authStore.getProfileData);

const getInitials = computed(() => {
  if (first_name.value && last_name.value) {
    return `${first_name.value[0]}${last_name.value[0]}`.toUpperCase();
  }
  if (username.value) {
    return username.value.slice(0, 2).toUpperCase();
  }
  return "AL";
});

watch(
  profile,
  (newProfile) => {
    if (newProfile) {
      username.value = newProfile.username || "";
      email.value = newProfile.email || "";
      first_name.value = newProfile.first_name || "";
      last_name.value = newProfile.last_name || "";
      is_locked.value = Boolean(newProfile.is_locked);
      profile_picture_preview.value = newProfile.profile_picture || null;
    }
  },
  { immediate: true }
);

const onProfilePictureChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    if (file.size > 5 * 1024 * 1024) {
      toast.error("Profile picture size exceeds 5MB limit.");
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      profile_picture_preview.value = e.target.result;
    };
    reader.readAsDataURL(file);
    profile_picture.value = file;
  }
};

const removeAvatar = () => {
  profile_picture.value = null;
  profile_picture_preview.value = null;
};

const editProfileUtil = async () => {
  try {
    const formData = new FormData();
    formData.append("username", username.value.trim());
    formData.append("email", email.value.trim());
    if (password.value) {
      formData.append("password", password.value);
    }
    formData.append("first_name", first_name.value.trim());
    formData.append("last_name", last_name.value.trim());
    formData.append("is_locked", is_locked.value ? "true" : "false");

    if (profile_picture.value) {
      formData.append("profile_picture", profile_picture.value);
    }

    await authStore.updateProfile(formData);
    password.value = "";
  } catch (error) {
    console.error("Error updating profile:", error);
  }
};

onMounted(() => {
  authStore.getProfileAction();
});
</script>