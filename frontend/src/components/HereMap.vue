<template>
  <div id="map" class="mt-0">
    <div
      id="mapContainer"
      style="height: 600px; width: 100%"
      ref="hereMap"
    ></div>
  </div>
</template>

<script>
const H = window.H;
export default {
  name: "HereMap",
  props: {
    center: Object,
  },
  data() {
    return {
      platform: null,
      apikey: "78bhiTliLYkKcCMilhXup8uJVRnoWcMvJaVJbFNOWrA",
      map: null,
      ui: null,
    };
  },
  watch: {
    items() {
      this.addItems();
    },
  },
  async mounted() {
    // Initialize the platform object:
    const platform = new window.H.service.Platform({
      apikey: this.apikey,
    });
    this.platform = platform;
    this.initializeHereMap();
    this.addItems();
  },
  computed: {
    items() {
      if (!this.$store.state.showObjects) return [];
      let items = [...this.$store.state.items];
      return items.sort((a, b) => {
        if (a.size >= b.size) {
          return -1;
        } else {
          return 1;
        }
      });
    },
  },
  methods: {
    initializeHereMap() {
      // rendering map

      const mapContainer = this.$refs.hereMap;
      // Obtain the default map types from the platform object
      var maptypes = this.platform.createDefaultLayers();

      // Instantiate (and display) a map object:
      var map = new H.Map(mapContainer, maptypes.vector.normal.map, {
        zoom: 13,
        center: this.center,
      });

      addEventListener("resize", () => map.getViewPort().resize());

      // add behavior control
      new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

      // add UI
      this.ui = H.ui.UI.createDefault(map, maptypes);
      // End rendering the initial map

      this.map = map;
    },
  },
};
</script>

<style scoped>
#map {
  text-align: center;
  background-color: #ccc;
}
</style>