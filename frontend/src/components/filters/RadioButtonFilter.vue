<template>
  <v-card elevation="0">
    <v-card-title>{{ label }}</v-card-title>
    <v-radio-group v-model="selected">
      <v-radio
        v-for="(choice, i) in choices"
        :value="choice"
        :label="choice"
        :key="`${i}-${choice}-${label}`"
      ></v-radio>
    </v-radio-group>
  </v-card>
</template>

<script>
import { mapActions } from "vuex";
export default {
  props: ["label", "choices", "id"],
  data() {
    return {
      selected: null,
    };
  },
  watch: {
    async selected(value) {
      let goodsFilters = this.$store.state.goodsFilters;
      goodsFilters[`filter_${this.id}`] = value;
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