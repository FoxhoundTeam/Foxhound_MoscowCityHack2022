<template>
  <div>
    <v-row dense
      ><v-col cols="12"
        ><v-autocomplete
          label="Категория"
          :items="$store.state.categories.filter((v) => v.status == 'approved')"
          v-model="selectedCategoryId"
          item-text="name"
          item-value="id"
          clearable
        ></v-autocomplete></v-col
    ></v-row>
    <v-row dense>
      <v-col
        cols="12"
        v-for="(filter, i) in selectedCategory.filters"
        :key="`${filter.id}-${i}`"
      >
        <check-box-filter
          v-if="filter.type === 'checkbox'"
          :label="filter.label"
          :choices="filter.choices"
          :id="filter.id"
        />
        <radio-button-filter
          v-else-if="filter.type === 'radio'"
          :label="filter.label"
          :choices="filter.choices"
          :id="filter.id"
        />
        <range-filter
          v-else-if="filter.type === 'range'"
          :label="filter.label"
          :id="filter.id"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import CheckBoxFilter from "./filters/CheckBoxFilter.vue";
import RadioButtonFilter from "./filters/RadioButtonFilter.vue";
import RangeFilter from "./filters/RangeFilter.vue";
export default {
  components: { CheckBoxFilter, RadioButtonFilter, RangeFilter },
  computed: {
    ...mapGetters(["categoryById"]),
    selectedCategory() {
      return this.categoryById(this.selectedCategoryId) || {};
    },
    selectedCategoryId: {
      get() {
        return this.$store.state.selectedCategoryId;
      },
      set(value) {
        this.$store.commit("setSelectedCategoryId", value);
      },
    },
  },
  methods: {
    ...mapActions(["getGoods"]),
  },
  watch: {
    async selectedCategoryId(value) {
      await this.getGoods();
      this.$router.replace({
        name: "Search",
        query: { ...this.$route.query, category_id: value },
      });
    },
    $route(value) {
      if (value.query.category_id) {
        this.selectedCategoryId = Number(value.query.category_id);
      } else {
        this.selectedCategoryId = null;
      }
    },
  },
  mounted() {
    if (this.$route.query.category_id) {
      this.selectedCategoryId = Number(this.$route.query.category_id);
    } else {
      this.selectedCategoryId = null;
    }
  },
  beforeDestroy() {
      this.$store.commit("setGoodsFilters", {});
  }
};
</script>

<style>
</style>