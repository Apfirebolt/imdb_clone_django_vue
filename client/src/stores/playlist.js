import { defineStore } from "pinia";
import { ref } from "vue";
import Cookie from "js-cookie";
import router from "../routes";
import { useAuth } from "./auth";
import { backendClient } from "../plugins/interceptor";
import { toast } from "vue3-toastify";
import { toastOptions } from "../utils";


export const usePlaylistStore = defineStore("playlist", {
  state: () => ({
    playlists: ref([]),
    playlist: ref(null),
    auditLogs: ref([]),
    loading: ref(false),
    error: ref(null),
  }),

  getters: {
    getPlaylists(state) {
      return state.playlists;
    },
    getPlaylist(state) {
      return state.playlist;
    },
    getAuditLogs(state) {
      return state.auditLogs;
    },
    isLoading(state) {
      return state.loading;
    },
    getError(state) {
      return state.error;
    },
  },

  actions: {
    logoutOnUnauthorized() {
      const authStore = useAuth();
      authStore.logout();
      router.push("/login");
      toast.error("Session expired. Please log in again.", toastOptions);
    },

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
        if (error.response && error.response.status === 401) {
          this.logoutOnUnauthorized();
        } else {
          toast.error("Failed to fetch playlists. Please try again.", toastOptions);
          this.error = error;
        }
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
        if (response.status === 201) {
          toast.success("Playlist created successfully!", toastOptions);
          this.playlists.push(response.data);
          return response.data;
        }
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
          Authorization: `Bearer ${JSON.parse(authData).access}`,
        };
        const response = await backendClient.put(
          `playlists/${id}`,
          updatedData,
          { headers }
        );
        if (response.status === 200) {
          const index = this.playlists.findIndex((p) => p.id === id);
          if (index !== -1) {
            this.playlists[index] = response.data;
          }
          toast.success("Playlist updated successfully!", toastOptions);
          return response.data;
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.logoutOnUnauthorized();
        } else {
          toast.error("Failed to update playlist. Please try again.", toastOptions);
        }
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
        const response = await backendClient.delete(`playlists/${id}`, {
          headers,
        });
        if (response.status === 204) {
          this.playlists = this.playlists.filter((p) => p.id !== id);
          toast.success("Playlist deleted successfully!", toastOptions);
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.logoutOnUnauthorized();
        } else {
          toast.error("Failed to delete playlist. Please try again.", toastOptions);
        }
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    // get single playlist by id
    async getPlaylistById(id) {
      this.loading = true;
      this.error = null;
      try {
        const authData = Cookie.get("user");
        const headers = {
          Authorization: `Bearer ${JSON.parse(authData).access}`,
        };
        const response = await backendClient.get(`playlists/${id}`, {
          headers,
        });
        if (response.status === 200) {
          this.playlist = response.data;
        }
      } catch (error) {
        this.error = error;
        // handle 401 error
        if (error.response && error.response.status === 401) {
          this.logoutOnUnauthorized();
        } else {
          toast.error("Failed to fetch playlist. Please try again.", toastOptions);
        }
        return null;
      } finally {
        this.loading = false;
      }
    },

    async getUserPlaylists(userId) {
      this.loading = true;
      this.error = null;
      try {
        const authData = Cookie.get("user");
        const headers = {
          Authorization: `Bearer ${JSON.parse(authData).access}`,
        };
        const response = await backendClient.get(`playlists?user_id=${userId}`, {
          headers,
        });
        if (response.status === 200) {
          return response.data;
        }
      } catch (error) {
        this.error = error;
        if (error.response && error.response.status === 401) {
          this.logoutOnUnauthorized();
        } else {
          toast.error("Failed to fetch user playlists. Please try again.", toastOptions);
        }
        return [];
      } finally {
        this.loading = false;
      }
    },

    async addMovieToPlaylist(playlistId, movieData) {
      this.loading = true;
      this.error = null;
      try {
        const authData = Cookie.get("user");
        const headers = {
          Authorization: `Bearer ${JSON.parse(authData).access}`,
        };
        const data = {
          movie: {
            imdb_id: movieData.id,
            title: movieData.originalTitle,
            description: movieData.description,
            primary_image: movieData.primaryImage,
            trailer: movieData.trailer,
            release_date: movieData.releaseDate,
            metascore: movieData.metascore,
            genres: movieData.genres,
          },
        };
        const response = await backendClient.put(
          `playlists/${playlistId}/add-movie`,
          data,
          { headers }
        );
        if (response.status === 200) {
          const index = this.playlists.findIndex((p) => p.id === playlistId);
          if (index !== -1) {
            this.playlists[index] = response.data;
          }
          toast.success("Movie added to playlist successfully!", toastOptions);
          return response.data;
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.logoutOnUnauthorized();
        } else {
          toast.error("Failed to add movie to playlist. Please try again.", toastOptions);
        }
        this.error = error;
        return null;
      } finally {
        this.loading = false;
      }
    },

    // remove movie from a playlist
    async removeMovieFromPlaylist(playlistId, movieId) {
      this.loading = true;
      this.error = null;
      try {
        const authData = Cookie.get("user");
        const headers = {
          Authorization: `Bearer ${JSON.parse(authData).access}`,
        };
        const response = await backendClient.put(
          `playlists/${playlistId}/remove-movie`,
          { movie_id: movieId },
          { headers }
        );
        if (response.status === 200) {
          const index = this.playlists.findIndex((p) => p.id === playlistId);
          if (index !== -1) {
            this.playlists[index] = response.data;
          }
          toast.success(
            "Movie removed from playlist successfully!",
            toastOptions
          );
          return response.data;
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.logoutOnUnauthorized();
        } else {
          toast.error("Failed to remove movie from playlist. Please try again.", toastOptions);
        }
        this.error = error;
        return null;
      } finally {
        this.loading = false;
      }
    },

    async updateMovie(movieId, reviewData) {
      this.loading = true;
      this.error = null;
      try {
        const authData = Cookie.get("user");
        const headers = {
          Authorization: `Bearer ${JSON.parse(authData).access}`,
        };
        const response = await backendClient.put(
          `movies/${movieId}/review`,
          reviewData,
          { headers }
        );
        if (response.status === 201) {
          toast.success("Review added successfully!", toastOptions);
          return response.data;
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.logoutOnUnauthorized();
        } else {
          toast.error("Failed to update movie review. Please try again.", toastOptions);
        }
        this.error = error;
        return null;
      } finally {
        this.loading = false;
      }
    },

    async fetchAuditLogs() {
      this.loading = true;
      this.error = null;
      try {
        const authData = Cookie.get("user");
        const headers = {
          Authorization: `Bearer ${JSON.parse(authData).access}`,
        };
        const response = await backendClient.get("audit-logs", { headers });
        if (response.status === 200) {
          this.auditLogs = response.data;
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.logoutOnUnauthorized();
        } else {
          toast.error("Failed to fetch audit logs. Please try again.", toastOptions);
        }
        this.error = error;
      } finally {
        this.loading = false;
      }
    },
  },

  resetPlaylists() {
    this.playlists = [];
    this.playlist = null;
    this.loading = false;
    this.error = null;
  },
});
