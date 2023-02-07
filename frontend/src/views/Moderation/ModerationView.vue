<template>
  <div class="row pt-5">
    <div class="col-12">
      <h1>Панель модератора</h1>
    </div>

    <div class="col-md-4 mt-3">
      <RouterLink :to="{name: 'moderation_pages'}">
        <Block class="d-flex align-items-center flex-column">
          <i class="fas fa-file text-primary position-relative" style="font-size: 65px;">
            <span v-if="$store.state.moderation.pages" style="font-size: 16px;" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
              {{ $store.state.moderation.pages }}
              <span class="visually-hidden">unread messages</span>
            </span>
          </i>
            <h5 class="mt-3 text-center">Ресурсы</h5>
        </Block>
      </RouterLink>
    </div>

    <div class="col-md-4 mt-3">
      <RouterLink to="/account">
        <Block class="d-flex align-items-center flex-column">
          <i class="fas fa-comments text-primary position-relative" style="font-size: 65px;">
            <span v-if="$store.state.moderation.reviews" style="font-size: 16px;" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
              {{ $store.state.moderation.reviews }}
              <span class="visually-hidden">unread messages</span>
            </span>
          </i>
          <h5 class="mt-3 text-center">Отзывы</h5>
        </Block>
      </RouterLink>
    </div>

    <div class="col-md-4 mt-3">
      <RouterLink to="/account">
        <Block class="d-flex align-items-center flex-column">
          <i class="fas fa-exclamation-circle text-primary position-relative" style="font-size: 65px;">
            <span v-if="$store.state.moderation.reports" style="font-size: 16px;" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
              {{ $store.state.moderation.reports }}
              <span class="visually-hidden">unread messages</span>
            </span>
          </i>
          <h5 class="mt-3 text-center">Сообщения о сбоях</h5>
        </Block>
      </RouterLink>
    </div>
  </div>
</template>

<script>
import Block from "@/components/UI/Block.vue";

export default {
  name: "ModerationView",
  components: {Block},
  data() {
    return {
      pages_on_moderation: 0,
      reviews_on_moderation: 12,
      reports_on_moderation: 5,
    }
  },

  methods: {

  },

  async mounted() {

  }
}
</script>

<style scoped>

</style>