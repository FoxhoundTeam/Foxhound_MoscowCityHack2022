<template>
  <v-app-bar app>
    <v-app-bar-title
      ><router-link
        :to="{ name: 'Index' }"
        class="text-decoration-none text-dark"
        >FoxIndustry</router-link
      ></v-app-bar-title
    >
    <v-btn
      v-if="$route.name != 'SearchCompany'"
      link
      text
      :to="{ name: 'SearchCompany' }"
      class="text-dark"
      dark
      >Поиск производителей</v-btn
    >
    <v-btn
      v-if="!['Search', 'Index'].includes($route.name)"
      link
      text
      :to="{ name: 'Search' }"
      class="text-dark"
      dark
      >Поиск товаров</v-btn
    >
    <search-field
      v-if="$route.name == 'Search'"
      class="ml-5 mt-5 py-0"
      :dense="true"
    />
    <v-spacer></v-spacer>
    <v-btn
      v-if="!$store.state.isAuthenticated"
      color="primary"
      :to="{ name: 'Login' }"
      >Войти</v-btn
    >
    <div v-else>
      <v-btn
        v-if="$store.state.user.role === 'company'"
        link
        text
        :to="{ name: 'MyGoods' }"
        class="text-dark"
        dark
        >Мои товары</v-btn
      >
      <v-btn
        v-if="$store.state.user.role === 'company'"
        link
        text
        :to="{ name: 'AddGood' }"
        class="text-dark"
        dark
        >Добавить товар</v-btn
      >
      <v-btn
        v-if="['admin', 'moderator'].includes($store.state.user.role)"
        link
        text
        :to="{ name: 'AdminCategory' }"
        class="text-dark"
        dark
        >Настроить категории</v-btn
      >
      <v-btn
        v-if="['admin', 'moderator'].includes($store.state.user.role)"
        link
        text
        :to="{ name: 'AdminGood' }"
        class="text-dark"
        dark
        >Настроить товары</v-btn
      >
      <v-menu open-on-hover bottom offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn text class="text-dark" dark v-bind="attrs" v-on="on"
            ><v-icon left dark> mdi-account </v-icon>
            {{ $store.state.user.name }}
          </v-btn>
        </template>

        <v-list>
          <div v-if="$store.state.user.role === 'company'">
            <v-list-item v-if="$store.state.user.username">
              <v-list-item-title
                >ИНН: {{ $store.state.user.username }}</v-list-item-title
              >
            </v-list-item>
            <v-list-item v-if="$store.state.user.phone">
              <v-list-item-title
                >Телефон: {{ $store.state.user.phone }}</v-list-item-title
              >
            </v-list-item>
            <v-list-item v-if="$store.state.user.email">
              <v-list-item-title
                >Почта: {{ $store.state.user.email }}</v-list-item-title
              >
            </v-list-item>
          </div>
          <v-divider />
          <v-list-item link>
            <v-list-item-title @click="logout">Выйти</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </div>
  </v-app-bar>
</template>

<script>
import SearchField from "./fields/SearchField.vue";
import { mapActions } from "vuex";
export default {
  components: { SearchField },
  methods: {
    async logout() {
      await this.logoutDispatch();
      this.$router.replace({ name: "Index" });
    },
    ...mapActions({
      logoutDispatch: "logout",
    }),
  },
};
</script>

<style>
</style>