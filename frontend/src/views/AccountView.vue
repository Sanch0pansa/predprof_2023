<template>
  <h1>hgfhgfgh</h1>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "AccountView.vue",
  data() {
    return {

    }
  },
  computed: {
    ...mapState({
      isAuth: state => state.auth.isAuth,
      user: state => state.auth.user,
    }),
  }
}
</script>

<style scoped>

</style>