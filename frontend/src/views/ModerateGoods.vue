<template>
  <v-card elevation="0">
    <v-card-title>
      <h3 class="font-weight-bold text-h3 basil--text">
        Администрирование товаров
      </h3>
    </v-card-title>
    <v-divider></v-divider>
    <v-row class="px-4">
      <v-col cols="7">
        <v-text-field label="Название" outlined v-model="search"></v-text-field>
      </v-col>
      <v-col cols="5">
        <div class="d-flex align-items-center justify-content-end">
          <v-select
            label="Статус"
            outlined
            clearable
            v-model="status"
            :items="statuses"
          ></v-select>
          <v-tooltip bottom open-delay="500">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                class="mx-1 mb-5"
                v-bind="attrs"
                v-on="on"
                icon
                @click="showCreateGood"
              >
                <v-icon color="gray" v-bind="attrs" v-on="on"> add </v-icon>
              </v-btn>
            </template>
            <span>Добавить</span>
          </v-tooltip>
        </div>
      </v-col>
    </v-row>
    <v-row class="px-4">
      <v-col>
        <v-row>
          <v-col
            cols="4"
            v-for="(good, i) in goods.items"
            :key="`${i}-${good.id}`"
          >
            <list-good-card
              to=""
              @click="showEditGood(good)"
              :good="good"
              :show_category="true"
              :show_status="true"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row v-if="length > 1">
      <v-col cols="4"> &nbsp;</v-col>
      <v-col>
        <v-pagination v-model="page" :length="length" :total-visible="7" circle></v-pagination>
      </v-col>
      <v-col cols="4"> </v-col>
    </v-row>
    <edit-good-modal v-model="showEditModal" :good="editGood" />
    <create-good-admin-modal v-model="showCreateModal" @created="setGoods"/>
  </v-card>
</template>

<script>
import { STATUSES } from "@/consts";
import ListGoodCard from "@/components/cards/ListGoodCard.vue";
import EditGoodModal from "@/components/modals/EditGoodModal.vue";
import http from "@/http";
import CreateGoodAdminModal from '@/components/modals/CreateGoodAdminModal.vue';
export default {
  components: { ListGoodCard, EditGoodModal, CreateGoodAdminModal, },
  data() {
    return {
      goods: {
        size: 12,
        total: 0,
      },
      page: 1,
      statuses: STATUSES,
      status: null,
      search: "",
      editGood: {},
      showEditModal: false,
      showCreateModal: false,
    };
  },
  computed: {
    length() {
      return Math.round(this.goods.total / this.goods.size) + 1;
    },
  },
  async mounted() {
    await this.setGoods();
  },
  watch: {
    async page() {
      await this.setGoods();
    },
    async status() {
      await this.setGoods();
    },
    async search() {
      await this.setGoods();
    },
  },
  methods: {
    async setGoods() {
      let filters = {
        page: this.page,
        size: 12,
      };
      if (this.search) filters.name = this.search;
      if (this.status) filters.status = this.status;
      let response = (await http.getList("Good", filters, true)).data;
      this.goods = response;
    },
    showEditGood(good) {
      this.editGood = good;
      this.showEditModal = true;
    },
    showCreateGood() {
        this.showCreateModal = true;
    }
  },
};
</script>

<style>
</style>