<template>
  <div class="row pt-5 text-center">
    <div class="col-md-4"></div>
    <div class="col-md-4">
      <h2 class="mb-5">Авторизация</h2>
      <LoginForm></LoginForm>
    </div>
  </div>

</template>

<script>
import LoginForm from "@/components/forms/LoginForm.vue";

export default {
  components: {LoginForm},
  name: "LoginView"
}
</script>

<style scoped>

</style>