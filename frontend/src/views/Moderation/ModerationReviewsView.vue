<template>
  <div class="row pt-5">
    <div class="col-12">
      <h1>Модерация отзывов</h1>
    </div>
    <div class="col-12 mt-5 d-flex flex-column gap-3">
      <ModerationReviewsList :reviews="reviews" @action="sendPatchReviewStatus"></ModerationReviewsList>
    </div>
  </div>
</template>

<script>
import {mapActions} from "vuex";
import ModerationReviewsList from "@/components/items/ModerationReviewsList.vue";

export default {
  name: "ModerationReviewsView",
  components: {ModerationReviewsList},
  data() {
    return {
      reviews: {
        moderation: [

        ],
        rejected: [

        ]
      }
    }
  },
  methods: {
    ...mapActions({
      getModerationReviews: "moderation/getModerationReviews",
      getRejectedReviews: "moderation/getRejectedReviews",
      patchReviewStatus: "moderation/patchReviewStatus",
    }),
    async fetchReviews() {
      this.reviews.moderation = await this.getModerationReviews();
      this.reviews.rejected = await this.getRejectedReviews();
    },

    async sendPatchReviewStatus({id, action}) {
      let res = await this.patchReviewStatus({
        id: id,
        action: action
      });

      if (res.success) {
        await this.fetchReviews();
      }
    }
  },
  async mounted() {
    await this.fetchReviews();
  }
}
</script>

<style scoped>

</style>