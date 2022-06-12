<template>
  <v-card>
    <v-card-title>Добавление товара</v-card-title>
    <v-card-text>
      <v-autocomplete
        label="Категория"
        :items="categories"
        v-model="category_id"
        item-text="name"
        item-value="id"
        append-outer-icon="mdi-plus"
        @click:append-outer="showAddCategoryModal = true"
      ></v-autocomplete>
      <v-autocomplete
        label="Товар"
        v-if="category_id"
        :items="goods"
        item-text="name"
        item-value="id"
        v-model="good_id"
        append-outer-icon="mdi-plus"
        @click:append-outer="showAddGoodModal = true"
      ></v-autocomplete>
      <v-text-field label="Цена" v-model="price" v-if="good_id"></v-text-field>
    </v-card-text>
    <v-card-actions>
      <v-btn
        color="primary"
        large
        :disabled="!price"
        @click="create"
        :loading="creating"
        >Создать</v-btn
      >
    </v-card-actions>
    <create-good-modal v-model="showAddGoodModal" />
    <create-category-modal v-model="showAddCategoryModal" />
  </v-card>
</template>

<script>
import CreateGoodModal from "../modals/CreateGoodModal.vue";
import http from "../../http";
import CreateCategoryModal from "../modals/CreateCategoryModal.vue";
export default {
  components: { CreateGoodModal, CreateCategoryModal },
  data() {
    return {
      price: 0,
      showAddGoodModal: false,
      showAddCategoryModal: false,
      creating: false,
    };
  },
  computed: {
    category_id: {
      get() {
        return this.$store.state.createCategoryId;
      },
      set(value) {
        this.$store.commit("setCreateCategoryId", value);
      },
    },
    good_id: {
      get() {
        return this.$store.state.createGoodId;
      },
      set(value) {
        this.$store.commit("setCreateGoodId", value);
      },
    },
    goods: {
      get() {
        return this.$store.state.createGoodsList;
      },
      set(value) {
        this.$store.commit("setCreateGoodsList", value);
      },
    },
    categories: {
      get() {
        return this.$store.state.categories;
      },
      set(value) {
        this.$store.commit("setCategories", value);
      },
    },
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
  watch: {
    async category_id(value) {
      if (!value) return;
      this.goods = (
        await http.getList("GoodList", { category_id: value }, true)
      ).data;
    },
    "$store.state.categories"() {
      this.categories = this.$store.state.categories;
    },
  },
  mounted() {
    this.categories = this.$store.state.categories;
  },
  methods: {
    async create() {
      this.creating = true;
      let response = await http.createItem(`/api/good/${this.good_id}/create_for_company/`, {
        price: this.price,
        user_id: this.$store.state.user.id,
      });
      if (response == {}) return
      this.goods = [];
      this.categories = [];
      this.good_id = null;
      this.category_id = null;
      this.snackbarText = "Товар успешно добавлен";
      this.showSnackbar = true;
      this.creating = false;
      this.$router.replace({ name: "Index" });
    },
  },
};
</script>

<style>
</style>