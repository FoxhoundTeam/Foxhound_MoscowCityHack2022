<template>
  <div id="app">
    <v-app style="min-height: 100vh">
      <nav-bar />
      <v-main class="m-2">
        <router-view></router-view>
      </v-main>
      <v-dialog v-model="showErrorModal" max-width="300">
        <v-card>
          <v-card-title class="text-h5"> Ошибка </v-card-title>

          <v-card-text>
            {{ modalContent }}
          </v-card-text>

          <v-card-actions>
            <v-btn color="green darken-1" text @click="showErrorModal = false">
              OK
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-snackbar v-model="showSnackbar" color="success" :timeout="2000">
        {{ snackbarText }}

        <template v-slot:action="{ attrs }">
          <v-btn
            color="white"
            text
            v-bind="attrs"
            @click="showSnackbar = false"
          >
            Закрыть
          </v-btn>
        </template>
      </v-snackbar>
      <v-overlay :value="appLoading">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
    </v-app>
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";
import ErrorModal from "./plugins/ErrorModal";

export default {
  components: { NavBar },
  name: "app",
  data() {
    return {
      showErrorModal: false,
      modalContent: null,
      appLoading: true,
    };
  },
  async mounted() {
    ErrorModal.ErrorEvent.$on("show", (params) => {
      this.modalContent = params.data;
      this.showErrorModal = true;
    });
    await this.$store.dispatch("getCategories");
    this.appLoading = false;
  },
  computed: {
    showSnackbar: {
      get() {
        return this.$store.state.showSnackbar;
      },
      set(value) {
        this.$store.commit("setShowSnackbar", value);
      },
    },
    snackbarText: {
      get() {
        return this.$store.state.snackbarText;
      },
      set(value) {
        this.$store.commit("setSnackbarText", value);
      },
    },
  },
};
</script>
<style>
#app {
}
a {
  text-decoration: none !important;
}
</style>
