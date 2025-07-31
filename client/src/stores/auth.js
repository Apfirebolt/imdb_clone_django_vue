import { defineStore } from "pinia";
import { ref } from "vue";
import Cookie from "js-cookie";
import router from "../routes";
import { toast } from 'vue3-toastify';
import { backendClient } from "../plugins/interceptor";

const toastOptions = {
  position: "top-right",
  autoClose: 5000,
  hideProgressBar: false,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  progress: undefined,
};

export const useAuth = defineStore("auth", {
  state: () => ({
    authData: Cookie.get("user") ? JSON.parse(Cookie.get("user")) : null,
    loading: ref(false),
  }),

  getters: {
    getAuthData() {
      return this.authData;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    async loginAction(loginData) {
      try {
        const response = await backendClient.post("login", loginData);
        if (response.data) {
          this.authData = response.data;
          // Show success toast
          toast.success("Login successful!", toastOptions);
          // set the data in cookie
          Cookie.set("user", JSON.stringify(response.data), { expires: 30 });
          // wait for 2 second before redirecting
          setTimeout(() => {
            router.push("/dashboard");
          }, 2000);
        }
      } catch (error) {
        let message = "An error occurred!";
        if (error.response && error.response.data) {
          message = error.response.data.message;
        }
        console.log('Some error', error);
        return error;
      }
    },

    async registerAction(registerData) {
      try {
        const response = await backendClient.post("register", registerData);
        if (response.data && response.status === 201) {
          this.authData = response.data;
          // Show success toast
          toast.success("Registration successful!", toastOptions);
          Cookie.set("user", JSON.stringify(response.data), { expires: 30 });
          router.push("/dashboard");
        }
      } catch (error) {
        let message = "An error occurred!";
        if (error.response && error.response.data) {
          message = error.response.data.message;
        }
        console.log(error);
        return error;
      }
    },

    async getProfileData() {
      try {
        // get the token from the cookie
        const authData = Cookie.get("user");
        const headers = {
          Authorization: `Bearer ${JSON.parse(authData).token}`,
        };
        const response = await backendClient.get("users/profile", { headers });
        console.log(response.data);
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    logout() {
      this.authData = null;
      Cookie.remove("user");
      router.push("/login");
    },

    resetAuth() {
      this.authData = {};
    },
  },
});