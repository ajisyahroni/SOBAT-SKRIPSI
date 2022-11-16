<template>
  <v-app>
    <v-main style="background-color: #f5f5f5">
      <router-view />
    </v-main>
    <Dialog ref="dialog" />
  </v-app>
</template>

<script>
import Dialog from "./components/Dialog.vue";
import Vue from "vue";
export default {
  name: "App",
  components: {
    Dialog,
  },

  created() {
    const appendQuery = () => {
      let { query } = this.$route;

      let x = {
        ...query,
        pop: "true",
      };

      this.$router.push({ query: x }).catch((e) => e);
    };

    Vue.prototype.$dialog = {
      open: (c, opt) => {
        appendQuery();
        return this.$refs.dialog.open(c, opt);
      },
      close: () => this.$refs.dialog.close(),
    };
  },

  mounted() {
    window.addEventListener("popstate", () => {
      this.$dialog.close();
    });
  },

  data: () => ({
    //
  }),
};
</script>
