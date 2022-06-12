<template>
  <v-autocomplete
    @keyup.enter="doSearch(search)"
    v-model="selected"
    no-filter
    :items="items"
    :loading="isLoading"
    :search-input.sync="search"
    hide-selected
    hide-no-data
    label="Поиск"
    clearable
    rounded
    outlined
    append-icon=""
    append-outer-icon="mdi-magnify"
    @click:append-outer="doSearch(search)"
    :dense="dense"
  >
    <template #item="{ item }">
      <v-list-item class="d-flex" @click="doSearch(item)">
        <div class="ml-2">{{ item }}</div>
      </v-list-item>
    </template>
  </v-autocomplete>
</template>

<script>
import http from "../../http";
export default {
  props: {
    dense: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      search: "",
      isLoading: false,
    };
  },
  methods: {
    doSearch(value) {
      this.items = [value];
      this.selected = value;
      this.$router.push({ name: "Search", query: {...this.$route.query, q: value } });
    },
  },
  computed: {
    items: {
      get() {
        return this.$store.state.autocompleteItems;
      },
      set(value) {
        this.$store.commit("setAutocompleteItems", value);
      },
    },
    selected: {
      get() {
        return this.$store.state.search;
      },
      set(value) {
        this.$store.commit("setSearch", value);
      },
    },
  },
  watch: {
    async search(value) {
      if (!value || value == this.$route.query.q) {
        return;
      }
      this.isLoading = true;
      var response = await http.getList("Autocomplete", { q: value }, false);
      this.items = response.data;
      this.isLoading = false;
    },
    $route(value) {
      this.items = [value.query.q];
      this.selected = value.query.q;
    },
  },
  mounted() {
    this.items = [this.$route.query.q];
    this.selected = this.$route.query.q;
  },
};
</script>

<style>
</style>