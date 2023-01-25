<template>
  <div class="row pt-5 text-center">
    <div class="col-md-3"></div>
    <div class="col-md-6">
      <h2 class="mb-5">Регистрация</h2>
      <RegisterForm></RegisterForm>
    </div>
  </div>

</template>

<script>
import RegisterForm from "@/components/forms/RegisterForm.vue";

export default {
  components: {RegisterForm},
  name: "RegisterView"
}
</script>

<style scoped>

</style>