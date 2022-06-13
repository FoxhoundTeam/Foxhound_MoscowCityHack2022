<template>
  <div fluid class="mx-5 mt-5">
    <v-row v-if="Object.values(companyFactory).length != 0">
      <v-col cols="12">
        <company-factory-card :company="companyFactory" />
      </v-col>
    </v-row>
    <v-row v-if="length > 1">
      <v-col cols="4"> &nbsp;</v-col>
      <v-col>
        <v-pagination v-model="page" :length="length" :total-visible="7" circle></v-pagination>
      </v-col>
      <v-col cols="4"> </v-col>
    </v-row>
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
            <list-good-card :good="good" :show_category="true"/>
          </v-col>
        </v-row>
        <v-row v-if="loading">
          <v-col cols="3" v-for="i in 12" :key="`${i}-sceleton`">
            <v-sheet elevation="2">
              <v-skeleton-loader
                class="mx-auto"
                type="card-heading, list-item-three-line"
              ></v-skeleton-loader>
            </v-sheet>
          </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-row>
          <v-col
            cols="3"
            v-for="(good, i) in goodsFromNetwork"
            :key="`${i}-${good.name}`"
          >
            <list-good-card-dynamic :good="good" />
          </v-col>
        </v-row>
        <v-row v-if="loadingFromNetwork">
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
  </div>
</template>

<script>
import FilterLeftSide from "@/components/FilterLeftSide.vue";
import ListGoodCard from "@/components/cards/ListGoodCard.vue";
import { mapActions } from "vuex";
import http from "@/http";
import ListGoodCardDynamic from "@/components/cards/ListGoodCardDynamic.vue";
import CompanyFactoryCard from "@/components/cards/CompanyFactoryCard.vue";
export default {
  components: {
    FilterLeftSide,
    ListGoodCard,
    ListGoodCardDynamic,
    CompanyFactoryCard,
  },
  data() {
    return {
      page: 1,
      goodsFromNetwork: [],
      loadingFromNetwork: false,
      companyFactory: {},
    };
  },
  async mounted() {
    if (this.$route.query.page) {
      this.page = Number(this.$route.query.page);
    }
    await this.getGoods();
    await this.getGoodsFromNetwork();
    await this.getCompanyFactory();
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
    },
  },
  methods: {
    ...mapActions(["getGoods"]),
    async getGoodsFromNetwork() {
      this.goodsFromNetwork = [];
      if (!this.search) return
      this.loadingFromNetwork = true;
      this.goodsFromNetwork = (
        await http.getList("GoodsFromNetwork", { q: this.search }, true)
      ).data;
      this.loadingFromNetwork = false;
    },
    async getCompanyFactory() {
      this.companyFactory = {};
      if (!this.search) return
      this.goodsFromNetwork = (
        await http.getList("CompanyFacrory", { q: this.search }, true)
      ).data;
    },
  },
  watch: {
    async search(value) {
      this.$router.push({
        name: "Search",
        query: { ...this.$route.query, q: value },
      });
      if (this.page == 1) {
        await this.getGoods();
      } else {
        this.page = 1;
      }
      await this.getGoodsFromNetwork();
      await this.getCompanyFactory();
    },
    async page(value) {
      await this.getGoods();
      this.$router.push({
        name: "Search",
        query: { ...this.$route.query, page: value,},
      });
    },
  },
};
</script>

<style>
</style>