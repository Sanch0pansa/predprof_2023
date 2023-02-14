<template>
  <ul class="reviews" v-if="loaded">
    <PersonalReviewsListItem
        v-for="review in getReviews()"
        :mark="review.mark"
        :message="review.message"
        :added_at="review.added_at"
        :page="review.page"
        :id="review.id"
        :status="review.status"
        @delete="sendRemovePersonalReview"
    ></PersonalReviewsListItem>
    <li><b class="text-primary" v-if="reviews.length > 3" role="button" @click="() => {opened = !opened}">{{ opened ? "Свернуть" : `Развернуть (eщё ${reviews.length - 3})` }} </b></li>
  </ul>
  <Btn v-else @click="fetchPersonalReviews">Показать</Btn>
</template>

<script>
import PersonalReviewsListItem from "@/components/items/PersonalReviewsListItem.vue";
import {mapActions} from "vuex";
import Btn from "@/components/UI/Btn.vue";

export default {
  name: "PersonalReviewsList",
  components: {Btn, PersonalReviewsListItem},
  data() {
    return {
      reviews: [],
      loaded: false,
      opened: false,
    }
  },
  methods: {
    ...mapActions({
      getPersonalReviews: "reviews/getPersonalReviews",
      removePersonalReview: "reviews/removePersonalReview",
    }),

    async fetchPersonalReviews() {
      this.reviews = await this.getPersonalReviews();
      this.loaded = true;
    },

    async sendRemovePersonalReview(id) {
      await this.removePersonalReview({id: id});
    },

    getReviews() {
      if (this.opened) {
        return this.reviews;
      } else {
        return this.reviews.slice(0, 3);
      }
    }
  },
}
</script>

<style scoped>

</style>