<template>
  <div class="row pt-5 text-center">
    <div class="col-md-3"></div>
    <div class="col-md-6">
      <h2 class="mb-5">Авторизация</h2>
      <LoginForm></LoginForm>
      <RouterLink :to="{name: 'register'}" :class="`d-block mt-5`">Создать учётную запись</RouterLink>
    </div>
  </div>

</template>

<script>
import LoginForm from "@/components/forms/LoginForm.vue";
import {RouterLink} from "vue-router";

export default {
  components: {LoginForm, RouterLink},
  name: "LoginView"
}
</script>

<style scoped>

</style>