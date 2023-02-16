<template>
<div class="row pt-5">
  <PageBreadcrumbs :links-names="['account', 'edit_account']"></PageBreadcrumbs>
  <div class="col-12">
    <h1>{{ user.username }}</h1>
  </div>

  <div class="col-12 pt-4">
      <AccountForm></AccountForm>
  </div>
</div>
</template>

<script>
import {mapState} from "vuex";
import Block from "@/components/UI/Block.vue";
import AccountForm from "@/components/forms/AccountForm.vue";
import PageBreadcrumbs from "@/components/page/PageBreadcrumbs.vue";

export default {
  name: "AccountEditView.vue",
  components: {PageBreadcrumbs, AccountForm, Block},
  computed: {
    ...mapState({
      isAuth: state => state.auth.isAuth,
      user: state => state.auth.user,
    }),
  },
}
</script>

<style scoped>

</style>