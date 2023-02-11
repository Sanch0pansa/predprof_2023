<template>
  <div class="row pt-5">
    <div class="col-12">
      <h1>Панель администратора</h1>
    </div>
    <div class="col-12 mt-2">
      <PageSection :title="`Список уполномоченных пользователей`">
        <ModalBtn id="addingStaffUser">Добавить</ModalBtn>
        <PageTable
            class="mt-3"
            :headers="['Пользователь', 'Права', 'Действия']"
            :data="staffUsersForTable"
            :no-load-more="true"
        ></PageTable>
      </PageSection>
    </div>
    <Modal id="addingStaffUser" title="Добавление уполномоченного пользователя">
      <AddingStaffUserForm @updateStaffUsers="fetchStaffUsers"></AddingStaffUserForm>
    </Modal>
  </div>
</template>

<script>
import PageSection from "@/components/UI/Section.vue";
import PageTable from "@/components/page/PageTable.vue";
import Btn from "@/components/UI/Btn.vue";
import {mapActions} from "vuex";
import ModalBtn from "@/components/UI/ModalBtn.vue";
import Modal from "@/components/UI/Modal.vue";
import AddingStaffUserForm from "@/components/forms/AddingStaffUserForm.vue";

export default {
  name: "AdminView",
  components: {AddingStaffUserForm, Modal, ModalBtn, Btn, PageTable, PageSection},
  data() {
    return {
      staffUsers: [],
      staffUsersForTable: [],
    }
  },
  methods: {
    ...mapActions({
      getStaffUsers: "admin/getStaffUsers",
      changeUserRights: "admin/changeUserRights"
    }),

    async sendChangeUserRights(data) {
      await this.changeUserRights(data);
      await this.fetchStaffUsers();
    },

    async fetchStaffUsers() {
      this.staffUsers = await this.getStaffUsers();

      this.staffUsersForTable = [];
      this.staffUsers.forEach(user => {
        let actions = user.is_admin ? [
          {
            text: "Сделать пользователем",
            click: () => this.sendChangeUserRights({id: user.id, newRight: 'user'}),
            cls: "btn-secondary"
          },
          {
            text: "Сделать модератором",
            click: () => this.sendChangeUserRights({id: user.id, newRight: 'moderator'}),
            cls: "btn-warning ms-2"
          },
        ] : [
          {
            text: "Сделать пользователем",
            click: () => this.sendChangeUserRights({id: user.id, newRight: 'user'}),
            cls: "btn-secondary"
          },
          {
            text: "Сделать администратором",
            click: () => this.sendChangeUserRights({id: user.id, newRight: 'admin'}),
            cls: "btn-primary ms-2"
          },
        ];
        this.staffUsersForTable.push([
          {text: user.username, href: 'account'},
          user.is_admin ? "Администратор" : "Модератор",
          actions,
        ]);
      });
    }
  },

  async mounted() {
    await this.fetchStaffUsers();
  }
}
</script>

<style scoped>

</style>