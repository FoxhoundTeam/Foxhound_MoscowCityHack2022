<template>
  <v-card elevation="0">
    <v-card-title><h1>Каталог</h1></v-card-title>
    <v-row>
      <v-col cols="3" v-for="(part, i) in parts" :key="i">
        <v-list dense>
          <v-list-item-group>
            <v-list-item
              link
              :to="{ name: 'Search', query: { category_id: category.id } }"
              v-for="(category, i) in part"
              :key="`${i}-${category.id}`"
            >
              <v-list-item-content>
                <v-list-item-title v-text="category.name"></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
export default {
  computed: {
    parts() {
      let total = this.$store.state.categories.length;
      let part = Math.round(total / 4);
      let parts = [];
      for (const i of [0, 1, 2, 3]) {
        parts.push(
          this.$store.state.categories.slice(i * part, i * part + part)
        );
      }
      return parts;
    },
  },
};
</script>

<style>
</style>