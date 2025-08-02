<template>
  <div class="bg-info">
    <div class="bg-white shadow-lg rounded-lg p-4">
      <div
        class="flex flex-col md:flex-row md:items-center md:justify-between mb-6 mt-12 gap-4"
      >
        <!-- Title & Description Box -->
        <div class="bg-gray-100 rounded-lg p-4 flex-1">
          <h1 class="text-4xl font-bold text-primary mb-2">Profile</h1>
          
          <p class="text-dark leading-relaxed mb-4">
            Manage your profile information here. You can update your details and preferences.
          </p>
        </div>
      </div>

      <div class="mt-6">
        <h2 class="text-2xl font-bold mb-4">Your Information</h2>
        <form
          @submit.prevent="editProfileUtil({ username, email, password })"
          class="grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          <div>
            <label
              class="block text-sm font-medium text-gray-700 mb-1"
              for="username"
              >Username</label
            >
            <input
              id="username"
              v-model="username"
              type="text"
              class="mt-1 block w-full p-2 rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
              placeholder="Enter username"
              required
            />
          </div>
          <div>
            <label
              class="block text-sm font-medium text-gray-700 mb-1"
              for="email"
              >Email</label
            >
            <input
              id="email"
              v-model="email"
              type="email"
              class="mt-1 block w-full p-2 rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
              placeholder="Enter email"
              required
            />
          </div>
          <div>
            <label
              class="block text-sm font-medium text-gray-700 mb-1"
              for="password"
              >Password</label
            >
            <input
              id="password"
              v-model="password"
              type="password"
              class="mt-1 block w-full p-2 rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
              placeholder="Enter new password"
            />
          </div>
          <div class="col-span-1 md:col-span-3 flex justify-end mt-4">
            <button
              type="submit"
              class="px-6 py-2 bg-primary text-white rounded-lg shadow hover:bg-primary-dark transition"
            >
              Update Profile
            </button>
          </div>
        </form>
      </div>
    </div>

    <Loader v-if="loading" />
  </div>
</template>

<script setup>
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
} from "@headlessui/vue";
import { onMounted, ref, computed, watch } from "vue";
import { useAuth } from "../stores/auth";
import Loader from "../components/Loader.vue";

const authStore = useAuth();
const email = ref("");
const username = ref("");
const password = ref("");
const loading = computed(() => authStore.isLoading);
const profile = computed(() => authStore.getProfileData);

const editProfileUtil = async (profileData) => {
  try {
    await authStore.updateProfile(profileData);
  } catch (error) {
    console.error("Error updating profile:", error);
  }
};

watch(profile, (newProfile) => {
  if (newProfile) {
    username.value = newProfile.username;
    email.value = newProfile.email;
  }
});

onMounted(() => {
    authStore.getProfileAction();
});
</script>
