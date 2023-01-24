<template>
<header class="py-4 bg-white shadow">
  <div class="container">
    <nav class="navbar">
      <RouterLink :class="[`navbar-brand`]" :to="{name: 'home'}">SiteChecker</RouterLink>
      <ul class="navbar-nav">
        <li v-if="isAuth" class="nav-item dropstart">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            {{ user.username ? user.username : "" }}
            <i class="ms-2 fas fa-user text-primary"></i>
          </a>
          <ul class="dropdown-menu" style="position: absolute;">
            <li class="dropdown-item" role="button">Личный кабинет</li>
            <li class="dropdown-item text-danger" role="button" @click="logoutAction">Выход</li>
          </ul>
        </li>
        <li v-else class="nav-item">
<!--          <a href="">Log in</a>-->
          <RouterLink :to="{name: 'login'}">Log in</RouterLink>
        </li>
      </ul>
    </nav>
  </div>
</header>
</template>

<script>
import {mapState, mapGetters, mapActions, mapMutations} from 'vuex'
import { RouterLink, RouterView } from 'vue-router'


export default {
  name: "PageHeader",
  computed: {
    ...mapState({
        isAuth: state => state.auth.isAuth,
        user: state => state.auth.user,
      }),
  },
  methods: {
    ...mapActions({
      logout: 'auth/logout'
    }),

    async logoutAction() {
      await this.logout();

      this.$router.replace({ name: 'login' });
    }
  }
}
</script>

<style scoped>

</style>