<template>
<header class="py-4 bg-white shadow">
  <nav class="navbar navbar-expand-lg">
  <div class="container">
      <RouterLink :class="[`navbar-brand`]" :to="{name: 'home'}">SiteChecker</RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li v-if="isAuth" class="nav-item me-3">
            <RouterLink :to="{name: 'create_page'}" :class="['btn btn-primary']">Добавить ресурс</RouterLink>
          </li>
          <li v-if="isAuth" class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              {{ user.username ? user.username : "" }}
              <i class="ms-2 fas text-primary" :class="{
                'fa-user': !isModerator && !isAdmin,
                'fa-user-tie': isModerator && !isAdmin,
                'fa-crown': isModerator && isAdmin,
                }"></i>
            </a>
            <ul class="dropdown-menu" style="position: absolute; left: auto; right: 0px;">
              <li class="dropdown-item" role="button"><RouterLink :to="{name: 'account'}"><i class="text-primary fas fa-user"></i> Личный кабинет</RouterLink></li>
              <li class="dropdown-item" role="button" v-if="isModerator">
                <RouterLink :to="{name: 'moderation'}">
                  <i class="text-primary fas fa-user-tie"></i>
                  Модер. панель
                </RouterLink>
              </li>
              <li class="dropdown-item" role="button" v-if="isAdmin">
                <RouterLink :to="{name: 'admin'}">
<!--                  <i class="text-primary fas fa-crown"></i>-->
                  <i class="text-primary fas fa-crown" style="margin-left: -3px;"></i>
                  Админ. панель
                </RouterLink>
              </li>
              <li class="dropdown-item text-danger" role="button" @click="logoutAction">
                <a href="#" class="text-danger"><i class="text-danger fas fa-sign-out-alt"></i> Выход</a>
                </li>
            </ul>
          </li>
          <li v-if="!isAuth" class="nav-item">
            <RouterLink :to="{name: 'login'}" :class="['nav-link text-primary']">Войти</RouterLink>
          </li>
          <li v-if="!isAuth" class="nav-item">
            <RouterLink :to="{name: 'register'}" :class="['nav-link text-primary']">Зарегистрироваться</RouterLink>
          </li>
        </ul>
      </div>
  </div>
  </nav>
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
        isModerator: state => state.auth.isModerator,
        isAdmin: state => state.auth.isAdmin,
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