<template>
  <Block>
    <FormEl @handle="handle">
      <Inp
          :name="`login`"
          :label="`Логин:`"
          v-model="login"
          v-model:errors="errorBag.email">
      </Inp>
      <br>

      <Inp
          :name="`username`"
          :label="`Имя пользователя:`"
          v-model="username"
          v-model:errors="errorBag.username">
      </Inp>
      <br>

      <Inp
          :name="`password`"
          :label="`Пароль:`"
          v-model="password"
          :type="`password`"
          v-model:errors="errorBag.password">
      </Inp>
      <br>
      <Btn>Войти</Btn>
      <ErrorBag v-model:errors="errorBag.non_field_errors" v-model:success="errorBag.success"></ErrorBag>
    </FormEl>
  </Block>

</template>

<script>
import FormEl from "@/components/UI/FormEl.vue";
import {mapState, mapGetters, mapActions, mapMutations} from 'vuex'
import {errorBagFill} from "@/components/forms/errorBag.js";

export default {
  name: "RegisterForm",
  components: {FormEl},
  data() {
    return {
      login: "",
      username: "",
      password: "",
      errorBag: {
        email: [],
        password: [],
        username: [],
        non_field_errors: [],
        success: "",
      }
    }
  },
  methods: {
    ...mapActions({
      register: 'auth/registrate'
    }),
    async handle(ev) {

      const res = await this.register({
        login: this.login,
        password: this.password,
        username: this.username,
      });

      errorBagFill(this.errorBag, res);

      if (res.success) {
        setTimeout(() => {
          this.$router.replace({ name: 'home' })
        }, 1500);
      }

    }
  }
}
</script>

<style scoped>

</style>