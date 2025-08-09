<template>
  <div class="bg-info">
    <div class="bg-white shadow-lg rounded-lg p-4">
      <div
        class="flex flex-col md:flex-row md:items-center md:justify-between mb-6 mt-12 gap-4"
      >
        <!-- Title & Description Box -->
        <div class="bg-gray-100 rounded-lg p-4 flex-1">
          <h1 class="text-4xl font-bold text-primary mb-2">Users</h1>
          <p class="text-dark leading-relaxed mb-4">
            Manage your users here. View user details and perform actions.
          </p>
        </div>
      </div>

      <div class="mt-6">
        <h2 class="text-2xl font-bold mb-4">All Users</h2>
        <div
          class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
        >
          <div
            v-if="!users.length"
            class="col-span-1 sm:col-span-2 md:col-span-3 lg:col-span-4 bg-gray-100 rounded-lg p-6 text-center"
          >
            <p class="text-gray-600">No users available.</p>
          </div>
          <div
            v-for="user in users"
            :key="user.id"
            class="bg-white border rounded-lg shadow p-4 flex flex-col items-center"
          >
            <div class="mb-3">
              <font-awesome-icon
                icon="user-circle"
                class="text-4xl text-primary"
              />
            </div>
            <h3 class="text-xl font-semibold mb-1">{{ user.username }}</h3>
            <p class="text-gray-600 mb-2">{{ user.email }}</p>
            <div class="mt-auto flex justify-center space-x-2">
              <button
                @click="goToUserDetail(user.id)"
                class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition"
              >
                View
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Loader v-if="loading" />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores/users";
import { useAuth } from "../stores/auth";
import Loader from "../components/Loader.vue";

const userStore = useUserStore();
const authStore = useAuth();
const router = useRouter();
const users = computed(() => userStore.getUsers);
const loading = computed(() => userStore.isLoading);

const goToUserDetail = (userId) => {
  // Navigate to user detail page
  router.push({ name: "UserDetail", params: { id: userId } });
};

onMounted(() => {
    userStore.fetchUsers();
});
</script>
