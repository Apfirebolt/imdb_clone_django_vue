import { defineStore } from "pinia";
import { ref } from "vue";
import Cookie from "js-cookie";
import router from "../routes";
import { backendClient } from "../plugins/interceptor";

export const usePlaylistStore = defineStore("playlist", {
  state: () => ({
    playlists: ref([]),
    loading: ref(false),
    error: ref(null),
  }),

  getters: {
    getPlaylists(state) {
      return state.playlists;
    },
    isLoading(state) {
      return state.loading;
    },
    getError(state) {
      return state.error;
    },
  },

  actions: {
    async fetchPlaylists() {
      this.loading = true;
      this.error = null;
      try {
        const authData = Cookie.get("user");
        const headers = {
          Authorization: `Bearer ${JSON.parse(authData).access}`,
        };
        const response = await backendClient.get("playlists", { headers });
        this.playlists = response.data;
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    async createPlaylist(playlistData) {
      this.loading = true;
      this.error = null;
      try {
        const authData = Cookie.get("user");
        const headers = {
          Authorization: `Bearer ${JSON.parse(authData).access}`,
        };
        const response = await backendClient.post("playlists", playlistData, {
          headers,
        });
        this.playlists.push(response.data);
        return response.data;
      } catch (error) {
        this.error = error;
        return null;
      } finally {
        this.loading = false;
      }
    },

    async updatePlaylist(id, updatedData) {
      this.loading = true;
      this.error = null;
      try {
        const authData = Cookie.get("user");
        const headers = {
          Authorization: `Bearer ${JSON.parse(authData).token}`,
        };
        const response = await backendClient.put(
          `playlists/${id}`,
          updatedData,
          { headers }
        );
        const idx = this.playlists.findIndex((p) => p.id === id);
        if (idx !== -1) {
          this.playlists[idx] = response.data;
        }
        return response.data;
      } catch (error) {
        this.error = error;
        return null;
      } finally {
        this.loading = false;
      }
    },

    async deletePlaylist(id) {
      this.loading = true;
      this.error = null;
      try {
        const authData = Cookie.get("user");
        const headers = {
          Authorization: `Bearer ${JSON.parse(authData).access}`,
        };
        await backendClient.delete(`playlists/${id}`, { headers });
        this.playlists = this.playlists.filter((p) => p.id !== id);
      } catch (error) {
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    resetPlaylists() {
      this.playlists = [];
      this.error = null;
    },
  },
});
