<template>
  <v-card rounded outlined class="h-100" :href="good.href">
    <v-card-title>{{ good.name }}</v-card-title>
    <v-card-text>
      {{ good.description }}
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    good: {
      type: Object,
    },
  },
};
</script>

<style>
</style>