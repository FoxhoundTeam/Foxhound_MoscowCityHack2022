<template>
  <v-card>
    <v-card-title>{{ company.name }}</v-card-title>
    <v-card-text>
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">Информация о производителе</th>
              <th class="text-left"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="company.address">
              <td>Адрес</td>
              <td>{{ company.address }}</td>
            </tr>
            <tr v-if="company.phone">
              <td>Телефон</td>
              <td>{{ company.phone }}</td>
            </tr>
            <tr v-if="company.site">
              <td>Сайт</td>
              <td>{{ company.site }}</td>
            </tr>
            <tr v-if="company.email">
              <td>Почта</td>
              <td>{{ company.email }}</td>
            </tr>
            <tr v-if="company.username">
              <td>ИНН</td>
              <td>{{ company.username }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  computed: {
    ...mapGetters(["companyById"]),
    company() {
      return this.companyById(this.$route.params.id) || {};
    },
  },
};
</script>

<style>
</style>