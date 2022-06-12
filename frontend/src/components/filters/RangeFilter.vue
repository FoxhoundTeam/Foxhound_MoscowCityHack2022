<template>
  <v-card elevation="0">
    <v-card-title>{{ label }}</v-card-title>
    <v-text-field
      placeholder="От"
      outlined
      type="number"
      v-model.number="min"
      @blur="filterMin"
    ></v-text-field>
    <v-text-field
      placeholder="До"
      outlined
      type="number"
      v-model.number="max"
      @blur="filterMax"
    ></v-text-field>
  </v-card>
</template>

<script>
import { mapActions } from "vuex";
export default {
  props: ["label", "id"],
  data() {
    return {
      min: null,
      max: null,
    };
  },
  methods: {
    ...mapActions(["getGoods"]),
    async filterMin() {
      let goodsFilters = this.$store.state.goodsFilters;
      if (this.min == goodsFilters[`filter_${this.id}_gte`]) return
      if (this.min == "") delete goodsFilters[`filter_${this.id}_gte`];
      else goodsFilters[`filter_${this.id}_gte`] = this.min;
      this.$store.commit("setGoodsFilters", goodsFilters);
      await this.getGoods();
    },
    async filterMax() {
      let goodsFilters = this.$store.state.goodsFilters;
      if (this.min == goodsFilters[`filter_${this.id}_lte`]) return
      if (this.max == "") delete goodsFilters[`filter_${this.id}_lte`];
      else goodsFilters[`filter_${this.id}_lte`] = this.max;
      this.$store.commit("setGoodsFilters", goodsFilters);
      await this.getGoods();
    },
  },
};
</script>

<style>
</style>