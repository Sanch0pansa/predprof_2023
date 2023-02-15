<template>
  <li class="review">
    <div class="review-header">
      <Username :username="added_by_user__username" :id="added_by_user"></Username>
      <div class="text-muted">{{ (new Date(added_at)).toLocaleString("ru", {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: "numeric",
        minute: "numeric",
        second: "numeric"
      }) }}</div>
    </div>
    <div class="review-mark">
      <i class="fas fa-star fs-5" v-for="i in 5"
         :class="{
            'text-warning': i <= mark ,
            'text-secondary': i > mark
         }"
      ></i>
    </div>
    <div class="review-content">
      <p>{{ message }}</p>
      <Btn v-if="getIsModerator()" class="btn-warning mt-3" @click="sendPatchReviewStatus">Отправить на модерацию</Btn>
    </div>
  </li>
</template>

<script>
import {mapActions, mapGetters} from "vuex";
import Username from "@/components/UI/Username.vue";

export default {
  name: "ReviewsListItem",
  components: {Username},
  props: {
    id: {
      required: true,
      type: Number,
    },
    added_by_user: {
      required: true,
      type: Number
    },
    added_by_user__username: {
      required: true,
      type: String
    },
    added_at: {
      required: true,
      type: String
    },
    message: {
      required: true,
      type: String
    },
    mark: {
      required: true,
      type: Number
    }
  },
  methods: {
    ...mapGetters({
      getIsModerator: "auth/getIsModerator"
    }),

    ...mapActions({
      patchReviewStatus: "moderation/patchReviewStatus"
    }),

    async sendPatchReviewStatus() {
      await this.patchReviewStatus({id: this.id, action: 'revise'});
      this.$router.replace({name: "moderation_reviews"});
    }
  }
}
</script>

<style scoped>

</style>