<template>
  <v-card elevation="0">
    <v-card-title><h1>Каталог</h1></v-card-title>
    <v-list dense>
      <v-list-item-group>
        <v-list-item link :to="{name: 'Search', query: {category_id: category.id}}" v-for="(category, i) in $store.state.categories" :key="`${i}-${category.id}`">
          <v-list-item-content>
            <v-list-item-title v-text="category.name"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-card>
</template>

<script>
export default {

};
</script>

<style>
</style>