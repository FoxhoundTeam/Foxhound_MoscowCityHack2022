<template>
  <v-card class="border border-danger" rounded outlined :href="company.href">
    <v-card-title>{{ company.name }}</v-card-title>
    <v-card-text>
      {{ company.description }}
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    company: {
      type: Object,
    },
  },
};
</script>

<style>
</style>