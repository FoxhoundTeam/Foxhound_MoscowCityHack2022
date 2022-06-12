<template>
  <div fluid class="ml-5 mr-5">
    <v-row>
      <v-col cols="2">
        <filter-left-side />
      </v-col>
      <v-col cols="10">
        <v-row>
          <v-col
            cols="3"
            v-for="(good, i) in goods.items"
            :key="`${i}-${good.id}`"
          >
            <list-good-card :good="good" />
          </v-col>
        </v-row>
        <v-row v-if="loading">
          <v-col cols="3" v-for="i in 4" :key="`${i}-sceleton`">
            <v-sheet elevation="2">
              <v-skeleton-loader
                class="mx-auto"
                type="card-heading, list-item-three-line"
              ></v-skeleton-loader>
            </v-sheet>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row v-if="length > 1">
      <v-col cols="4"> &nbsp;</v-col>
      <v-col>
        <v-pagination v-model="page" :length="length" circle></v-pagination>
      </v-col>
      <v-col cols="4"> </v-col>
    </v-row>
  </div>
</template>

<script>
import FilterLeftSide from "@/components/FilterLeftSide.vue";
import ListGoodCard from "@/components/cards/ListGoodCard.vue";
import { mapActions } from "vuex";
export default {
  components: { FilterLeftSide, ListGoodCard },
  data() {
    return {
      page: 1,
    };
  },
  async mounted() {
    if (this.$route.query.page) {
      this.page = Number(this.$route.query.page);
    }
    await this.getGoods();
  },
  computed: {
    search() {
      return this.$store.state.search;
    },
    length() {
      return Math.round(this.goods.total / this.goods.size) + 1 || 1;
    },
    goods() {
      return this.$store.state.goods;
    },
    loading() {
        return this.$store.state.loadingGoods;
    }
  },
  methods: {
    ...mapActions(["getGoods"]),
  },
  watch: {
    async search(value) {
      if (this.page == 1) {
        await this.getGoods();
      } else {
        this.page = 1;
      }
      this.$router.push({
        name: "Search",
        query: { ...this.$route.query, q: value },
      });
    },
    async page(value) {
      await this.getGoods();
      this.$router.push({
        name: "Search",
        query: { ...this.$route.query, page: value },
      });
    },
  },
};
</script>

<style>
</style>