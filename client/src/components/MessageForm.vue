<template>
  <form
    @submit.prevent="submitForm"
    class="max-w-md mx-auto bg-white p-8 rounded shadow"
  >
    <h2 class="text-2xl font-bold mb-6">
      {{ props.message }}
    </h2>
    <div class="mb-4">
      <label class="block text-gray-700 mb-2" for="title">Title</label>
      <input
        id="title"
        v-model="form.title"
        type="text"
        class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        required
      />
    </div>
    <div class="mb-4">
      <label class="block text-gray-700 mb-2" for="message">Message</label>
      <textarea
        id="message"
        v-model="form.message"
        class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        rows="4"
        required
      ></textarea>
    </div>
    <button
      type="submit"
      class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
    >
      Send
    </button>
  </form>
</template>

<script setup>
import { reactive, onMounted } from "vue";

const emit = defineEmits(["send"]);
const props = defineProps({
  message: {
    type: String,
    default: () => "",
  },
});
const form = reactive({
  title: "",
  message: "",
});

function submitForm() {
  if (form.title && form.message) {
    emit("send", form);
    form.title = "";
    form.message = "";
  } else {
    console.error("Form is incomplete");
  }
}
</script>
