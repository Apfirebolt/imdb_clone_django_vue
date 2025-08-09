<template>
  <div class="bg-info min-h-screen">
    <div class="bg-white shadow-lg rounded-lg p-4 max-w-2xl mx-auto mt-12">
      <div
        class="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-4"
      >
        <!-- Title & Description Box -->
        <div class="bg-gray-100 rounded-lg p-4 flex-1">
          <h1 class="text-4xl font-bold text-primary mb-2">User Detail</h1>
          <p class="text-dark leading-relaxed mb-4">
            View detailed information about this user.
          </p>
        </div>
      </div>

      <div v-if="user" class="flex flex-col items-center mt-8">
        <font-awesome-icon
          icon="user-circle"
          class="text-6xl text-primary mb-4"
        />
        <h2 class="text-2xl font-bold mb-2">{{ user.username }}</h2>
        <p class="text-gray-600 mb-1">
          <strong>Email:</strong> {{ user.email }}
        </p>
        <p class="text-gray-600 mb-1" v-if="user.first_name || user.last_name">
          <strong>Name:</strong> {{ user.first_name }} {{ user.last_name }}
        </p>
        <p class="text-gray-600 mb-1" v-if="user.date_joined">
          <strong>Joined:</strong>
          {{ new Date(user.date_joined).toLocaleDateString() }}
        </p>
        <!-- Add more user fields as needed -->
      </div>
      <div v-else class="text-center text-gray-600 py-12">User not found.</div>
    </div>
    <Loader v-if="loading" />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useRoute } from "vue-router";
import { useUserStore } from "../stores/users";
import Loader from "../components/Loader.vue";

const route = useRoute();
const userStore = useUserStore();
const loading = computed(() => userStore.isLoading);
const user = computed(() => userStore.getUser);

onMounted(async () => {
  const userId = route.params.id;
  await userStore.getUserById(userId);
});
</script>
