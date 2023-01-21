<template>
  <Block>
    <FormEl @handle="handle">
      <Inp :name="`login`" :label="`Логин:`" v-model="login"></Inp>
      <br>
      <Inp :name="`password`" :label="`Пароль:`" v-model="password" :type="`password`"></Inp>
      <br>
      <Btn>Войти</Btn>
    </FormEl>
  </Block>

</template>

<script>
import FormEl from "@/components/UI/FormEl.vue";
import {mapState, mapGetters, mapActions, mapMutations} from 'vuex'

export default {
  name: "LoginForm",
  components: {FormEl},
  data() {
    return {
      login: "",
      password: ""
    }
  },
  methods: {
    ...mapActions({
      auth: 'auth/authentificate'
    }),
    async handle(ev) {

      const res = await this.auth({
        login: this.login,
        password: this.password,
      });

      if (res.success) {

      }
    }
  }
}
</script>

<style scoped>

</style>