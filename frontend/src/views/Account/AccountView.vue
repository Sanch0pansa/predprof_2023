<template>
  <div class="row pt-5">
    <PageBreadcrumbs :links-names="['account']"></PageBreadcrumbs>
    <div class="col-12">
        <h1>{{ user.username }} <RouterLink :to="{name: 'edit_account'}"><i role="button" class="fas fa-edit text-primary"></i></RouterLink></h1>
        <div class="d-flex align-items-center"><i class="fs-4 fab fa-telegram-plane me-2" :class="{
         'text-primary': true,
      }"></i>
          <span class="d-block" v-if="user.telegram_id">Привязан</span>
          <span class="d-block" v-else><RouterLink :to="{name: 'verify_telegram'}">Привязать</RouterLink></span>

          <i class="fas fa-ban text-danger fs-4 ms-2" role="button" v-if="user.telegram_id" @click="unlinkTelegramAction"></i>
        </div>
    </div>
    <div class="col-md-4">
      <PageSection :title="`Отслеживаемые ресурсы`">
        <SubscriptionsList
            v-model:pages="pages"
            v-if="pages.length"
        >

        </SubscriptionsList>
        <p class="text-muted" v-else>Нет отслеживаемых ресурсов</p>
      </PageSection>
      <PageSection :title="`Отзывы`">
        <PersonalReviewsList></PersonalReviewsList>
      </PageSection>
      <PageSection :title="`Сообщения о сбоях`">
        <PersonalReportsList></PersonalReportsList>
      </PageSection>
    </div>
    <div class="col-md-8">
      <PageSection :title="`События отслеживаемых ресурсов`">
        <PageEvents></PageEvents>
      </PageSection>
    </div>
  </div>
</template>

<script>
import {mapActions, mapState} from "vuex";
import PageSection from "@/components/UI/Section.vue";
import PagesList from "@/App.vue";
import SubscriptionsList from "@/components/items/SubscriptionsList.vue";
import PageEvents from "@/components/page/PageEvents.vue";
import ModalBtn from "@/components/UI/ModalBtn.vue";
import PersonalReviewsList from "@/components/items/PersonalReviewsList.vue";
import PersonalReportsList from "@/components/items/PersonalReportsList.vue";
import PageBreadcrumbs from "@/components/page/PageBreadcrumbs.vue";

export default {
  name: "AccountView.vue",
  components: {PersonalReportsList, PersonalReviewsList, ModalBtn, PageEvents, SubscriptionsList, PagesList, PageSection, PageBreadcrumbs},
  data() {
    return {
      pages: [],
    }
  },
  computed: {
    ...mapState({
      isAuth: state => state.auth.isAuth,
      user: state => state.auth.user,
    }),
  },

  methods: {
    ...mapActions({
      getAccountSubscriptions: "account/getAccountSubscriptions",
      unlinkTelegram: "telegram/unlinkTelegram",
      getUserData: "auth/getUserData",
    }),

    async unlinkTelegramAction() {
      if (confirm("Вы уверены, что хотите отвязать телеграм?")) {
        await this.unlinkTelegram();
        await this.getUserData();
      }
    },
  },

  async mounted() {
    this.pages = await this.getAccountSubscriptions();

  }
}
</script>

<style scoped>

</style>