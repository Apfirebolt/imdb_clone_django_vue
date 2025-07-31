<template>
  <form
    @submit.prevent="submitForm"
    class="max-w-md mx-auto bg-white p-8 rounded shadow"
  >
    <h2 class="text-2xl font-bold mb-6">Create Playlist</h2>
    <div class="mb-4">
      <label class="block text-gray-700 mb-2" for="name">Playlist Name</label>
      <input
        id="name"
        v-model="form.name"
        type="text"
        class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        required
      />
    </div>
    <div class="mb-4">
      <label class="block text-gray-700 mb-2" for="description"
        >Description</label
      >
      <textarea
        id="description"
        v-model="form.description"
        class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        rows="3"
      ></textarea>
    </div>
    <button
      type="submit"
      class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
    >
      Create
    </button>
  </form>
</template>

<script setup>
import { reactive } from "vue";

// emits ['create']
const emit = defineEmits(["create"]);

const form = reactive({
  name: "",
  description: "",
});

function submitForm() {
  if (form.name && form.description) {
    // Emit the create event with the form data
    emit("create", {
      name: form.name,
      description: form.description,
    });
    // Reset the form
    form.name = "";
    form.description = "";
  } else {
    // Handle validation error
    console.error("Form is incomplete");
  }
}
</script>
