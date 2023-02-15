<template>
  <Block>
    <FormEl @handle="handle">
      <Inp
          :name="`email`"
          :label="`Email:`"
          v-model="email"
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
          :label="`Новый пароль (Оставьте поле пустым, чтобы не менять пароль):`"
          v-model="password"
          :type="`password`"
          v-model:errors="errorBag.password">
      </Inp>
      <hr>
      <Inp
          :name="`current_password`"
          :label="`Текущий пароль (для подтверждения изменений):`"
          v-model="current_password"
          :type="`password`"
          v-model:errors="errorBag.current_password">
      </Inp>
      <br>
      <Btn>Сохранить</Btn>
      <ErrorBag v-model:errors="errorBag.non_field_errors" v-model:success="errorBag.success"></ErrorBag>
    </FormEl>
  </Block>

</template>

<script>
import FormEl from "@/components/UI/FormEl.vue";
import {mapState, mapGetters, mapActions, mapMutations} from 'vuex'
import {errorBagFill} from "@/components/forms/errorBag.js";

export default {
  name: "AccountForm",
  components: {FormEl},
  data() {
    return {
      email: "",
      username: "",
      password: "",
      current_password: "",
      errorBag: {
        email: [],
        password: [],
        current_password: [],
        username: [],
        non_field_errors: [],
        success: "",
      }
    }
  },
  methods: {
    ...mapActions({
      patchUserData: 'auth/patchUserData'
    }),
    async handle(ev) {

      let data = {
        email: this.email,
        username: this.username,
        current_password: this.current_password,
      };

      if (this.password !== "") {
        data.password = this.password;
      }

      const res = await this.patchUserData(data);
      
      errorBagFill(this.errorBag, res);

      if (res.success) {
        setTimeout(() => {
          this.$router.replace({ name: 'account' })
        }, 1500);
      }

    }
  },

  computed: {
    ...mapState({
      isAuth: state => state.auth.isAuth,
      user: state => state.auth.user,
    }),
  },

  async mounted() {
    console.log(this.user);
    this.email = this.user.email;
    this.username = this.user.username;
    this.password = this.user.password;
  }
}
</script>

<style scoped>

</style>