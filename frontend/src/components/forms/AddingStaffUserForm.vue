<template>
  <FormEl @handle="handle">
    <Inp
        label="Поиск пользователя по имени"
        name=""
        v-model="userSearch"
        @input="search"
    ></Inp>

    <ul v-if="!user.id" class="mt-2">
      <li v-for="usr in users" role="button" class="text-primary" @click="selectUser(usr)">{{ usr.username }}</li>
    </ul>
    <div class="mt-2" v-else>
      <div class="text-secondary">{{ user.username }} <i class="text-danger fas fa-times" role="button" @click="search"></i></div>
    </div>
    <hr>
    <Sel
          label="Роль"
          name=""
          :options="[
            {text: 'Модератор', value: 'moderator'},
            {text: 'Администратор', value: 'admin'}
          ]"
          v-model="rights"
    ></Sel>
    <hr>
    <Btn @click="handle">Добавить</Btn>
    <ErrorBag v-model:errors="errorBag.non_field_errors" v-model:success="errorBag.success"></ErrorBag>
  </FormEl>
</template>

<script>
import Inp from "@/components/UI/Inp.vue";
import Sel from "@/components/UI/Sel.vue";
import {mapActions} from "vuex";

export default {
  name: "AddingStaffUserForm",
  components: {Sel, Inp},
  data() {
    return {
      userSearch: "",
      users: [],
      user: {id: 0, username: 0},
      rights: "moderator",
      errorBag: {
        non_field_errors: [],
        success: ""
      }
    }
  },
  methods: {
    ...mapActions({
      searchUser: "admin/searchUser",
      changeUserRights: "admin/changeUserRights"
    }),

    async handle() {
      if (this.user.id === 0) {
        let notSelectedUserErrorText = "Пользователь не выбран";
        if (!this.errorBag.non_field_errors.includes(notSelectedUserErrorText)) {
          this.errorBag.non_field_errors.push(notSelectedUserErrorText);
        }

        return [];
      }

      let res = await this.changeUserRights({id: this.user.id, rights: this.rights});
      if (!res.success) {
        this.errorBag.non_field_errors.push("Что-то пошло не так");
      } else {
        this.errorBag.success = "Полномочия пользователя успешно изменены";
        this.$emit('updateStaffUsers');
      }
    },

    async search() {
      this.user = {id: 0, username: 0};
      if (this.userSearch === "") {
        this.users = [];
      } else {
        this.users = await this.searchUser({search: this.userSearch});
      }
    },

    async selectUser(user) {
      this.users = [];
      this.user = user;
    }
  },
}
</script>

<style scoped>

</style>