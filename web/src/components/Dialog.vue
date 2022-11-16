<template>
  <v-dialog
    v-model="dialog"
    overlay-color="#93B3B9"
    :width="options.width"
    :height="options.height"
    :fullscreen="options.fullscreen && isMdAndDown"
    :scrollable="options.scrollable"
    :persistent="options.persistent"
    :content-class="isMdAndDown ? undefined : 'rounded-40'"
  >
    <component
      :is="component"
      v-on="{ ...options.events }"
      v-bind="{ ...options.props }"
    />
  </v-dialog>
</template>

<script>
export default {
  data: () => ({
    dialog: false,
    resolve: null,
    reject: null,
    component: null,
    options: {
      height: "500",
      width: "700",
      fullscreen: true,
      scrollable: true,
      persistent: false,
      props: {},
      events: {},
    },
  }),

  watch: {
    dialog(v) {
      if (v === false) {
        this.component = null;
        this.options.props = {};
        this.options.events = {};
      }
    },
  },

  computed: {
    isMdAndDown() {
      return this.$vuetify.breakpoint.mdAndDown;
    },
  },

  methods: {
    close() {
      this.dialog = false;
    },

    open(component, opt) {
      this.dialog = true;
      this.component = component;
      this.options = Object.assign(this.options, opt);

      return new Promise((resolve, reject) => {
        this.resolve = resolve;
        this.reject = reject;
      });
    },
  },
};
</script>
<style>
</style>