<template>
  <v-card elevation="0">
    <v-card-title>{{ label }}</v-card-title>
    <v-checkbox
      v-for="(choice, i) in choices"
      v-model="selected"
      :value="choice"
      :label="choice"
      hide-details
      :key="`${i}-${choice}-${label}`"
    ></v-checkbox>
  </v-card>
</template>

<script>
import { mapActions } from "vuex";
export default {
  props: ["label", "choices", "id"],
  data() {
    return {
      selected: [],
    };
  },
  watch: {
    async selected(value) {
      let goodsFilters = this.$store.state.goodsFilters;
      if (value.length == 0) delete goodsFilters[`filter_${this.id}`]
      else goodsFilters[`filter_${this.id}`] = value.join(",");
      this.$store.commit("setGoodsFilters", goodsFilters);
      await this.getGoods();
    },
  },
  methods: {
    ...mapActions(["getGoods"]),
  },
};
</script>

<style>
</style>