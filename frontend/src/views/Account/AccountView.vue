<template>
  <div class="row pt-5">
    <div class="col-12">
        <h1>{{ user.username }}</h1>
        <div class="d-flex align-items-center"><i class="fs-4 fab fa-telegram-plane me-2" :class="{
         'text-primary': true,
      }"></i>
          <span class="d-block" v-if="user.telegram_id">Привязан</span>
          <span class="d-block" v-else><RouterLink :to="{name: 'verify_telegram'}">Привязать</RouterLink></span>

          <i class="fas fa-ban text-danger fs-4 ms-2" role="button" v-if="user.telegram_id"></i>
        </div>
    </div>
    <div class="col-md-4">
      <PageSection :title="`Отслеживаемые ресурсы`">
        <SubscriptionsList :pages="pages">

        </SubscriptionsList>
      </PageSection>
    </div>
  </div>
</template>

<script>
import {mapActions, mapState} from "vuex";
import PageSection from "@/components/UI/Section.vue";
import PagesList from "@/App.vue";
import SubscriptionsList from "@/components/items/SubscriptionsList.vue";

export default {
  name: "AccountView.vue",
  components: {SubscriptionsList, PagesList, PageSection},
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
      getAccountSubscriptions: "account/getAccountSubscriptions"
    })
  },

  async mounted() {
    this.pages = await this.getAccountSubscriptions();

  }
}
</script>

<style scoped>

</style>