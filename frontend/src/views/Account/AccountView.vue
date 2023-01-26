<template>
  <div class="row pt-5">
    <h1>{{ user.username }}</h1>
    <div class="d-flex align-items-center"><i class="fs-4 fab fa-telegram-plane me-2" :class="{
       'text-primary': true,
    }"></i>
      <span class="d-block" v-if="user.telegram_id">Привязан</span>
      <span class="d-block" v-else><RouterLink :to="{name: 'verify_telegram'}">Привязать</RouterLink></span>
    </div>
  </div>
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